"""Supervisor orchestrator implementation."""
from __future__ import annotations

import os
import uuid
from dataclasses import dataclass
from pathlib import Path
from typing import Annotated, List, Optional, Sequence

from typing_extensions import TypedDict

from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.errors import GraphInterrupt
from langgraph.graph import END, START, StateGraph
from langgraph.types import Command, Interrupt, Send, interrupt

import typer
from agents.management_agent import ManagementAgent
from agents.planning_agent import PlanningAgent
from agents.research_agent import ResearchAgent
from agents.reviewer_agent import ReviewerAgent
from agents.verifier_agent import VerifierAgent
from backends.base import BackendResult
from config import AppConfig, load_config
from models.plan import Plan, PlanPhase, PlanTask
from models.project import ContextPackage, ProjectRequest, TaskDocument
from models.reports import (
    BackendExecution,
    ChangeAssessment,
    OrchestrationReport,
    ReviewReport,
    VerificationReport,
)
from runtime.deep_agent_factory import DeepAgentFactory
from runtime.agents_md import compose_agents_backend_notes, load_root_agents_md
from runtime.logging import configure_logging
from runtime.router import BackendRouter
from runtime.state_store import StateStore


@dataclass
class TaskResult:
    task: TaskDocument
    execution: BackendExecution
    review: ReviewReport
    status: str


@dataclass
class PhaseResult:
    phase_name: str
    task_results: List[TaskResult]
    verification: VerificationReport
    status: str


class _ResetTaskResults(list):
    """Sentinel list type that signals the reducer to reset accumulated results."""


def _task_results_reducer(
    current: Optional[List[TaskResult]], update: List[TaskResult]
) -> List[TaskResult]:
    if isinstance(update, _ResetTaskResults):
        return list(update)
    merged: List[TaskResult] = list(current or [])
    merged.extend(update)
    return merged


class SupervisorState(TypedDict):
    request: ProjectRequest
    plan: Plan | None
    context: ContextPackage | None
    phase_index: int
    task_results: Annotated[List[TaskResult], _task_results_reducer]
    phase_results: List[PhaseResult]
    run_id: str
    final_report: OrchestrationReport | None


class SupervisorOrchestrator:
    """LangGraph-based supervisor orchestrator."""

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
        self._agents_md, self._agents_metadata = load_root_agents_md(self.config.paths.root_dir)
        self._task_override: TaskDocument | None = None
        self.graph = self._build_graph()

    def run(self, request: ProjectRequest, task: TaskDocument | None = None) -> OrchestrationReport:
        run_id = str(uuid.uuid4())
        initial_state: SupervisorState = {
            "request": request,
            "plan": None,
            "context": None,
            "phase_index": -1,
            "task_results": [],
            "phase_results": [],
            "run_id": run_id,
            "final_report": None,
        }
        config = {"configurable": {"thread_id": run_id}}
        final_state: SupervisorState | None = None
        self._task_override = task
        try:
            try:
                for state in self.graph.stream(initial_state, config, stream_mode="values"):
                    final_state = state  # type: ignore[assignment]
            except GraphInterrupt as exc:
                typer.echo(f"[abracapocus] Human checkpoint: {exc}")
                input("Press Enter to continue...")
                for state in self.graph.stream(Command(resume=True), config, stream_mode="values"):
                    final_state = state  # type: ignore[assignment]
        finally:
            self._task_override = None
        if final_state is None:
            raise RuntimeError("Graph execution did not complete")
        report = final_state.get("final_report")
        if report is None:
            raise RuntimeError("Final report missing from completed state")
        return report

    # Graph construction -------------------------------------------------

    def _build_graph(self):
        builder = StateGraph(SupervisorState)
        builder.add_node("planning_node", self._planning_node)
        builder.add_node("research_node", self._research_node)
        builder.add_node("phase_router", self._phase_router)
        builder.add_node("finalize_node", self._finalize_node)
        builder.add_node("task_node", self._task_node)
        builder.add_node("verification_node", self._verification_node)
        builder.add_node("phase_advance", self._phase_advance)
        builder.add_node("human_checkpoint", self._human_checkpoint)
        builder.add_edge(START, "planning_node")
        builder.add_edge("planning_node", "research_node")
        builder.add_edge("research_node", "phase_router")
        builder.add_edge("task_node", "verification_node")
        builder.add_edge("verification_node", "phase_advance")
        builder.add_edge("human_checkpoint", "phase_router")
        builder.add_edge("finalize_node", END)
        checkpoints_path = Path("state") / "checkpoints.db"
        checkpoints_path.parent.mkdir(parents=True, exist_ok=True)
        import sqlite3
        conn = sqlite3.connect(str(checkpoints_path), check_same_thread=False)
        checkpointer = SqliteSaver(conn)
        return builder.compile(checkpointer=checkpointer)

    # LangGraph nodes ----------------------------------------------------

    def _planning_node(self, state: SupervisorState) -> dict:
        runtime_state = self.state_store.read_state()
        previous_plan = self._load_plan_file(runtime_state.plan_version)
        if self._task_override:
            plan = self._build_task_plan(state["request"], self._task_override)
        else:
            plan = self.planning_agent.create_plan(state["request"], previous_plan=previous_plan)
        self.management_agent.register_plan(plan)
        return {"plan": plan, "phase_index": -1}

    def _research_node(self, state: SupervisorState) -> dict:
        context = self.research_agent.gather(state["request"])
        agents_notes = compose_agents_backend_notes(self._agents_md)
        notes = context.notes
        if agents_notes:
            notes = f"{notes}; {agents_notes}" if notes else agents_notes
        context = context.model_copy(
            update={
                "notes": notes,
                "agents_md": self._agents_md,
                "agents_metadata": self._agents_metadata,
            }
        )
        return {"context": context}

    def _phase_router(self, state: SupervisorState) -> Command:
        plan = state["plan"]
        if plan is None:
            raise RuntimeError("Plan missing during phase routing")
        next_index = self._next_incomplete_phase_index(plan)
        if next_index is None:
            return Command(goto="finalize_node")
        phase = plan.phases[next_index]
        phase.status = "in_progress"
        updates = {"phase_index": next_index, "task_results": self._reset_task_results()}
        context = state["context"]
        sends: List[Send] = [
            Send(
                "task_node",
                {
                    "task": phase_task.task,
                    "context": context,
                    "phase_name": phase.name,
                },
            )
            for phase_task in phase.tasks
        ]
        if sends:
            return Command(update=updates, goto=sends)
        return Command(update=updates, goto="verification_node")

    def _finalize_node(self, state: SupervisorState) -> dict:
        report = self._assemble_final_report(state)
        self._persist_report(report)
        self.logger.info(
            "run=%s phases=%d verification=%s",
            state["run_id"],
            len(state["phase_results"]),
            report.verification.status,
        )
        return {"final_report": report}

    def _task_node(self, send_state: dict) -> dict:
        task: TaskDocument = send_state["task"]
        context: ContextPackage | None = send_state.get("context")
        phase_name: str = send_state.get("phase_name", task.phase or "unknown")
        prefix = f"[abracapocus][phase:{phase_name}][task:{task.task_id}]"
        print(f"{prefix} routing task via backend router")
        decision = self.router.select(task)
        backend = decision.backend(self.config.paths.working_root)
        if not task.selected_backend:
            task.selected_backend = decision.backend_name
        dry_run = not getattr(backend, "supports_direct_execution", False)
        model_names = decision.models or [None]
        execution: BackendExecution | None = None
        for model_name in model_names:
            tags = decision.model_tags.get(model_name or "", [])
            try:
                result = backend.execute(
                    task,
                    context or ContextPackage(summaries=[], files=[], notes=""),
                    dry_run=dry_run,
                    model=model_name,
                    model_tags=tags,
                    task_type=decision.task_type,
                )
                execution = self._to_backend_execution(result)
            except Exception as exc:  # pragma: no cover - unexpected backend failure
                execution = BackendExecution(
                    backend=decision.backend_name,
                    command=[],
                    stdout="",
                    stderr=str(exc),
                    exit_code=1,
                    duration_seconds=0.0,
                    model=model_name,
                    model_tags=tags,
                    task_type=decision.task_type,
                    working_directory=None,
                    changed_files=[],
                    diff_summary="backend execution failed",
                )
            if execution.exit_code == 0:
                break
        if execution is None:
            raise RuntimeError("Backend execution did not produce a result")
        review = self._run_review(task, [execution])
        status = "passed" if execution.exit_code == 0 else "failed"
        task.status = "completed" if status == "passed" else "failed"
        print(f"{prefix} execution exit_code={execution.exit_code}")
        result = TaskResult(task=task, execution=execution, review=review, status=status)
        return {"task_results": [result]}

    def _verification_node(self, state: SupervisorState) -> dict:
        plan = state["plan"]
        phase_index = state["phase_index"]
        if plan is None or phase_index < 0:
            raise RuntimeError("Plan or phase index missing during verification")
        phase = plan.phases[phase_index]
        task_results = list(state["task_results"])
        executions = [result.execution for result in task_results]
        phase_verification_profile = next(
            (
                result.task.verification_profile
                for result in task_results
                if result.task.verification_profile
            ),
            None,
        )
        verification_task = TaskDocument(
            task_id=f"{phase.name}-verification",
            title=f"Verify phase {phase.name}",
            description=phase.objective,
            phase=phase.name,
            verification_profile=phase_verification_profile,
        )
        print(f"[abracapocus][verification:{phase.name}] starting verification for {len(task_results)} tasks")
        verification = (
            self._run_verification(verification_task, executions)
            if executions
            else VerificationReport(
                status="skipped",
                checks=[],
                notes="No tasks executed in phase",
                profile=self.config.verification.active_profile,
            )
        )
        all_tasks_passed = all(result.status == "passed" for result in task_results)
        phase_status = "passed" if verification.status == "passed" and all_tasks_passed else "failed"
        print(f"[abracapocus][verification:{phase.name}] status={verification.status}")
        phase_result = PhaseResult(
            phase_name=phase.name,
            task_results=task_results,
            verification=verification,
            status=phase_status,
        )
        phase_results = list(state["phase_results"])
        phase_results.append(phase_result)
        return {"phase_results": phase_results}

    def _phase_advance(self, state: SupervisorState) -> Command:
        plan = state["plan"]
        phase_index = state["phase_index"]
        if plan is None or phase_index < 0 or not state["phase_results"]:
            return Command(goto="phase_router")
        phase = plan.phases[phase_index]
        latest_result = state["phase_results"][-1]
        plan.record_completion(phase.name)
        next_index = self._next_incomplete_phase_index(plan)
        next_phase_name = plan.phases[next_index].name if next_index is not None else "completed"
        for task_result in latest_result.task_results:
            run_status = "ok" if task_result.execution.exit_code == 0 else "failed"
            self.management_agent.record_execution(
                run_id=state["run_id"],
                task=task_result.task,
                backend=task_result.execution.backend,
                reviewer_status=task_result.review.status,
                verifier_status=latest_result.verification.status,
                status=run_status,
            )
        runtime_state = self.state_store.read_state()
        runtime_state.completed_phases = [p.name for p in plan.phases if p.completed]
        runtime_state.remaining_phases = [p.name for p in plan.phases if not p.completed]
        runtime_state.active_phase = next_phase_name
        runtime_state.plan_version = plan.version
        self.state_store.write_state(runtime_state)
        updates = {"plan": plan, "task_results": self._reset_task_results()}
        if self._should_checkpoint(phase):
            return Command(update=updates, goto="human_checkpoint")
        return Command(update=updates, goto="phase_router")

    def _human_checkpoint(self, state: SupervisorState) -> dict:
        plan = state["plan"]
        phase_index = state["phase_index"]
        phase_name = "unknown"
        if plan and 0 <= phase_index < len(plan.phases):
            phase_name = plan.phases[phase_index].name
        response = interrupt(f"Phase '{phase_name}' completed. Confirm to continue.")
        print(f"[abracapocus][phase:{phase_name}] human checkpoint confirmed: {response}")
        return {}

    # Helper logic -------------------------------------------------------

    def _handle_interrupts(self, interrupts: Sequence[Interrupt]) -> Command:
        responses: dict[str, str] = {}
        for interrupt_info in interrupts:
            prompt = str(interrupt_info.value)
            user_response = input(f"{prompt} (press Enter to continue) ").strip() or "confirmed"
            responses[interrupt_info.id] = user_response
        if len(responses) == 1:
            return Command(resume=next(iter(responses.values())))
        return Command(resume=responses)

    def _reset_task_results(self) -> List[TaskResult]:
        return _ResetTaskResults()

    def _next_incomplete_phase_index(self, plan: Plan) -> int | None:
        for idx, phase in enumerate(plan.phases):
            if not phase.completed:
                return idx
        return None

    def _should_checkpoint(self, phase: PlanPhase) -> bool:
        if phase.human_checkpoint is not None:
            return phase.human_checkpoint
        return os.getenv("HUMAN_CHECKPOINTS", "false").lower() in {"1", "true", "yes", "on"}

    def _assemble_final_report(self, state: SupervisorState) -> OrchestrationReport:
        plan = state["plan"]
        phase_results = state["phase_results"]
        all_task_results = [task for phase in phase_results for task in phase.task_results]
        backend_executions = [task.execution for task in all_task_results]
        combined_review = self._combine_reviews(all_task_results)
        combined_verification = self._combine_phase_verifications(phase_results)
        if all_task_results:
            reference_task = all_task_results[0].task
        else:
            reference_task = TaskDocument(
                task_id=f"{state['run_id']}-aggregate",
                title=state["request"].goal,
                description=state["request"].goal,
                phase="aggregate",
            )
        assessment = self._assess_changes(reference_task, backend_executions, combined_verification)
        first_task = all_task_results[0].task if all_task_results else None
        metadata = {
            "run_id": state["run_id"],
            "project_name": state["request"].project_name,
            "plan_version": plan.version if plan else None,
            "task_id": first_task.task_id if first_task else None,
            "task_title": first_task.title if first_task else None,
            "task_status": first_task.status if first_task else None,
            "selected_backend": first_task.selected_backend if first_task else None,
            "verification_profile": first_task.verification_profile if first_task else None,
            "backend_reason": "phase_based",
            "agents_md": {
                "loaded": self._agents_metadata.get("loaded", False),
                "path": self._agents_metadata.get("path"),
                "rule_count": self._agents_metadata.get("rule_count", 0),
                "sha256_12": self._agents_metadata.get("sha256_12"),
            },
            "phase_results": [
                {
                    "phase_name": phase.phase_name,
                    "status": phase.status,
                    "verification": phase.verification.status,
                    "task_results": [
                        {
                            "task_id": task.task.task_id,
                            "status": task.status,
                            "backend": task.execution.backend,
                        }
                        for task in phase.task_results
                    ],
                }
                for phase in phase_results
            ],
        }
        return OrchestrationReport(
            plan_summary=plan.summary if plan else state["request"].goal,
            backend_executions=backend_executions,
            review=combined_review,
            verification=combined_verification,
            change_assessment=assessment,
            metadata=metadata,
        )

    def _combine_reviews(self, task_results: List[TaskResult]) -> ReviewReport:
        if not task_results:
            return ReviewReport(status="skipped", findings=[], summary="No tasks executed")
        findings = []
        summary_parts = []
        statuses = []
        for result in task_results:
            findings.extend(result.review.findings)
            summary_parts.append(f"{result.task.task_id}:{result.review.summary}")
            statuses.append(result.review.status)
        if any(status == "changes_requested" for status in statuses):
            status = "changes_requested"
        elif all(status == "skipped" for status in statuses):
            status = "skipped"
        else:
            status = "approved"
        summary = "; ".join(summary_parts) if summary_parts else "Review completed"
        return ReviewReport(status=status, findings=findings, summary=summary)

    def _combine_phase_verifications(self, phase_results: List[PhaseResult]) -> VerificationReport:
        if not phase_results:
            return VerificationReport(
                status="skipped",
                checks=[],
                notes="No phases executed",
                profile=self.config.verification.active_profile,
            )
        checks = []
        notes = []
        statuses = []
        profile = self.config.verification.active_profile
        for result in phase_results:
            checks.extend(result.verification.checks)
            notes.append(f"{result.phase_name}:{result.verification.status}")
            statuses.append(result.verification.status)
            profile = result.verification.profile
        if any(status == "failed" for status in statuses):
            status = "failed"
        elif all(status == "skipped" for status in statuses):
            status = "skipped"
        else:
            status = "passed"
        note_text = "; ".join(notes) if notes else "Verification complete"
        return VerificationReport(status=status, checks=checks, notes=note_text, profile=profile)

    # Existing helper methods retained -----------------------------------

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

    def _run_review(self, task: TaskDocument, executions: List[BackendExecution]) -> ReviewReport:
        if not self.config.routing.reviewer_required:
            return ReviewReport(status="skipped", findings=[], summary="Reviewer disabled")
        return self.reviewer_agent.review(task, executions)

    def _run_verification(self, task: TaskDocument, executions: List[BackendExecution]) -> VerificationReport:
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
        executions: List[BackendExecution],
        verification: VerificationReport,
    ) -> ChangeAssessment:
        primary = executions[0] if executions else None
        changed_files = primary.changed_files if primary else []
        diff_summary = primary.diff_summary if primary else ""
        if diff_summary:
            changed_summary = diff_summary
        elif changed_files:
            changed_summary = f"{len(changed_files)} files changed"
        else:
            changed_summary = "No file changes recorded"
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
