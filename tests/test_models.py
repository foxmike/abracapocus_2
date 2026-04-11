from models.plan import Plan, PlanPhase, PlanRecord, PlanTask
from models.project import ProjectRequest, TaskDocument


def test_plan_and_task_models():
    request = ProjectRequest(project_name="demo", goal="Ship feature")
    task = TaskDocument(
        task_id="t1",
        title="Do work",
        description="desc",
        phase="alpha",
        acceptance_criteria=["ship it"],
        selected_backend="codex_cli",
        verification_profile="default",
    )
    phase = PlanPhase(name="alpha", objective="o", tasks=[PlanTask(task=task)])
    plan = Plan(
        project_name=request.project_name,
        summary="demo",
        phases=[phase],
    )
    stored_task = plan.phases[0].tasks[0].task
    assert stored_task.title == "Do work"
    assert stored_task.selected_backend == "codex_cli"
    assert stored_task.verification_profile == "default"


def test_plan_record_completed():
    task = TaskDocument(task_id="t2", title="Research", description="desc", phase="research")
    completed_phase = PlanPhase(name="Research", objective="learn", tasks=[PlanTask(task=task)], completed=True)
    remaining_phase = PlanPhase(
        name="Build",
        objective="implement",
        tasks=[PlanTask(task=TaskDocument(task_id="t3", title="Build", description="", phase="impl"))],
    )
    plan = Plan(project_name="demo", summary="sum", phases=[completed_phase, remaining_phase], version="v20240101")
    record = PlanRecord(plan_version=plan.version, completed_phases=[completed_phase], remaining_phases=[remaining_phase])
    assert record.plan_version == "v20240101"
    assert record.completed_phases[0].completed is True
    assert record.remaining_phases[0].name == "Build"
