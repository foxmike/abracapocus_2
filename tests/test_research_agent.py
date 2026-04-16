from pathlib import Path

from agents.research_agent import ResearchAgent
from config import load_config
from models.project import ProjectRequest
from runtime.deep_agent_factory import DeepAgentFactory


def _write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def test_gather_returns_relevant_files_and_skips_excluded_dirs(tmp_path, monkeypatch):
    monkeypatch.setenv("DEEP_AGENT_MOCK_MODE", "true")
    _write(
        tmp_path / "app.py",
        "def run_quantum_turnip():\n"
        "    return 'quantum_turnip retrieval marker'\n",
    )
    _write(tmp_path / ".venv" / "hidden.py", "def hidden():\n    return 'quantum_turnip'\n")
    _write(tmp_path / "__pycache__" / "cache.py", "def cache():\n    return 'quantum_turnip'\n")

    factory = DeepAgentFactory(load_config().deep_agent)
    agent = ResearchAgent(factory, repo_root=tmp_path)
    request = ProjectRequest(project_name="demo", goal="find quantum_turnip")

    context = agent.gather(request)

    assert "app.py" in context.files
    assert all(".venv" not in file_path for file_path in context.files)
    assert all("__pycache__" not in file_path for file_path in context.files)


def test_gather_files_are_real_paths_under_repo_root(tmp_path, monkeypatch):
    monkeypatch.setenv("DEEP_AGENT_MOCK_MODE", "true")
    _write(tmp_path / "README.md", "project context anchor token")

    factory = DeepAgentFactory(load_config().deep_agent)
    agent = ResearchAgent(factory, repo_root=tmp_path)
    request = ProjectRequest(project_name="demo", goal="anchor token")

    context = agent.gather(request)

    assert context.files
    assert all((tmp_path / file_path).exists() for file_path in context.files)
