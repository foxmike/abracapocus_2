from backends.gemini_cli import GeminiCliBackend
from models.project import ContextPackage, TaskDocument


def _sample_task() -> TaskDocument:
    return TaskDocument(
        task_id="task-gemini-1",
        title="Implement feature",
        description="Do something real",
        phase="phase_7",
    )


def _sample_context() -> ContextPackage:
    return ContextPackage(summaries=["s"], files=["main.py"], notes="context")


def test_gemini_backend_uses_non_interactive_flags(tmp_path):
    backend = GeminiCliBackend(working_root=tmp_path)
    command = backend.build_command(_sample_task(), _sample_context())

    assert "--prompt" in command
    assert "--output-format" in command
    output_index = command.index("--output-format")
    assert command[output_index + 1] == "json"
    assert "--approval-mode" in command
    approval_index = command.index("--approval-mode")
    assert command[approval_index + 1] == "yolo"
    assert "--yolo" in command


def test_gemini_backend_includes_workdir_as_context(tmp_path):
    backend = GeminiCliBackend(working_root=tmp_path)
    command = backend.build_command(_sample_task(), _sample_context())

    include_index = command.index("--include-directories")
    assert command[include_index + 1] == str(tmp_path)


def test_gemini_backend_applies_model_when_provided(tmp_path):
    backend = GeminiCliBackend(working_root=tmp_path)
    command = backend.build_command(_sample_task(), _sample_context(), model="gemini-2.5-pro")

    assert "--model" in command
    model_index = command.index("--model")
    assert command[model_index + 1] == "gemini-2.5-pro"
