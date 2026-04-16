import shutil
from pathlib import Path

from runtime.context_store import ContextStore


def _write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def _repo_dir(name: str) -> Path:
    path = Path.cwd() / "state" / "test_context_store" / name
    if path.exists():
        shutil.rmtree(path)
    path.mkdir(parents=True, exist_ok=True)
    return path


def _docs_for_path(store: ContextStore, rel_path: str) -> list[str]:
    data = store.collection.get(where={"path": rel_path}, include=["documents"])
    return data.get("documents") or []


def test_index_repo_indexes_eligible_files_and_persists_state():
    tmp_path = _repo_dir("index_repo")
    _write(tmp_path / "app.py", "def run():\n    return 'run'\n")
    _write(tmp_path / "README.md", "Project overview\n\nDetails")
    _write(tmp_path / "docs" / "guide.md", "Guide section")
    _write(tmp_path / ".venv" / "skip.py", "def skip():\n    pass\n")
    _write(tmp_path / "__pycache__" / "cache.py", "def cache():\n    pass\n")
    _write(tmp_path / "node_modules" / "pkg.py", "def pkg():\n    pass\n")
    _write(tmp_path / ".git" / "hooks.md", "hidden")
    _write(tmp_path / "ignored.pyc", "binary")
    _write(tmp_path / "notes.txt", "not indexed")

    store = ContextStore()
    store.index_repo(tmp_path)

    all_data = store.collection.get(include=["metadatas"])
    indexed_paths = {metadata["path"] for metadata in all_data.get("metadatas") or []}
    assert indexed_paths == {"app.py", "README.md", "docs/guide.md"}

    chroma_dir = tmp_path / "state" / "chroma"
    assert chroma_dir.exists()
    assert any(chroma_dir.iterdir())


def test_query_returns_relevant_chunks_with_paths():
    tmp_path = _repo_dir("query")
    _write(
        tmp_path / "app.py",
        "def run_quantum_turnip():\n"
        "    return 'quantum_turnip keeps retrieval deterministic'\n",
    )
    _write(tmp_path / "README.md", "This paragraph is unrelated to the app implementation.")

    store = ContextStore()
    store.index_repo(tmp_path)

    matches = store.query("quantum_turnip", k=2)
    assert matches
    assert len(matches) <= 2
    assert all({"path", "chunk", "distance"}.issubset(match.keys()) for match in matches)
    assert any(match["path"] == "app.py" and "quantum_turnip" in str(match["chunk"]) for match in matches)


def test_update_files_reindexes_only_provided_paths():
    tmp_path = _repo_dir("update_files")
    app_path = tmp_path / "app.py"
    deleted_path = tmp_path / "delete_me.md"
    _write(app_path, "def feature():\n    return 'old_token'\n")
    _write(tmp_path / "notes.md", "stable_token lives here")
    _write(deleted_path, "remove_token")

    store = ContextStore()
    store.index_repo(tmp_path)

    _write(app_path, "def feature():\n    return 'new_token'\n")
    deleted_path.unlink()

    store.update_files(["app.py", "delete_me.md"])

    app_docs = "\n".join(_docs_for_path(store, "app.py"))
    notes_docs = "\n".join(_docs_for_path(store, "notes.md"))
    deleted_docs = _docs_for_path(store, "delete_me.md")

    assert "new_token" in app_docs
    assert "old_token" not in app_docs
    assert "stable_token" in notes_docs
    assert deleted_docs == []


def test_query_always_includes_hint_files_from_context_file():
    tmp_path = _repo_dir("query_hints")
    _write(
        tmp_path / "app.py",
        "def run_quantum_turnip():\n"
        "    return 'quantum_turnip keeps retrieval deterministic'\n",
    )
    _write(tmp_path / "README.md", "This should always be included via hints.")
    _write(tmp_path / "docs" / "guide.md", "Guide should be included by glob hint.")
    _write(
        tmp_path / ".abracapocus_context",
        "# include files for every query\n"
        "README.md   # inline comment should be ignored\n"
        "docs/*.md\n"
        "missing.md\n",
    )

    store = ContextStore()
    store.index_repo(tmp_path)

    matches = store.query("quantum_turnip", k=1)
    matched_paths = {match["path"] for match in matches}

    assert "app.py" in matched_paths
    assert "README.md" in matched_paths
    assert "docs/guide.md" in matched_paths
    assert "missing.md" not in matched_paths


def test_query_silently_ignores_missing_hint_file():
    tmp_path = _repo_dir("query_missing_hint")
    _write(tmp_path / "app.py", "def run():\n    return 'present_token'\n")
    _write(tmp_path / ".abracapocus_context", "missing.md\n")

    store = ContextStore()
    store.index_repo(tmp_path)

    matches = store.query("present_token", k=1)

    assert matches
    assert all(match["path"] != "missing.md" for match in matches)
