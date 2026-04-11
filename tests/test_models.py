from models.plan import Plan, PlanPhase, PlanTask
from models.project import ProjectRequest, TaskDocument


def test_plan_and_task_models():
    request = ProjectRequest(project_name="demo", goal="Ship feature")
    task = TaskDocument(task_id="t1", title="Do work", description="desc", phase="alpha")
    plan = Plan(
        project_name=request.project_name,
        summary="demo",
        phases=[PlanPhase(name="alpha", objective="o", tasks=[PlanTask(task=task)])],
    )
    assert plan.phases[0].tasks[0].task.title == "Do work"
