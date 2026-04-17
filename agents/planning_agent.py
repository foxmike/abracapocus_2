"""Planning agent implementation."""
from __future__ import annotations

from datetime import datetime
import json
from pathlib import Path
import re
from typing import List

from agents.base import BaseAgent
from agents.complexity_classifier import ComplexityClassifier, ComplexityScore
from agents.plan_critic import PlanCriticAgent, PlanCritique
from models.plan import Plan, PlanPhase, PlanTask
from models.project import ProjectRequest, TaskDocument
from runtime.deep_agent_factory import DeepAgentFactory
from runtime.model_profile_store import ModelProfileStore


class PlanningAgent(BaseAgent):
    def __init__(self, factory: DeepAgentFactory, history_path: Path | None = None) -> None:
        super().__init__(
            name="planning_agent",
            prompt_file="prompts/planning.md",
            skills=["skills/planning", "skills/phase_progression"],
            factory=factory,
        )
        self.classifier = ComplexityClassifier()
        self.plan_critic = PlanCriticAgent(factory)
        self.last_critiques: List[PlanCritique] = []
        self.history_path = history_path or Path("state") / "plan_history.json"
        self.last_historical_examples: List[dict] = []
        self.model_profiles = ModelProfileStore()

    def create_plan(self, request: ProjectRequest, previous_plan: Plan | None = None) -> Plan:
        examples = self._load_similar_plan_examples(request.project_name, request.goal)
        self.last_historical_examples = examples
        _ = self.invoke({"goal": request.goal, "constraints": request.constraints, "examples": examples})
        criteria = self._criteria(request)
        context_files = self._context_files(request.context)
        plan_score = self.classifier.classify(
            title=request.goal,
            description=request.goal,
            acceptance_criteria=criteria,
            context_files=context_files,
        )
        task_scores = [
            self.classifier.classify(
                title=criterion,
                description=criterion,
                acceptance_criteria=[criterion],
                context_files=context_files,
            )
            for criterion in criteria
        ]
        phases = self._build_phases(request, criteria, plan_score, task_scores)
        plan = Plan(
            project_name=request.project_name,
            summary=f"Plan for {request.goal}",
            phases=phases,
            version=f"v{datetime.utcnow().strftime('%Y%m%d')}",
        )
        self.last_critiques = self.plan_critic.review(plan)
        if self.last_critiques:
            plan = self._revise_plan(plan, self.last_critiques, context_files)

        if previous_plan:
            for old_phase in previous_plan.phases:
                if old_phase.completed:
                    plan.phases.insert(0, old_phase)
        return plan

    def _criteria(self, request: ProjectRequest) -> List[str]:
        criteria = [criterion.strip() for criterion in request.constraints if criterion.strip()]
        if criteria:
            return criteria
        return [request.goal]

    def _context_files(self, context: str | None) -> List[str]:
        if not context:
            return []
        files: List[str] = []
        for token in re.split(r"[\n,]", context):
            candidate = token.strip()
            if not candidate:
                continue
            if "/" in candidate or "." in candidate:
                files.append(candidate)
        return files

    def _build_phases(
        self,
        request: ProjectRequest,
        criteria: List[str],
        plan_score: ComplexityScore,
        task_scores: List[ComplexityScore],
    ) -> List[PlanPhase]:
        phase_count = max(1, plan_score.recommended_phases)
        phases = [
            PlanPhase(
                name=f"Phase {index + 1}",
                objective=f"Deliver scope={plan_score.scope} work package {index + 1}",
                tasks=[],
            )
            for index in range(phase_count)
        ]

        tasks = self._decompose_from_criteria(criteria, task_scores, phases)
        for task in tasks:
            phase_number = int(task.phase.split(" ")[1])
            phase_index = max(0, min(phase_number - 1, phase_count - 1))
            phases[phase_index].tasks.append(PlanTask(task=task))
        return phases

    def _decompose_from_criteria(
        self,
        criteria: List[str],
        task_scores: List[ComplexityScore],
        phases: List[PlanPhase],
    ) -> List[TaskDocument]:
        tasks: List[TaskDocument] = []
        seen_criteria: set[str] = set()
        slug_counts: dict[str, int] = {}
        phase_count = len(phases)

        for index, criterion in enumerate(criteria):
            normalized_criterion = criterion.strip()
            if not normalized_criterion:
                continue
            if normalized_criterion in seen_criteria:
                continue
            seen_criteria.add(normalized_criterion)

            base_slug = self._slugify(normalized_criterion)
            slug_counts[base_slug] = slug_counts.get(base_slug, 0) + 1
            suffix = f"-{slug_counts[base_slug]}" if slug_counts[base_slug] > 1 else ""
            task_id = f"criterion-{base_slug}{suffix}"

            task_score = task_scores[index]
            phase_index = self._phase_index_for_criterion(
                criterion_index=index,
                task_score=task_score,
                phase_count=phase_count,
            )
            task_type = self._infer_task_type(phases[phase_index].name, normalized_criterion)
            cost_tier, context_size = self._complexity_budget(task_score, normalized_criterion)
            assigned_model = self.model_profiles.get_best_model_for_backend(
                backend_name=task_score.recommended_backend,
                task_type=task_type,
                cost_tier=cost_tier,
                context_size=context_size,
            )
            tasks.append(
                TaskDocument(
                    task_id=task_id,
                    title=f"Acceptance criterion {index + 1}",
                    description=normalized_criterion,
                    phase=phases[phase_index].name,
                    acceptance_criteria=[normalized_criterion],
                    selected_backend=task_score.recommended_backend,
                    model=assigned_model,
                )
            )
        return tasks

    def _infer_task_type(self, phase: str, description: str) -> str:
        phase_lower = (phase or "").lower()
        description_lower = (description or "").lower()
        if "research" in phase_lower or "plan" in phase_lower or "design" in description_lower:
            return "planning"
        if "verify" in phase_lower or "review" in phase_lower or "qa" in description_lower:
            return "review"
        if len(description) < 160:
            return "quick"
        return "coding"

    def _complexity_budget(self, score: ComplexityScore, description: str) -> tuple[str, int]:
        if score.recommended_phases >= 5 or len(description) >= 320:
            return "high", 64000
        if score.recommended_phases >= 3 or len(description) >= 180:
            return "medium", 32000
        return "low", 8000

    def _phase_index_for_criterion(
        self,
        criterion_index: int,
        task_score: ComplexityScore,
        phase_count: int,
    ) -> int:
        if phase_count <= 1:
            return 0
        index_phase = min(criterion_index, phase_count - 1)
        complexity_phase = max(0, min(task_score.recommended_phases - 1, phase_count - 1))
        return max(index_phase, complexity_phase)

    def _slugify(self, value: str) -> str:
        normalized = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
        if not normalized:
            return "task"
        return normalized[:32]

    def _load_similar_plan_examples(self, project_name: str, goal: str) -> List[dict]:
        if not self.history_path.exists():
            return []
        data = json.loads(self.history_path.read_text(encoding="utf-8") or "[]")
        if not isinstance(data, list):
            return []

        goal_tokens = self._goal_tokens(goal)
        ranked: List[tuple[int, int, dict]] = []
        for index, entry in enumerate(data):
            if not isinstance(entry, dict):
                continue
            if entry.get("project_name") != project_name:
                continue
            entry_goal = str(entry.get("goal") or "")
            overlap = len(goal_tokens & self._goal_tokens(entry_goal))
            if overlap <= 0:
                continue
            ranked.append((overlap, index, entry))
        ranked.sort(key=lambda item: (-item[0], -item[1]))
        return [item[2] for item in ranked[:3]]

    def _goal_tokens(self, text: str) -> set[str]:
        return {token for token in re.findall(r"[a-z0-9]+", text.lower()) if len(token) > 2}

    def _revise_plan(
        self,
        plan: Plan,
        critiques: List[PlanCritique],
        context_files: List[str],
    ) -> Plan:
        revised = plan.model_copy(deep=True)
        critique_codes = {critique.code for critique in critiques}
        if "missing_verification_task" in critique_codes:
            self._ensure_verification_task(revised, context_files)
        return revised

    def _ensure_verification_task(self, plan: Plan, context_files: List[str]) -> None:
        for phase in plan.phases:
            for phase_task in phase.tasks:
                descriptor = (
                    f"{phase_task.task.title} {phase_task.task.description} {phase_task.task.phase}"
                ).lower()
                if "verif" in descriptor or "review" in descriptor or "qa" in descriptor:
                    return

        if not plan.phases:
            plan.phases.append(
                PlanPhase(name="Phase 1", objective="Verification", tasks=[])
            )
        verification_phase = plan.phases[-1]
        verification_score = self.classifier.classify(
            title="Verification",
            description="Verify task outcomes against acceptance criteria",
            acceptance_criteria=["Verification checks pass"],
            context_files=context_files,
        )
        verification_phase.tasks.append(
            PlanTask(
                task=TaskDocument(
                    task_id="plan-verification-gate",
                    title="Verification gate",
                    description="Run deterministic verification and confirm acceptance criteria alignment",
                    phase=verification_phase.name,
                    acceptance_criteria=["Verification checks pass"],
                    selected_backend=verification_score.recommended_backend,
                    model=self.model_profiles.get_best_model_for_backend(
                        backend_name=verification_score.recommended_backend,
                        task_type="review",
                        cost_tier="medium",
                        context_size=32000,
                    ),
                )
            )
        )
