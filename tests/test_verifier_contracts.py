from types import SimpleNamespace

from agents.verifier_agent import VerifierAgent
from config import load_config
from models.project import TaskDocument
from models.reports import BackendExecution
from runtime.deep_agent_factory import DeepAgentFactory


def test_verifier_runs_profile(monkeypatch):
    config = load_config()
    factory = DeepAgentFactory(config.deep_agent)
    agent = VerifierAgent(factory, config.verification)
    calls = []

    def fake_run(command, capture_output, text, check, cwd):
        calls.append((tuple(command), cwd))
        return SimpleNamespace(stdout="ok", stderr="", returncode=0)

    monkeypatch.setattr("agents.verifier_agent.subprocess.run", fake_run)
    task = TaskDocument(task_id="verify", title="Verify", description="", phase="verification")
    execution = BackendExecution(
        backend="codex_cli",
        command=["echo"],
        stdout="done",
        stderr="",
        exit_code=0,
        duration_seconds=0.1,
        working_directory=".",
    )
    report = agent.verify(task, execution)
    assert report.status == "passed"
    assert report.profile == config.verification.active_profile
    assert len(report.checks) == len(config.verification.active_checks())
    assert all(check.command for check in report.checks)
    assert calls


def test_verifier_collects_failures(monkeypatch):
    config = load_config()
    factory = DeepAgentFactory(config.deep_agent)
    agent = VerifierAgent(factory, config.verification)

    def fake_run(command, capture_output, text, check, cwd):
        return SimpleNamespace(stdout="", stderr="boom", returncode=1)

    monkeypatch.setattr("agents.verifier_agent.subprocess.run", fake_run)
    task = TaskDocument(task_id="verify", title="Verify", description="", phase="verification")
    execution = BackendExecution(
        backend="codex_cli",
        command=["echo"],
        stdout="done",
        stderr="",
        exit_code=0,
        duration_seconds=0.1,
        working_directory=".",
    )
    report = agent.verify(task, execution)
    assert report.status == "failed"
    assert report.profile == config.verification.active_profile
    assert all(check.status == "failed" for check in report.checks)


def test_verifier_task_profile_override(monkeypatch):
    config = load_config()
    factory = DeepAgentFactory(config.deep_agent)
    agent = VerifierAgent(factory, config.verification)

    def fake_run(command, capture_output, text, check, cwd):
        return SimpleNamespace(stdout="ok", stderr="", returncode=0)

    monkeypatch.setattr("agents.verifier_agent.subprocess.run", fake_run)
    task = TaskDocument(
        task_id="verify",
        title="Verify",
        description="",
        phase="verification",
        verification_profile="minimal",
    )
    execution = BackendExecution(
        backend="codex_cli",
        command=["echo"],
        stdout="done",
        stderr="",
        exit_code=0,
        duration_seconds=0.1,
        working_directory=".",
    )
    report = agent.verify(task, execution)
    assert report.profile == "minimal"
    assert len(report.checks) == len(config.verification.active_checks("minimal"))


def test_verifier_invalid_profile(monkeypatch):
    config = load_config()
    factory = DeepAgentFactory(config.deep_agent)
    agent = VerifierAgent(factory, config.verification)

    def fake_run(command, capture_output, text, check, cwd):
        return SimpleNamespace(stdout="ok", stderr="", returncode=0)

    monkeypatch.setattr("agents.verifier_agent.subprocess.run", fake_run)
    task = TaskDocument(
        task_id="verify",
        title="Verify",
        description="",
        phase="verification",
        verification_profile="does-not-exist",
    )
    execution = BackendExecution(
        backend="codex_cli",
        command=["echo"],
        stdout="done",
        stderr="",
        exit_code=0,
        duration_seconds=0.1,
        working_directory=".",
    )
    report = agent.verify(task, execution)
    assert report.profile == config.verification.active_profile
