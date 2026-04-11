"""Self-check script used by demo verification."""
from __future__ import annotations

import sys
from pathlib import Path


def main() -> None:
    status_path = Path("docs/demo_status.md")
    if not status_path.exists():
        sys.stderr.write("docs/demo_status.md is missing\n")
        raise SystemExit(1)
    content = status_path.read_text(encoding="utf-8")
    required_tokens = ["Demo Self-Improvement Log", "Task ID:", "Title:", "Goal:"]
    missing = [token for token in required_tokens if token not in content]
    if missing:
        sys.stderr.write(f"demo_status missing tokens: {', '.join(missing)}\n")
        raise SystemExit(1)
    sys.stdout.write("demo selfcheck passed\n")


if __name__ == "__main__":
    main()
