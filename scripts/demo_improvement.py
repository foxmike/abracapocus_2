"""Deterministic demo self-improvement script."""
from __future__ import annotations

import argparse
from datetime import datetime
from pathlib import Path


def build_entry(task_id: str, title: str, description: str, phase: str, context: str) -> str:
    timestamp = datetime.utcnow().isoformat(timespec="seconds")
    lines = [
        f"## Run {timestamp}",
        f"- Task ID: {task_id}",
        f"- Title: {title}",
        f"- Phase: {phase or 'n/a'}",
        f"- Goal: {description or 'n/a'}",
    ]
    if context:
        lines.append(f"- Context: {context}")
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="Demo self-improvement writer")
    parser.add_argument("--task-id", required=True)
    parser.add_argument("--title", required=True)
    parser.add_argument("--description", default="")
    parser.add_argument("--phase", default="")
    parser.add_argument("--context-notes", default="")
    args = parser.parse_args()

    status_path = Path("docs/demo_status.md")
    status_path.parent.mkdir(parents=True, exist_ok=True)
    header = "# Demo Self-Improvement Log\n\nThis file is updated automatically when `python main.py demo` runs.\n\n"
    if status_path.exists():
        content = status_path.read_text(encoding="utf-8")
        if not content.startswith("# Demo Self-Improvement Log"):
            content = header + content
    else:
        content = header
    entry = build_entry(args.task_id, args.title, args.description, args.phase, args.context_notes)
    status_path.write_text(content + entry, encoding="utf-8")
    print(f"Updated {status_path} with new entry at {datetime.utcnow().isoformat(timespec='seconds')}")


if __name__ == "__main__":
    main()
