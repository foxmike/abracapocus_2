"""Management agent for project state."""
from __future__ import annotations

from datetime import datetime
from pathlib import Path

from agents.base import BaseAgent
from models.plan import Plan
from models.project import TaskDocument
from models.state import ExecutionHistory, RuntimeState, TaskRecord, TaskStatus
from runtime.deep_agent_factory import DeepAgentFactory
from runtime.state_store import StateStore


class ManagementAgent(BaseAgent):
    def __init__(self, factory: DeepAgentFactory, state_store: StateStore) -> None:
        super().__init__(
            name="management_agent",
            prompt_file="prompts/management.md",
            skills=["skills/task_handoff", "skills/change_assessment"],
            factory=factory,
        )
        self.state_store = state_store

    def register_plan(self, plan: Plan) -> RuntimeState:
        def _update(state: RuntimeState) -> RuntimeState:
            records = [
                TaskRecord(
                    task_id=phase_task.task.task_id,
                    title=phase_task.task.title,
                    phase=phase.name,
                    backend=phase_task.task.selected_backend or state.default_backend,
                )
                for phase in plan.phases
                for phase_task in phase.tasks
            ]
            state.plan_version = plan.version
            state.tasks = records
            state.active_phase = plan.phases[0].name
            state.completed_phases = [phase.name for phase in plan.phases if phase.completed]
            state.remaining_phases = [phase.name for phase in plan.phases if not phase.completed]
            return state

        self.invoke({"plan_version": plan.version, "phase_count": len(plan.phases)})
        updated = self.state_store.update(_update)
        self._persist_plan(plan)
        return updated

    def record_execution(
        self,
        run_id: str,
        task: TaskDocument,
        backend: str,
        reviewer_status: str,
        verifier_status: str,
        status: str,
    ) -> RuntimeState:
        timestamp = datetime.utcnow()

        def _update(state: RuntimeState) -> RuntimeState:
            for record in state.tasks:
                if record.task_id == task.task_id:
                    record.status = TaskStatus.completed if status == "ok" else TaskStatus.blocked
                    record.backend = backend
                    record.last_run = timestamp
                    break
            state.history.append(
                ExecutionHistory(
                    run_id=run_id,
                    task_id=task.task_id,
                    backend=backend,
                    status=status,
                    reviewer_status=reviewer_status,
                    verifier_status=verifier_status,
                )
            )
            return state

        self.invoke({"task_id": task.task_id, "status": status})
        return self.state_store.update(_update)

    def _persist_plan(self, plan: Plan) -> None:
        plans_dir = Path("plans")
        plans_dir.mkdir(parents=True, exist_ok=True)
        path = plans_dir / f"{plan.version}.json"
        path.write_text(plan.model_dump_json(indent=2), encoding="utf-8")
