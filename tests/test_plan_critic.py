from agents.plan_critic import PlanCriticAgent
from config import load_config
from models.plan import Plan, PlanPhase, PlanTask
from models.project import TaskDocument
from runtime.deep_agent_factory import DeepAgentFactory


def test_plan_with_empty_acceptance_criteria_gets_flagged(monkeypatch):
    monkeypatch.setenv("DEEP_AGENT_MOCK_MODE", "true")
    critic = PlanCriticAgent(DeepAgentFactory(load_config().deep_agent))
    plan = Plan(
        project_name="demo",
        summary="demo",
        phases=[
            PlanPhase(
                name="Phase 1",
                objective="demo",
                tasks=[
                    PlanTask(
                        task=TaskDocument(
                            task_id="t-empty",
                            title="Implement",
                            description="Do implementation",
                            phase="Phase 1",
                            acceptance_criteria=[],
                        )
                    )
                ],
            )
        ],
    )

    critiques = critic.review(plan)
    codes = {critique.code for critique in critiques}

    assert "empty_acceptance_criteria" in codes


def test_plan_without_verification_task_gets_critique(monkeypatch):
    monkeypatch.setenv("DEEP_AGENT_MOCK_MODE", "true")
    critic = PlanCriticAgent(DeepAgentFactory(load_config().deep_agent))
    plan = Plan(
        project_name="demo",
        summary="demo",
        phases=[
            PlanPhase(
                name="Phase 1",
                objective="demo",
                tasks=[
                    PlanTask(
                        task=TaskDocument(
                            task_id="criterion-build",
                            title="Acceptance criterion 1",
                            description="Implement feature",
                            phase="Phase 1",
                            acceptance_criteria=["feature implemented"],
                        )
                    )
                ],
            )
        ],
    )

    critiques = critic.review(plan)
    codes = {critique.code for critique in critiques}

    assert "missing_verification_task" in codes


def test_plan_without_research_task_gets_critique(monkeypatch):
    monkeypatch.setenv("DEEP_AGENT_MOCK_MODE", "true")
    critic = PlanCriticAgent(DeepAgentFactory(load_config().deep_agent))
    plan = Plan(
        project_name="demo",
        summary="demo",
        phases=[
            PlanPhase(
                name="Phase 1",
                objective="Build",
                tasks=[
                    PlanTask(
                        task=TaskDocument(
                            task_id="criterion-build",
                            title="Acceptance criterion 1",
                            description="Implement feature",
                            phase="Phase 1",
                            acceptance_criteria=["feature implemented"],
                        )
                    )
                ],
            )
        ],
    )

    critiques = critic.review(plan)
    codes = {critique.code for critique in critiques}

    assert "missing_research_task" in codes


def test_out_of_order_phases_get_phase_ordering_critique(monkeypatch):
    monkeypatch.setenv("DEEP_AGENT_MOCK_MODE", "true")
    critic = PlanCriticAgent(DeepAgentFactory(load_config().deep_agent))
    plan = Plan(
        project_name="demo",
        summary="demo",
        phases=[
            PlanPhase(name="Phase 2", objective="Build", tasks=[]),
            PlanPhase(name="Phase 1", objective="Research", tasks=[]),
        ],
    )

    critiques = critic.review(plan)
    codes = {critique.code for critique in critiques}

    assert "phase_ordering_issue" in codes
