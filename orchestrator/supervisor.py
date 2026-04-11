"""Supervisor orchestrator implementation."""
from __future__ import annotations

import uuid
from typing import Optional

from agents.management_agent import ManagementAgent
from agents.planning_agent import PlanningAgent
from agents.research_agent import ResearchAgent
from agents.reviewer_agent import ReviewerAgent
from agents.verifier_agent import VerifierAgent
from backends.base import BackendResult
from config import AppConfig, load_config
from models.plan import Plan
from models.project import ProjectRequest, TaskDocument
from models.reports import BackendExecution, OrchestrationReport
from runtime.deep_agent_factory import DeepAgentFactory
from runtime.logging import configure_logging
from runtime.router import BackendRouter
from runtime.state_store import StateStore


class SupervisorOrchestrator:
    """Coordinates agents and coding backends."""

    def __init__(self, config: Optional[AppConfig] = None) -> None:
        self.config = config or load_config()
        self.state_store = StateStore(self.config)
        self.logger = configure_logging(self.config)
        self.factory = DeepAgentFactory(self.config.deep_agent)
        self.planning_agent = PlanningAgent(self.factory)
        self.research_agent = ResearchAgent(self.factory)
        self.management_agent = ManagementAgent(self.factory, self.state_store)
        self.reviewer_agent = ReviewerAgent(self.factory)
        self.verifier_agent = VerifierAgent(self.factory)
        self.router = BackendRouter(self.config)

    def run(self, request: ProjectRequest) -> OrchestrationReport:
        plan = self.planning_agent.create_plan(request)
        self.management_agent.register_plan(plan)
        task = self._select_task(plan)
        context = self.research_agent.gather(request)
        decision = self.router.select(task)
        backend = decision.backend()
        backend_result = backend.execute(task, context, dry_run=True)
        execution = self._to_backend_execution(backend_result)
        review = self.reviewer_agent.review(task, execution)
        verification = self.verifier_agent.verify(task, execution)
        run_id = str(uuid.uuid4())
        self.management_agent.record_execution(
            run_id=run_id,
            task=task,
            backend=execution.backend,
            reviewer_status=review.status,
            verifier_status=verification.status,
            status="ok" if execution.exit_code == 0 else "failed",
        )
        report = OrchestrationReport(
            plan_summary=plan.summary,
            backend_execution=execution,
            review=review,
            verification=verification,
            metadata={"run_id": run_id, "backend_reason": decision.reason},
        )
        self._persist_report(report)
        self.logger.info(
            "run=%s backend=%s review=%s verification=%s",
            run_id,
            execution.backend,
            review.status,
            verification.status,
        )
        return report

    def _select_task(self, plan: Plan) -> TaskDocument:
        for phase in plan.phases:
            for plan_task in phase.tasks:
                return plan_task.task
        raise RuntimeError("Plan contains no tasks")

    def _to_backend_execution(self, result: BackendResult) -> BackendExecution:
        return BackendExecution(
            backend=result.backend,
            command=result.command,
            stdout=result.stdout,
            stderr=result.stderr,
            exit_code=result.exit_code,
            duration_seconds=result.duration_seconds,
        )

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
    return orchestrator.run(demo_request())
