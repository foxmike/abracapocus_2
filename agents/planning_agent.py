"""Planning agent implementation."""
from __future__ import annotations

from datetime import datetime
from typing import List

from agents.base import BaseAgent
from models.plan import Plan, PlanPhase, PlanTask
from models.project import ProjectRequest, TaskDocument
from runtime.deep_agent_factory import DeepAgentFactory


class PlanningAgent(BaseAgent):
    def __init__(self, factory: DeepAgentFactory) -> None:
        super().__init__(
            name="planning_agent",
            prompt_file="prompts/planning.md",
            skills=["skills/planning", "skills/phase_progression"],
            factory=factory,
        )

    def create_plan(self, request: ProjectRequest) -> Plan:
        _ = self.invoke({"goal": request.goal, "constraints": request.constraints})
        base_tasks = self._seed_tasks(request)
        phases: List[PlanPhase] = [
            PlanPhase(
                name="Phase 1: Research",
                objective="Collect repo intelligence and constraints",
                tasks=[PlanTask(task=base_tasks[0])],
            ),
            PlanPhase(
                name="Phase 2: Implementation",
                objective="Execute coding work via CLI backend",
                tasks=[PlanTask(task=base_tasks[1])],
            ),
            PlanPhase(
                name="Phase 3: Verification",
                objective="Stabilize, verify, and prepare handoff",
                tasks=[PlanTask(task=base_tasks[2])],
            ),
        ]
        return Plan(
            project_name=request.project_name,
            summary=f"Plan for {request.goal}",
            phases=phases,
            version=f"v{datetime.utcnow().strftime('%Y%m%d')}",
        )

    def _seed_tasks(self, request: ProjectRequest) -> List[TaskDocument]:
        goal_slug = request.goal.lower().replace(" ", "-")[:20]
        return [
            TaskDocument(
                task_id=f"research-{goal_slug}",
                title="Research existing assets",
                description="Summarize repository and docs for downstream agents",
                phase="research",
                acceptance_criteria=["Key directories cataloged", "Constraints captured"],
            ),
            TaskDocument(
                task_id=f"build-{goal_slug}",
                title="Execute coding work",
                description=request.goal,
                phase="implementation",
                acceptance_criteria=["Implements goal description"],
            ),
            TaskDocument(
                task_id=f"verify-{goal_slug}",
                title="Verify and document",
                description="Run deterministic verification and document changes",
                phase="verification",
                acceptance_criteria=["Verification run recorded", "Reports stored"],
            ),
        ]
