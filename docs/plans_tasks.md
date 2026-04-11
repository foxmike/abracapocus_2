# Plans, Phases, Tasks, and Reports

## Plans

Stored under `plans/` as JSON. Each plan uses the `models.plan.Plan` schema and includes:
- `project_name`
- `summary`
- `version`
- `phases` (array of `PlanPhase` objects)

Plans can be initialized via `make plan-init` or programmatically via the planning agent when the supervisor runs. The management agent writes plan metadata into `state/runtime_state.json` for quick lookup.

## Phases

`phases/<phase_name>.json` capture the state of each phase, e.g., ownership, entry/exit criteria, and outstanding tasks. `make phase-init` scaffolds these files, and `make phase-show` prints them.

## Tasks

`tasks/<task_id>.json` follow `models.project.TaskDocument`. They may be created manually (`make task-init`) or derived from plans. `task-run` loads a task file and invokes the supervisor orchestrator for that task, enabling iterative work on large programs.

## Reports

Each orchestration creates `reports/run-<uuid>.json`, containing:
- Plan summary snapshot
- Backend execution details (command, stdout/stderr, exit code)
- Review report (status + findings)
- Verification report (status + checks)
- Metadata (routing reason, run id)

These reports offer deterministic auditing and handoff-ready documentation.

## Change assessments and handoffs

The management agent records execution history (task id, backend, reviewer/verifier status) so that future plan revisions have a canonical view of what changed. Skills such as `skills/change_assessment` and `skills/task_handoff` describe the future Deep Agents behavior expected when the system starts executing real CLI commands.
