from pathlib import Path

from backends.aider_cli import AiderCliBackend
from models.project import ContextPackage, TaskDocument


def _sample_task() -> TaskDocument:
    return TaskDocument(
        task_id="task-aider-1",
        title="Implement feature",
        description="Do something real",
        phase="phase_0",
    )


def _sample_context() -> ContextPackage:
    return ContextPackage(summaries=["s"], files=["main.py"], notes="context")


def test_aider_backend_always_includes_root_flag(tmp_path):
    backend = AiderCliBackend(working_root=tmp_path)
    command = backend.build_command(_sample_task(), _sample_context())

    assert "--root" in command


def test_aider_backend_root_matches_workdir(tmp_path):
    backend = AiderCliBackend(working_root=tmp_path)
    backend.workdir = Path(tmp_path) / "nested"
    command = backend.build_command(_sample_task(), _sample_context())

    root_index = command.index("--root")
    assert command[root_index + 1] == str(backend.workdir)

