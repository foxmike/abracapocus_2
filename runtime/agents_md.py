"""Helpers for loading and summarizing root AGENTS.md guidance."""
from __future__ import annotations

import hashlib
from pathlib import Path


def load_root_agents_md(root_dir: Path) -> tuple[str, dict]:
    """Load AGENTS.md from repo root and return content plus concise metadata."""

    agents_path = root_dir / "AGENTS.md"
    if not agents_path.exists():
        return "", {
            "loaded": False,
            "path": str(agents_path),
            "rule_count": 0,
            "sha256_12": None,
        }
    content = agents_path.read_text(encoding="utf-8")
    normalized_lines = [line.strip() for line in content.splitlines() if line.strip()]
    bullet_lines = [line for line in normalized_lines if line.startswith("-")]
    digest = hashlib.sha256(content.encode("utf-8")).hexdigest()[:12]
    metadata = {
        "loaded": True,
        "path": str(agents_path),
        "rule_count": len(bullet_lines),
        "sha256_12": digest,
    }
    return content, metadata


def compose_agents_backend_notes(agents_md: str, max_lines: int = 20) -> str:
    """Create a concise backend-facing AGENTS guidance block."""

    if not agents_md.strip():
        return ""
    lines = [line.rstrip() for line in agents_md.splitlines() if line.strip()]
    excerpt = lines[:max_lines]
    if len(lines) > max_lines:
        excerpt.append("...(truncated)")
    return "AGENTS.md guidance:\n" + "\n".join(excerpt)
