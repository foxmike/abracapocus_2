"""Supervisor orchestrator implementation."""
from __future__ import annotations

import uuid
from pathlib import Path
from typing import Optional

from agents.management_agent import ManagementAgent
from agents.planning_agent import PlanningAgent
from agents.research_agent import ResearchAgent
from agents.reviewer_agent import ReviewerAgent
from agents.verifier_agent import VerifierAgent
from backends.base import BackendResult
from config import AppConfig, load_config
from models.plan import Plan, PlanPhase, PlanTask
from models.project import ProjectRequest, TaskDocument
from models.reports import (
    BackendExecution,
    ChangeAssessment,
    OrchestrationReport,
    ReviewReport,
    VerificationReport,
)
from runtime.deep_agent_factory import DeepAgentFactory
from runtime.logging import configure_logging
from runtime.router import BackendRouter
from runtime.state_store import StateStore


class SupervisorOrchestrator:
    """Coordinates agents and coding backends."""

    def __init__(self, config: Optional[AppConfig] = None) -> None:
        self.config = config or load_config()
        self.state_store = StateStore(self.config)
        initial_state = self.state_store.read_state()
        self._apply_overrides(initial_state.operator_overrides)
        self.logger = configure_logging(self.config)
        self.factory = DeepAgentFactory(self.config.deep_agent)
        self.planning_agent = PlanningAgent(self.factory)
        self.research_agent = ResearchAgent(self.factory)
        self.management_agent = ManagementAgent(self.factory, self.state_store)
        self.reviewer_agent = ReviewerAgent(self.factory)
        self.verifier_agent = VerifierAgent(self.factory, self.config.verification)
        self.router = BackendRouter(self.config)

    def run(self, request: ProjectRequest, task: TaskDocument | None = None) -> OrchestrationReport:
        state_snapshot = self.state_store.read_state()
        existing_plan = self._load_plan_file(state_snapshot.plan_version)
        if task is None:
            plan = self.planning_agent.create_plan(request, previous_plan=existing_plan)
        else:
            plan = self._build_task_plan(request, task)
        self.management_agent.register_plan(plan)
        task = self._select_task(plan)
        task.status = "in_progress"
        context = self.research_agent.gather(request)
        decision = self.router.select(task)
        if not task.selected_backend:
            task.selected_backend = decision.backend_name
        backend = decision.backend()
        results: list[BackendResult] = []
        dry_run = not getattr(backend, "supports_direct_execution", False)
        models_to_run = decision.models or [None]
        for model_name in models_to_run:
            tags = decision.model_tags.get(model_name or "", []) if model_name else []
            result = backend.execute(
                task,
                context,
                dry_run=dry_run,
                model=model_name,
                model_tags=tags,
                task_type=decision.task_type,
            )
            results.append(result)
        executions = [self._to_backend_execution(item) for item in results]
        review = self._run_review(task, executions)
        verification = self._run_verification(task, executions)
        run_id = str(uuid.uuid4())
        any_success = any(execution.exit_code == 0 for execution in executions)
        task.status = "completed" if any_success else "failed"
        self.management_agent.record_execution(
            run_id=run_id,
            task=task,
            backend=executions[0].backend,
            reviewer_status=review.status,
            verifier_status=verification.status,
            status="ok" if any_success else "failed",
        )
        assessment = self._assess_changes(task, executions, verification)
        report = OrchestrationReport(
            plan_summary=plan.summary,
            backend_executions=executions,
            review=review,
            verification=verification,
            change_assessment=assessment,
            metadata={
                "run_id": run_id,
                "backend_reason": decision.reason,
                "models": decision.models,
                "task_type": decision.task_type,
                "task_id": task.task_id,
                "task_title": task.title,
                "task_status": task.status,
                "selected_backend": task.selected_backend,
                "verification_profile": task.verification_profile,
            }
            | decision.metadata,
        )
        self._persist_report(report)
        self.logger.info(
            "run=%s backend=%s review=%s verification=%s",
            run_id,
            executions[0].backend,
            review.status,
            verification.status,
        )
        return report

    def _select_task(self, plan: Plan) -> TaskDocument:
        for phase in plan.phases:
            for plan_task in phase.tasks:
                return plan_task.task
        raise RuntimeError("Plan contains no tasks")

    def _build_task_plan(self, request: ProjectRequest, task: TaskDocument) -> Plan:
        phase = PlanPhase(
            name=f"{task.phase.title()} Phase" if task.phase else "Task Phase",
            objective=task.description or task.title,
            tasks=[PlanTask(task=task)],
        )
        return Plan(
            project_name=request.project_name,
            summary=f"Task run: {task.title}",
            phases=[phase],
            version=f"task-{task.task_id}",
        )

    def _to_backend_execution(self, result: BackendResult) -> BackendExecution:
        return BackendExecution(
            backend=result.backend,
            command=result.command,
            stdout=result.stdout,
            stderr=result.stderr,
            exit_code=result.exit_code,
            duration_seconds=result.duration_seconds,
            model=result.model,
            model_tags=result.model_tags,
            task_type=result.task_type,
            working_directory=result.working_directory,
            changed_files=result.changed_files,
            diff_summary=result.diff_summary,
        )

    def _run_review(self, task: TaskDocument, executions: list[BackendExecution]) -> ReviewReport:
        if not self.config.routing.reviewer_required:
            return ReviewReport(status="skipped", findings=[], summary="Reviewer disabled")
        return self.reviewer_agent.review(task, executions)

    def _run_verification(self, task: TaskDocument, executions: list[BackendExecution]) -> VerificationReport:
        if not self.config.routing.verification_required:
            return VerificationReport(
                status="skipped",
                checks=[],
                notes="Verifier disabled",
                profile=self.config.verification.active_profile,
            )
        return self.verifier_agent.verify(task, executions)

    def _assess_changes(
        self,
        task: TaskDocument,
        executions: list[BackendExecution],
        verification: VerificationReport,
    ) -> ChangeAssessment:
        primary = executions[0] if executions else None
        changed_files = primary.changed_files if primary else []
        diff_summary = primary.diff_summary if primary else ""
        changed_summary = diff_summary or (f"{len(changed_files)} files changed" if changed_files else "No file changes recorded")
        verification_summary = verification.status
        if verification.status == "failed":
            assessment_status = "not_aligned"
            notes = "Verification failed"
        elif verification.status == "skipped":
            assessment_status = "partially_aligned"
            notes = "Verification skipped"
        elif changed_files:
            assessment_status = "aligned"
            notes = "Changes detected and verification passed"
        else:
            assessment_status = "partially_aligned"
            notes = "No file changes detected"
        return ChangeAssessment(
            task_intent=task.description or task.title,
            changed_files_summary=changed_summary,
            verification_summary=verification_summary,
            assessment_status=assessment_status,
            notes=notes,
        )

    def _apply_overrides(self, overrides: dict | None) -> None:
        if not overrides:
            return
        backend_override = overrides.get("backend")
        if backend_override:
            self.config.routing.manual_backend = backend_override
        profile_override = overrides.get("verification_profile")
        if profile_override and self.config.verification.has_profile(profile_override):
            self.config.verification.active_profile = profile_override
        agents = overrides.get("agents", {})
        if "reviewer" in agents:
            self.config.routing.reviewer_required = bool(agents["reviewer"])
        if "verifier" in agents:
            self.config.routing.verification_required = bool(agents["verifier"])

    def _load_plan_file(self, version: str | None) -> Plan | None:
        if not version:
            return None
        path = self.config.paths.plans_dir / f"{version}.json"
        if not path.exists():
            return None
        return Plan.model_validate_json(path.read_text(encoding="utf-8"))

    def _persist_report(self, report: OrchestrationReport) -> None:
        reports_dir = self.config.paths.reports_dir
        reports_dir.mkdir(parents=True, exist_ok=True)
        path = reports_dir / f"run-{report.metadata['run_id']}.json"
        path.write_text(report.model_dump_json(indent=2), encoding="utf-8")


def demo_request() -> ProjectRequest:
    return ProjectRequest(
        project_name="abracapocus_2",
        goal="Scaffold Deep Agents orchestration",
        context="demo",
    )


def run_demo() -> OrchestrationReport:
    orchestrator = SupervisorOrchestrator()
    task = TaskDocument(
        task_id="demo-self-improve",
        title="Refresh demo status log",
        description="Update docs/demo_status.md with the latest demo guidance",
        phase="implementation",
        acceptance_criteria=[
            "docs/demo_status.md exists",
            "Log includes latest task details",
        ],
        selected_backend="demo_cli",
        verification_profile="default",
    )
    request = demo_request()
    request.goal = task.description
    return orchestrator.run(request, task=task)
