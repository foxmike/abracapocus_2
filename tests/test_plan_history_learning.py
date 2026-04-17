import json
from pathlib import Path

from agents.management_agent import ManagementAgent
from agents.planning_agent import PlanningAgent
from config import load_config
from models.plan import Plan, PlanPhase, PlanTask
from models.project import ProjectRequest, TaskDocument
from orchestrator.supervisor import SupervisorOrchestrator
from runtime.deep_agent_factory import DeepAgentFactory
from runtime.state_store import StateStore


def test_successful_run_writes_plan_template_history(monkeypatch, tmp_path):
    monkeypatch.setenv("DEEP_AGENT_MOCK_MODE", "true")
    monkeypatch.setenv("ABRACAPOCUS_ALLOW_MAIN", "true")
    config = _tmp_config(tmp_path)
    orchestrator = SupervisorOrchestrator(config)
    task = TaskDocument(
        task_id="history-task",
        title="History Task",
        description="Verify history persistence",
        phase="implementation",
        selected_backend="aider_cli",
        verification_profile="minimal",
    )
    request = ProjectRequest(project_name=config.project_name, goal=task.description, context="history")

    report = orchestrator.run(request, task=task)

    history_path = config.paths.state_file.parent / "plan_history.json"
    assert report.verification.status == "passed"
    assert history_path.exists()
    entries = json.loads(history_path.read_text(encoding="utf-8"))
    assert entries
    assert entries[-1]["project_name"] == config.project_name
    assert entries[-1]["goal"] == task.description


def test_second_run_loads_similar_plan_examples(monkeypatch, tmp_path):
    monkeypatch.setenv("DEEP_AGENT_MOCK_MODE", "true")
    config = _tmp_config(tmp_path)
    factory = DeepAgentFactory(config.deep_agent)
    state_store = StateStore(config)
    manager = ManagementAgent(factory, state_store)
    history_path = config.paths.state_file.parent / "plan_history.json"

    base_plan = _sample_plan(project_name=config.project_name)
    manager.store_successful_plan_template(base_plan, "secure auth rollout")

    planner = PlanningAgent(factory, history_path=history_path)
    planner.create_plan(
        ProjectRequest(
            project_name=config.project_name,
            goal="auth rollout verification",
            constraints=["Add auth checks"],
        )
    )

    assert planner.last_historical_examples
    assert planner.last_historical_examples[0]["project_name"] == config.project_name


def test_plan_history_capped_to_twenty_entries(monkeypatch, tmp_path):
    monkeypatch.setenv("DEEP_AGENT_MOCK_MODE", "true")
    config = _tmp_config(tmp_path)
    factory = DeepAgentFactory(config.deep_agent)
    manager = ManagementAgent(factory, StateStore(config))
    history_path = config.paths.state_file.parent / "plan_history.json"

    for index in range(25):
        manager.store_successful_plan_template(
            _sample_plan(project_name=config.project_name),
            goal=f"goal-{index}",
        )

    entries = json.loads(history_path.read_text(encoding="utf-8"))
    goals = [entry["goal"] for entry in entries]
    assert len(entries) == 20
    assert "goal-0" not in goals
    assert goals[-1] == "goal-24"


def _sample_plan(project_name: str) -> Plan:
    task = TaskDocument(
        task_id="t1",
        title="Task",
        description="desc",
        phase="Phase 1",
        acceptance_criteria=["ok"],
    )
    return Plan(
        project_name=project_name,
        summary="sample",
        phases=[PlanPhase(name="Phase 1", objective="obj", tasks=[PlanTask(task=task)])],
        version="vtest",
    )


def _tmp_config(tmp_path: Path):
    config = load_config()
    paths = config.paths.model_copy(
        update={
            "working_root": tmp_path,
            "logs_dir": tmp_path / "logs",
            "reports_dir": tmp_path / "reports",
            "plans_dir": tmp_path / "plans",
            "tasks_dir": tmp_path / "tasks",
            "phases_dir": tmp_path / "phases",
            "state_file": tmp_path / "state" / "runtime_state.json",
        }
    )
    paths.logs_dir.mkdir(parents=True, exist_ok=True)
    paths.reports_dir.mkdir(parents=True, exist_ok=True)
    paths.plans_dir.mkdir(parents=True, exist_ok=True)
    paths.tasks_dir.mkdir(parents=True, exist_ok=True)
    paths.phases_dir.mkdir(parents=True, exist_ok=True)
    paths.state_file.parent.mkdir(parents=True, exist_ok=True)
    config.paths = paths
    return config
