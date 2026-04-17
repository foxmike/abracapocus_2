from pathlib import Path

from agents.management_agent import ManagementAgent
from agents.planning_agent import PlanningAgent
from config import load_config
from models.project import ProjectRequest
from runtime.deep_agent_factory import DeepAgentFactory
from runtime.state_store import StateStore


def test_single_criterion_creates_single_phase(monkeypatch):
    monkeypatch.setenv("DEEP_AGENT_MOCK_MODE", "true")
    planning = PlanningAgent(DeepAgentFactory(load_config().deep_agent))
    request = ProjectRequest(
        project_name="demo",
        goal="Fix typo",
        constraints=["Typos removed from README"],
    )

    plan = planning.create_plan(request)
    tasks = [phase_task.task for phase in plan.phases for phase_task in phase.tasks]
    criterion_tasks = [task for task in tasks if task.task_id.startswith("criterion-")]

    assert len(plan.phases) == 1
    assert len(criterion_tasks) == 1
    assert any(task.task_id == "plan-verification-gate" for task in tasks)
    assert all(task.selected_backend for task in tasks)


def test_five_criteria_creates_five_tasks_across_phases(monkeypatch):
    monkeypatch.setenv("DEEP_AGENT_MOCK_MODE", "true")
    planning = PlanningAgent(DeepAgentFactory(load_config().deep_agent))
    request = ProjectRequest(
        project_name="demo",
        goal="Ship integration update",
        constraints=[
            "A",
            "B",
            "C",
            "D",
            "E",
        ],
    )

    plan = planning.create_plan(request)
    tasks = [phase_task.task for phase in plan.phases for phase_task in phase.tasks]
    criterion_tasks = [task for task in tasks if task.task_id.startswith("criterion-")]
    phases_with_tasks = [phase for phase in plan.phases if phase.tasks]

    assert len(plan.phases) >= 5
    assert len(criterion_tasks) >= 5
    assert len(phases_with_tasks) >= 5
    assert all(task.selected_backend for task in tasks)


def test_each_task_uses_backend_from_its_complexity_score(monkeypatch):
    monkeypatch.setenv("DEEP_AGENT_MOCK_MODE", "true")
    planning = PlanningAgent(DeepAgentFactory(load_config().deep_agent))
    request = ProjectRequest(
        project_name="demo",
        goal="Deliver mixed scope",
        constraints=[
            "Design rollout milestones",
            "Implement execution wiring",
        ],
    )

    plan = planning.create_plan(request)
    tasks = [phase_task.task for phase in plan.phases for phase_task in phase.tasks]
    criterion_tasks = [task for task in tasks if task.task_id.startswith("criterion-")]

    assert criterion_tasks[0].selected_backend == "claude_code_cli"
    assert criterion_tasks[1].selected_backend == "gemini_cli"
    assert criterion_tasks[0].model == "claude-code"
    assert criterion_tasks[1].model == "gemini"


def test_three_criteria_create_three_tasks_across_phases(monkeypatch):
    monkeypatch.setenv("DEEP_AGENT_MOCK_MODE", "true")
    planning = PlanningAgent(DeepAgentFactory(load_config().deep_agent))
    request = ProjectRequest(
        project_name="demo",
        goal="Ship planning update",
        constraints=["First criterion", "Second criterion", "Third criterion"],
    )

    plan = planning.create_plan(request)
    tasks = [phase_task.task for phase in plan.phases for phase_task in phase.tasks]
    criterion_tasks = [task for task in tasks if task.task_id.startswith("criterion-")]
    task_phases = {task.phase for task in tasks}

    assert len(criterion_tasks) == 3
    assert len(task_phases) == 3


def test_task_id_slugs_are_unique_and_deterministic(monkeypatch):
    monkeypatch.setenv("DEEP_AGENT_MOCK_MODE", "true")
    planning = PlanningAgent(DeepAgentFactory(load_config().deep_agent))
    request = ProjectRequest(
        project_name="demo",
        goal="Decompose criteria",
        constraints=["Alpha criterion", "Beta criterion", "Alpha criterion"],
    )

    plan_a = planning.create_plan(request)
    plan_b = planning.create_plan(request)
    tasks_a = [phase_task.task for phase in plan_a.phases for phase_task in phase.tasks]
    tasks_b = [phase_task.task for phase in plan_b.phases for phase_task in phase.tasks]
    ids_a = [task.task_id for task in tasks_a if task.task_id.startswith("criterion-")]
    ids_b = [task.task_id for task in tasks_b if task.task_id.startswith("criterion-")]

    assert ids_a == ids_b
    assert len(ids_a) == len(set(ids_a))


def test_no_duplicate_tasks_generated_for_duplicate_criteria(monkeypatch):
    monkeypatch.setenv("DEEP_AGENT_MOCK_MODE", "true")
    planning = PlanningAgent(DeepAgentFactory(load_config().deep_agent))
    request = ProjectRequest(
        project_name="demo",
        goal="Deduplicate criteria",
        constraints=["Same criterion", "Same criterion", "Different criterion"],
    )

    plan = planning.create_plan(request)
    tasks = [phase_task.task for phase in plan.phases for phase_task in phase.tasks]
    criterion_tasks = [task for task in tasks if task.task_id.startswith("criterion-")]
    descriptions = [task.description for task in criterion_tasks]

    assert len(criterion_tasks) == 2
    assert descriptions.count("Same criterion") == 1


def test_phase_assignment_uses_index_and_complexity(monkeypatch):
    monkeypatch.setenv("DEEP_AGENT_MOCK_MODE", "true")
    planning = PlanningAgent(DeepAgentFactory(load_config().deep_agent))
    request = ProjectRequest(
        project_name="demo",
        goal="Ship secure rollout",
        constraints=["Add auth token migration", "Update docs"],
    )

    plan = planning.create_plan(request)
    tasks = [phase_task.task for phase in plan.phases for phase_task in phase.tasks]
    criterion_tasks = [task for task in tasks if task.task_id.startswith("criterion-")]
    phase_by_description = {task.description: task.phase for task in criterion_tasks}

    assert phase_by_description["Add auth token migration"] == "Phase 5"
    assert phase_by_description["Update docs"] == "Phase 2"


def test_plan_persists_to_plans_directory(monkeypatch, tmp_path):
    monkeypatch.setenv("DEEP_AGENT_MOCK_MODE", "true")
    config = _tmp_config(tmp_path)
    factory = DeepAgentFactory(config.deep_agent)
    planning = PlanningAgent(factory)
    manager = ManagementAgent(factory, StateStore(config))
    request = ProjectRequest(
        project_name="demo",
        goal="Design release plan",
        constraints=["Design implementation milestones"],
    )

    plan = planning.create_plan(request)
    original_cwd = Path.cwd()
    try:
        monkeypatch.chdir(tmp_path)
        manager.register_plan(plan)
    finally:
        monkeypatch.chdir(original_cwd)

    path = tmp_path / "plans" / f"{plan.version}.json"
    assert path.exists()
    content = path.read_text(encoding="utf-8")
    assert "missing_verification_task" in {critique.code for critique in planning.last_critiques}
    assert "plan-verification-gate" in content


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
