# Operations Guide

## Environments

Set environment variables in `.env` or via the shell. Key ones:
- `APP_ENV`: `development`, `staging`, or `production`.
- `DEFAULT_BACKEND`: default coding backend name.
- `ROUTING_MODE`: `manual`, `rules`, or `auto`.
- `DEEP_AGENT_MOCK_MODE`: set to `false` to use a real LangChain Deep Agent stack.
- `DEEP_AGENT_MODEL`: LLM name for Deep Agents when mock mode is disabled.

## Installing

```bash
make install
```
Installs the Python dependencies listed in `requirements.txt` in the active environment.

## Running the orchestrator

- `make run GOAL="Ship feature" CONTEXT="phase alpha"`
- `make demo` triggers `python main.py demo`.
- `make task-run TASK=tasks/sample_task.json` routes through the supervisor using the selected backend.

## State management

Runtime state lives in `state/runtime_state.json`. Use:
- `make state-show`
- `make state-reset`

## Plan/phase/task utilities

`python -m scripts.ops` offers subcommands used by the Makefile:
- `plan-init --name master --summary "..."`
- `plan-show`
- `phase-init --name phase-1`
- `phase-show phase-1`
- `task-init --id task-1 --title "Implement" --phase phase-1`
- `task-list`
- `task-show task-1`

These commands create JSON documents under `plans/`, `phases/`, and `tasks/` to coordinate long-lived programs.

## Routing + backend control

- `make backend-list`
- `make backend-set NAME=claude_code_cli`
- `make config-show`

Routing policies are defined in `runtime/router.py`. Operators can toggle manual or rules-based routing at runtime by editing `.env` or setting environment variables before invoking commands.

## Verification-first workflow

Every run triggers `VerifierAgent.verify`, which currently performs `py_compile`. Extend the method to call your own deterministic CI/lint/test suites. `make test` executes the internal pytest suite.

## Logs and reports

- Logs: `logs/abracapocus.log` (append-only).
- Reports: `reports/run-<uuid>.json` contain the orchestration inputs/outputs.
- Execution history: stored in `state/runtime_state.json` for historical auditing.

## Extending scripts

`scripts/ops.py` is Typer-based; add new commands or reuse existing helpers when wiring new Makefile targets. All scripts avoid shell-specific tooling for portability.
