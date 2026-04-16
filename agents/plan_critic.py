"""Plan critic agent for two-pass planning review."""
from __future__ import annotations

from dataclasses import dataclass
from typing import List

from agents.base import BaseAgent
from models.plan import Plan
from runtime.deep_agent_factory import DeepAgentFactory


@dataclass(slots=True)
class PlanCritique:
    code: str
    severity: str
    detail: str
    location: str


class PlanCriticAgent(BaseAgent):
    def __init__(self, factory: DeepAgentFactory) -> None:
        super().__init__(
            name="plan_critic_agent",
            prompt_file="prompts/plan_critic.md",
            skills=["skills/planning", "skills/phase_progression"],
            factory=factory,
        )

    def review(self, plan: Plan) -> List[PlanCritique]:
        _ = self.invoke({"phase_count": len(plan.phases), "summary": plan.summary})
        critiques: List[PlanCritique] = []
        if not self._has_verification_task(plan):
            critiques.append(
                PlanCritique(
                    code="missing_verification_task",
                    severity="high",
                    detail="Plan does not include a verification task.",
                    location="plan",
                )
            )
        if not self._has_research_task(plan):
            critiques.append(
                PlanCritique(
                    code="missing_research_task",
                    severity="medium",
                    detail="Plan does not include a research task.",
                    location="plan",
                )
            )
        for phase in plan.phases:
            for plan_task in phase.tasks:
                if not plan_task.task.acceptance_criteria:
                    critiques.append(
                        PlanCritique(
                            code="empty_acceptance_criteria",
                            severity="high",
                            detail="Task has no acceptance criteria.",
                            location=plan_task.task.task_id,
                        )
                    )
        if not self._phases_ordered(plan):
            critiques.append(
                PlanCritique(
                    code="phase_ordering_issue",
                    severity="medium",
                    detail="Plan phases are not ordered.",
                    location="plan",
                )
            )
        return critiques

    def _has_verification_task(self, plan: Plan) -> bool:
        for phase in plan.phases:
            if "verif" in phase.name.lower():
                return True
            for plan_task in phase.tasks:
                descriptor = (
                    f"{plan_task.task.title} {plan_task.task.description} {plan_task.task.phase}"
                ).lower()
                if "verif" in descriptor or "review" in descriptor or "qa" in descriptor:
                    return True
        return False

    def _has_research_task(self, plan: Plan) -> bool:
        for phase in plan.phases:
            if "research" in phase.name.lower():
                return True
            for plan_task in phase.tasks:
                descriptor = (
                    f"{plan_task.task.title} {plan_task.task.description} {plan_task.task.phase}"
                ).lower()
                if "research" in descriptor or "investigate" in descriptor:
                    return True
        return False

    def _phases_ordered(self, plan: Plan) -> bool:
        numbered = []
        for phase in plan.phases:
            parts = phase.name.split()
            if len(parts) >= 2 and parts[0].lower() == "phase" and parts[1].isdigit():
                numbered.append(int(parts[1]))
        return numbered == sorted(numbered)

