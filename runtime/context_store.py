"""Context store for retrieval over repository files."""
from __future__ import annotations

import ast
import hashlib
import math
import os
import re
import shutil
import tempfile
import uuid
from pathlib import Path

import chromadb
from chromadb.errors import NotFoundError


class ContextStore:
    """Persistent retrieval store backed by ChromaDB."""

    _EXCLUDED_DIRS = {".venv", "__pycache__", ".git", "node_modules"}
    _EXCLUDED_SUFFIXES = {".pyc"}
    _ALLOWED_SUFFIXES = {".py", ".md"}
    _HINTS_FILE = ".abracapocus_context"

    def __init__(self) -> None:
        self.client: chromadb.PersistentClient | None = None
        self.collection = None
        self.collection_name = "context_store"
        self.repo_root: Path | None = None
        self.hint_paths: list[str] = []

    def index_repo(self, root: str | Path) -> None:
        """Index all eligible files under the provided repository root."""
        repo_root = Path(root).resolve()
        self.repo_root = repo_root
        self.hint_paths = self._load_hint_paths()
        self._ensure_store()
        self.collection_name = "context_store"
        try:
            self.client.delete_collection(name=self.collection_name)
            self.collection = self.client.get_or_create_collection(name=self.collection_name)
        except Exception:
            self._reinitialize_store_with_tmp()
            self.collection_name = f"context_store_{uuid.uuid4().hex[:8]}"
            self.collection = self.client.get_or_create_collection(name=self.collection_name)

        ids: list[str] = []
        documents: list[str] = []
        embeddings: list[list[float]] = []
        metadatas: list[dict[str, object]] = []

        for file_path in self._iter_eligible_files(repo_root):
            rel_path = file_path.relative_to(repo_root).as_posix()
            for chunk_index, chunk_text in enumerate(self._chunk_file(file_path)):
                chunk_id = self._chunk_id(rel_path, chunk_index)
                ids.append(chunk_id)
                documents.append(chunk_text)
                embeddings.append(self._embed_text(chunk_text))
                metadatas.append(
                    {
                        "path": rel_path,
                        "chunk_index": chunk_index,
                        "ext": file_path.suffix,
                    }
                )

        if ids:
            self.collection.add(ids=ids, documents=documents, embeddings=embeddings, metadatas=metadatas)

    def update_files(self, changed_files: list[str | Path]) -> None:
        """Re-index only provided files and remove outdated chunks."""
        if self.repo_root is None:
            raise ValueError("ContextStore must be indexed before update_files().")

        self._ensure_store()
        self._ensure_collection()
        for changed_file in changed_files:
            rel_path = self._normalize_relative_path(changed_file)
            try:
                self.collection.delete(where={"path": rel_path})
            except NotFoundError:
                self._ensure_collection(force=True)

            abs_path = self.repo_root / rel_path
            if not abs_path.exists() or not self._is_eligible_file(abs_path):
                continue

            chunks = self._chunk_file(abs_path)
            if not chunks:
                continue

            ids = [self._chunk_id(rel_path, idx) for idx in range(len(chunks))]
            embeddings = [self._embed_text(chunk) for chunk in chunks]
            metadatas = [
                {"path": rel_path, "chunk_index": idx, "ext": abs_path.suffix}
                for idx in range(len(chunks))
            ]
            self.collection.add(ids=ids, documents=chunks, embeddings=embeddings, metadatas=metadatas)

    def query(self, text: str, k: int = 15) -> list[dict[str, object]]:
        """Return top-k relevant chunks with source file path."""
        self._ensure_store()
        self.hint_paths = self._load_hint_paths()
        if k <= 0:
            return []

        results = self.collection.query(
            query_embeddings=[self._embed_text(text)],
            n_results=k,
            include=["documents", "metadatas", "distances"],
        )

        documents = (results.get("documents") or [[]])[0]
        metadatas = (results.get("metadatas") or [[]])[0]
        distances = (results.get("distances") or [[]])[0]

        matches: list[dict[str, object]] = []
        for document, metadata, distance in zip(documents, metadatas, distances):
            matches.append(
                {
                    "path": metadata.get("path") if metadata else None,
                    "chunk": document,
                    "distance": distance,
                }
            )
        self._append_hint_matches(matches)
        return matches

    def _load_hint_paths(self) -> list[str]:
        if self.repo_root is None:
            return []

        hint_file = self.repo_root / self._HINTS_FILE
        if not hint_file.exists():
            return []

        hint_paths: list[str] = []
        lines = hint_file.read_text(encoding="utf-8", errors="ignore").splitlines()
        for line in lines:
            pattern = line.split("#", 1)[0].strip()
            if not pattern:
                continue
            for path in self.repo_root.glob(pattern):
                if not path.is_file():
                    continue
                rel_path = path.resolve().relative_to(self.repo_root).as_posix()
                if rel_path not in hint_paths:
                    hint_paths.append(rel_path)

        return hint_paths

    def _append_hint_matches(self, matches: list[dict[str, object]]) -> None:
        seen_paths = {match.get("path") for match in matches}
        for hint_path in self.hint_paths:
            if hint_path in seen_paths:
                continue

            data = self.collection.get(where={"path": hint_path}, include=["documents", "metadatas"])
            documents = data.get("documents") or []
            metadatas = data.get("metadatas") or []
            if not documents:
                continue

            metadata = metadatas[0] if metadatas else {"path": hint_path}
            matches.append(
                {
                    "path": metadata.get("path"),
                    "chunk": documents[0],
                    "distance": None,
                }
            )
            seen_paths.add(hint_path)

    def _ensure_store(self) -> None:
        if self.repo_root is None:
            raise ValueError("Repository root is not set. Call index_repo(root) first.")
        if self.client is not None and self.collection is not None:
            self._ensure_collection()
            return

        persist_path = self.repo_root / "state" / "chroma"
        temp_path = persist_path / "tmp"
        persist_path.mkdir(parents=True, exist_ok=True)
        temp_path.mkdir(parents=True, exist_ok=True)
        os.environ.setdefault("TMPDIR", str(temp_path))
        os.environ.setdefault("SQLITE_TMPDIR", str(temp_path))
        try:
            self.client = chromadb.PersistentClient(path=str(persist_path))
            self.collection = self.client.get_or_create_collection(name=self.collection_name)
        except Exception:
            self.client = None
            self.collection = None
            recovered_path = self.repo_root / "state" / "chroma_recovered"
            shutil.rmtree(recovered_path, ignore_errors=True)
            recovered_path.mkdir(parents=True, exist_ok=True)
            temp_path = recovered_path / "tmp"
            temp_path.mkdir(parents=True, exist_ok=True)
            os.environ["TMPDIR"] = str(temp_path)
            os.environ["SQLITE_TMPDIR"] = str(temp_path)
            self.client = chromadb.PersistentClient(path=str(recovered_path))
            self.collection = self.client.get_or_create_collection(name=self.collection_name)

    def _reinitialize_store_with_tmp(self) -> None:
        self.client = None
        self.collection = None
        persist_path = Path(tempfile.mkdtemp(prefix="abracapocus_chroma_"))
        temp_path = persist_path / "tmp"
        temp_path.mkdir(parents=True, exist_ok=True)
        os.environ["TMPDIR"] = str(temp_path)
        os.environ["SQLITE_TMPDIR"] = str(temp_path)
        self.client = chromadb.PersistentClient(path=str(persist_path))

    def _ensure_collection(self, force: bool = False) -> None:
        if self.client is None:
            return
        if force or self.collection is None:
            self.collection = self.client.get_or_create_collection(name=self.collection_name)
            return
        try:
            self.collection.count()
        except NotFoundError:
            self.collection = self.client.get_or_create_collection(name=self.collection_name)

    def _iter_eligible_files(self, root: Path):
        for current_root, dirs, files in os.walk(root):
            dirs[:] = [directory for directory in dirs if directory not in self._EXCLUDED_DIRS]

            current_path = Path(current_root)
            for file_name in files:
                file_path = current_path / file_name
                if self._is_eligible_file(file_path):
                    yield file_path

    def _is_eligible_file(self, path: Path) -> bool:
        suffix = path.suffix.lower()
        if suffix in self._EXCLUDED_SUFFIXES:
            return False
        if suffix not in self._ALLOWED_SUFFIXES:
            return False
        for part in path.parts:
            if part in self._EXCLUDED_DIRS:
                return False
        return True

    def _normalize_relative_path(self, value: str | Path) -> str:
        path = Path(value)
        if path.is_absolute():
            if self.repo_root is None:
                raise ValueError("Repository root is not set.")
            path = path.resolve().relative_to(self.repo_root)
        return path.as_posix()

    def _chunk_file(self, file_path: Path) -> list[str]:
        content = file_path.read_text(encoding="utf-8", errors="ignore")
        if file_path.suffix == ".py":
            return self._chunk_python(content)
        if file_path.suffix == ".md":
            return self._chunk_markdown(content)
        return [content] if content.strip() else []

    def _chunk_python(self, source: str) -> list[str]:
        try:
            tree = ast.parse(source)
        except SyntaxError:
            return [source] if source.strip() else []

        lines = source.splitlines()
        chunks: list[str] = []
        spans: list[tuple[int, int]] = []

        for node in tree.body:
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                start = max(node.lineno - 1, 0)
                end = max((getattr(node, "end_lineno", node.lineno) or node.lineno), node.lineno)
                spans.append((start, end))

        if not spans:
            return [source] if source.strip() else []

        cursor = 0
        for start, end in spans:
            if start > cursor:
                prefix = "\n".join(lines[cursor:start]).strip()
                if prefix:
                    chunks.append(prefix)
            block = "\n".join(lines[start:end]).strip()
            if block:
                chunks.append(block)
            cursor = end

        if cursor < len(lines):
            suffix = "\n".join(lines[cursor:]).strip()
            if suffix:
                chunks.append(suffix)

        return chunks

    def _chunk_markdown(self, source: str) -> list[str]:
        paragraphs = [paragraph.strip() for paragraph in re.split(r"\n\s*\n", source) if paragraph.strip()]
        return paragraphs

    def _chunk_id(self, rel_path: str, chunk_index: int) -> str:
        return f"{rel_path}::{chunk_index}"

    def _embed_text(self, text: str) -> list[float]:
        dim = 256
        vector = [0.0] * dim
        tokens = re.findall(r"[A-Za-z0-9_]+", text.lower())
        if not tokens:
            return vector

        for token in tokens:
            digest = hashlib.sha256(token.encode("utf-8")).digest()
            index = int.from_bytes(digest[:2], "big") % dim
            sign = 1.0 if digest[2] % 2 == 0 else -1.0
            vector[index] += sign

        norm = math.sqrt(sum(value * value for value in vector))
        if norm > 0:
            vector = [value / norm for value in vector]
        return vector
