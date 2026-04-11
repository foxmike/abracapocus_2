from agents.verifier_agent import VerifierAgent
from config import load_config
from models.project import TaskDocument
from models.reports import BackendExecution
from runtime.deep_agent_factory import DeepAgentFactory


def test_verifier_runs_compile():
    config = load_config()
    factory = DeepAgentFactory(config.deep_agent)
    agent = VerifierAgent(factory)
    task = TaskDocument(task_id="verify", title="Verify", description="", phase="verification")
    execution = BackendExecution(
        backend="codex_cli",
        command=["echo"],
        stdout="done",
        stderr="",
        exit_code=0,
        duration_seconds=0.1,
    )
    report = agent.verify(task, execution)
    assert report.status in {"passed", "failed"}
    assert report.checks
