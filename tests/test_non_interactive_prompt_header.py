from pathlib import Path

from backends.aider_cli import AiderCliBackend
from backends.claude_code_cli import ClaudeCodeCliBackend
from backends.codex_cli import CodexCliBackend
from backends.demo_cli import DemoCliBackend
from backends.gemini_cli import GeminiCliBackend


def test_backend_prompts_prepend_non_interactive_header(tmp_path) -> None:
    header = Path("prompts/shared/non_interactive_header.md").read_text(encoding="utf-8").strip()
    backends = [
        CodexCliBackend(working_root=tmp_path),
        AiderCliBackend(working_root=tmp_path),
        GeminiCliBackend(working_root=tmp_path),
        ClaudeCodeCliBackend(working_root=tmp_path),
        DemoCliBackend(working_root=tmp_path),
    ]

    for backend in backends:
        assert backend.prompt.startswith(header)
        assert "non-interactively" in backend.prompt
