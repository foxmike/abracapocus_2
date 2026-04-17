# abracapocus_2 Quickstart Guide

## 1. What is abracapocus_2
abracapocus_2 is a LangGraph-based agentic coding platform that orchestrates Codex, Aider, Gemini, and Claude Code CLI backends—plus a demo backend—to autonomously develop software projects. The supervisor agent plans multi-phase work, dispatches tasks to the optimal backend, runs reviewer and verifier agents, and emits detailed reports so large features can move through planning, parallel execution, verification, and reporting with minimal human intervention.

## 2. Prerequisites
### Python runtime and dependencies
- Python 3.11+ (see `pyproject.toml`).
- A virtual environment is recommended. Install dependencies with `make install`, which runs `pip install -r requirements.txt`.

### Optional coding CLIs
Install any backends you plan to run in direct-execution mode:
- `codex` (Codex CLI)
- `aider`
- `gemini`
- `claude-code`

The system automatically falls back to dry-run simulations when a CLI is missing, but installing the tools unlocks real edits.

### Required environment variables
| Variable | Purpose / effect | Typical values |
| --- | --- | --- |
| `APP_ENV` | Sets runtime mode recorded in reports and logs. | `development` \| `staging` \| `production` |
| `DEFAULT_BACKEND` | Supervisor fallback backend when no overrides apply. | `codex_cli`, `aider_cli`, etc. |
| `BACKEND_OVERRIDE` | Forces `RoutingSettings.manual_backend`. Used when `ROUTING_MODE=manual`. | backend name |
| `ROUTING_MODE` | Routing policy: `manual`, `rules`, or `auto` (see `runtime/router.py`). | `manual` (default) |
| `ABRACAPOCUS_ALLOW_MAIN` | Enables/disables protection against running from `main`/`master`. | `false` (recommended) |
| `ABRACAPOCUS_BASE_BRANCH` | Target base branch used by `make merge` / `make abandon`. | `main` (or `develop`) |
| `DEEP_AGENT_MOCK_MODE` | Toggles the LangChain Deep Agent factory between mock and real execution. | `true` \| `false` |
| `DEEP_AGENT_MODEL` | Provider:model string used when mock mode is disabled. | `openai:gpt-4o`, etc. |
| `OPENAI_API_KEY` | Required when Deep Agents call OpenAI models directly. | API key |
| `OPENROUTER_PREFERRED_MODELS` | Comma-separated list used by `select_openrouter_model` for `aider_cli`. | `openrouter/qwen/...` |
| `HUMAN_CHECKPOINTS` | Forces pauses after each phase for manual approval. | `true` \| `false` |
| `VERIFICATION_PROFILE` | Default profile (`minimal`, `default`, `strict`) if no override is set. | profile name |
| `BACKEND_OVERRIDE` | Manual backend selection; also configurable via `make backend-set`. | backend name |

Other keys such as `GOOGLE_API_KEY` or `ANTHROPIC_API_KEY` may be required by specific CLIs.

### .env setup
1. Copy the template: `cp .env.example .env`.
2. Populate the variables above plus any provider-specific API keys.
3. Keep `.env` in sync with your deployment environment; `config.py` calls `load_dotenv()` so values load automatically.

## 3. Defining a project
### Authoring a TaskDocument
Task documents live under `tasks/<task_id>.json` and follow `models.project.TaskDocument`. Example:

```json
{
  "task_id": "api-add-orders",
  "title": "Add POST /orders endpoint",
  "description": "Expose POST /orders that writes to the fulfillment service and emits audit logs.",
  "phase": "implementation",
  "acceptance_criteria": [
    "Request body validated against the schema in docs/api.md",
    "Order persisted and queued to the fulfillment service",
    "New pytest covering happy path and validation errors"
  ],
  "selected_backend": "codex_cli",
  "verification_profile": "strict"
}
```

- `task_id`: Unique identifier and filename stem.
- `title`: Operator-friendly summary used in prompts.
- `description`: Detailed brief forwarded to the backend.
- `phase`: Plan phase this task belongs to (`PlanPhase.name`).
- `acceptance_criteria`: List of concrete pass/fail checks.
- `selected_backend`: Optional override for routing.
- `verification_profile`: Optional override for verification rigor.

Create a skeleton via Makefile or the Typer CLI:

```bash
make task-init TASK=api-add-orders GOAL="Add POST /orders" PHASE=phase-2
python -m scripts.ops task-init --task-id api-add-orders --title "Add POST /orders" \
  --phase phase-2 --description "Expose POST /orders..." \
  --acceptance "Request body validated" --acceptance "New pytest" \
  --backend codex_cli --profile strict
```

Edit the resulting JSON to refine acceptance criteria or add context packages if needed.

### Initializing plan artifacts
- `make plan-init PLAN_NAME=master` writes `plans/master.json`.
- `make phase-init PHASE=phase-1` scaffolds `phases/phase-1.json`.

Run `make setup` to execute `install`, `state-reset`, and `plan-init` in one command.

### Running a single task
Execute one stored task file (file name or `task_id`):

```bash
make task-run TASK=api-add-orders CONTEXT="beta branch cut"
```

The supervisor loads the JSON, routes it to the backend, runs review + verification, and prints the resulting report. Use `make report-show` afterward to re-open the saved JSON.

### Branch workflow
abracapocus_2 can enforce per-run git branch isolation:

1. Configure protection in `.env`:
   - `ABRACAPOCUS_ALLOW_MAIN=false` to block direct runs on `main` / `master`.
   - `ABRACAPOCUS_BASE_BRANCH=main` (default) or another integration branch like `develop`.
2. Start work with `make task-run ...`; `SupervisorOrchestrator.run()` creates a run branch named `abracapocus/{task_id}-{YYYYMMDD}-{run_id[:8]}` before planning/execution starts.
3. If you are currently on `main` / `master` and protection is enabled, the run stops with a clear error until you switch branches (or explicitly set `ABRACAPOCUS_ALLOW_MAIN=true`).
4. Successful phases can auto-commit on the run branch.
5. Use `make branch-show` to inspect the latest run branch metadata.
6. Use `make merge TASK=<task_id>` to merge the run branch into the configured base branch (`ABRACAPOCUS_BASE_BRANCH`).
7. Use `make abandon TASK=<task_id>` to drop a run branch and return to the configured base branch.

Example for a non-default base branch:

```bash
ABRACAPOCUS_BASE_BRANCH=develop make merge TASK=api-add-orders
```

This routes the merge into `develop` instead of `main`.

### Running a full goal
To ask the supervisor to plan and execute a new goal end-to-end without a pre-authored task:

```bash
make run GOAL="Implement recurring billing MVP" CONTEXT="Q3 roadmap"
```

This path triggers the planning agent, generates or reuses plans/phases, and executes every phase sequentially.

### When to use task files vs. `GOAL`
- **Task files (`make task-run`)**: Repeatable work, regression fixes, or multi-day tracks where you want deterministic history under `tasks/`.
- **Direct `GOAL` (`make run`)**: Exploratory efforts or fresh initiatives where the planning agent should shape the phases on the fly using prior plan records.
- Combine both by letting `make run` create the plan, then iterating on individual tasks with `make task-run` for focused debugging.

## 4. Backends
- **`codex_cli`** (`backends/codex_cli.py`): Preferred for autonomous multi-file feature work. Builds `codex exec --full-auto` commands, honors acceptance criteria in the prompt, and sets `supports_direct_execution=True` so real edits occur when the `codex` binary is installed.
- **`aider_cli`** (`backends/aider_cli.py`): Best for targeted refactors or doc updates. It supplies up to five contextual files via `--file` flags, calls OpenRouter models, and respects `OPENROUTER_PREFERRED_MODELS`. Installs of `aider` unlock direct execution.
- **`gemini_cli`** (`backends/gemini_cli.py`): Uses `gemini code --project <phase> --task <id> --summary ...`. Good for tasks that benefit from Google Gemini’s reasoning. Requires the `gemini` CLI.
- **`claude_code_cli`** (`backends/claude_code_cli.py`): Anthropic Claude Code integration through `claude-code run`. It currently runs in dry-run mode (no `supports_direct_execution`) but still produces command traces, making it useful for design or planning tasks even if the CLI is not installed.
- **`demo_cli`** (`backends/demo_cli.py`): Safe demo/test backend that only runs `python scripts/demo_improvement.py` to append `docs/demo_status.md`. Ideal for verifying orchestration in new environments.

To set the backend:
- Per task: add `"selected_backend": "aider_cli"` to the TaskDocument.
- Operator override: `make backend-set NAME=gemini_cli` (persists into `state/runtime_state.json`).
- Ad-hoc environment override: export `BACKEND_OVERRIDE=codex_cli` before running `make run`.

The router (`runtime/router.py`) also respects `ROUTING_MODE` (`manual`, `rules`, `auto`). Rules mode recognizes simple heuristics (e.g., titles containing “refactor” -> `aider_cli`). Auto mode picks `codex_cli` for complex tasks and `gemini_cli` for lighter work. When `aider_cli` is selected, the router records the chosen OpenRouter model(s) so reports capture which model executed the task.

## 5. Verification profiles
`config.py` defines three profiles:

| Profile | Commands | When to use |
| --- | --- | --- |
| `minimal` | `python -m py_compile main.py` | Smoke-check syntax in fast prototype loops. |
| `default` | `py_compile` + `python scripts/selfcheck.py` | Day-to-day runs, ensures demo log stays healthy. |
| `strict` | `py_compile`, `pytest -q`, `pytest -q --maxfail=1` | Release candidates or risky migrations where tests must pass twice. |

- Set the global profile via `.env` (`VERIFICATION_PROFILE=strict`) or `make verification-set PROFILE=strict`.
- Override per task with `"verification_profile": "strict"` in the TaskDocument—the supervisor honors task-specific settings before falling back to the global profile.
- Run a profile manually any time using `make task-verify PROFILE=default`.

## 6. Makefile command reference
### Core workflow
| Target | Description | Example |
| --- | --- | --- |
| `help` | Lists documented targets. | `make help` |
| `install` | Installs Python dependencies. | `make install` |
| `setup` | Runs `install`, `state-reset`, and `plan-init`. | `make setup PLAN_NAME=roadmap` |
| `run` | Executes the supervisor with a new goal/context. | `make run GOAL="Ship API" CONTEXT="prod rollout"` |
| `demo` | Runs `python main.py` (demo scenario). | `make demo` |
| `test` | Executes pytest. | `make test` |
| `lint` | Runs Ruff linting. | `make lint` |
| `format` | Applies Ruff formatting. | `make format` |
| `clean` | Removes caches and report artifacts. | `make clean` |
| `tree` | Prints the repo tree. | `make tree` |
| `docs` | Lists files under `docs/`. | `make docs` |

### State, plans, and phases
| Target | Description | Example |
| --- | --- | --- |
| `state-show` | Prints `state/runtime_state.json`. | `make state-show` |
| `state-reset` | Clears runtime state. | `make state-reset` |
| `plan-init` | Creates `plans/<PLAN_NAME>.json`. | `make plan-init PLAN_NAME=release-plan` |
| `plan-show` | Displays a stored plan. | `make plan-show PLAN_NAME=release-plan` |
| `phase-init` | Creates `phases/<PHASE>.json`. | `make phase-init PHASE=phase-2` |
| `phase-show` | Displays a stored phase file. | `make phase-show PHASE=phase-2` |

### Tasks and verification
| Target | Description | Example |
| --- | --- | --- |
| `task-init` | Scaffolds `tasks/<TASK>.json` (title from `GOAL`). | `make task-init TASK=api-add GOAL="Add API endpoint" PHASE=phase-2` |
| `task-list` | Lists all task JSON files. | `make task-list` |
| `task-show` | Prints a task document. | `make task-show TASK=api-add` |
| `task-run` | Runs the supervisor on a task file. | `make task-run TASK=api-add CONTEXT="beta branch"` |
| `task-verify` | Executes the named verification profile. | `make task-verify PROFILE=strict` |

### Reporting, backends, and verification profiles
| Target | Description | Example |
| --- | --- | --- |
| `report-show` | Shows the latest (or specific) report JSON. | `make report-show` |
| `backend-list` | Lists registered backends. | `make backend-list` |
| `backend-set` | Persists a backend override. | `make backend-set NAME=aider_cli` |
| `verification-set` | Persists a verification profile override. | `make verification-set PROFILE=default` |

### Agents, prompts, and skills
| Target | Description | Example |
| --- | --- | --- |
| `agent-list` | Prints built-in agent names. | `make agent-list` |
| `agent-set` | Enables/disables reviewer or verifier runtime agents. | `make agent-set AGENT=reviewer ENABLED=false` |
| `config-show` | Displays the effective runtime config summary. | `make config-show` |
| `prompt-show` | Prints a prompt file (use `PROMPT` var). | `make prompt-show PROMPT=supervisor` |
| `skill-list` | Lists available skill documents. | `make skill-list` |

## 7. Example scenarios
### Scenario 1 – Add a new API endpoint
1. Ensure Codex is the active backend: `make backend-set NAME=codex_cli`.
2. Author the task: `python -m scripts.ops task-init --task-id api-orders --title "Add POST /orders" --phase implementation --description "Expose POST..." --acceptance "Validates payload" --acceptance "Queues fulfillment" --backend codex_cli`.
3. Execute the task with business context: `make task-run TASK=api-orders CONTEXT="Sprint 8 new orders API"`.
4. Review the results: `make report-show`.

### Scenario 2 – Refactor a module using Aider
1. Prefer OpenRouter coding models: `export OPENROUTER_PREFERRED_MODELS="openrouter/qwen/qwen3-coder-next,openrouter/deepseek/deepseek-v3.2"`.
2. Pin Aider as the backend: `make backend-set NAME=aider_cli`.
3. Capture the refactor task: `python -m scripts.ops task-init --task-id refactor-ingest --title "Refactor ingest pipeline" --phase implementation --description "Split ingest.py into stages" --acceptance "No behavior regressions" --backend aider_cli`.
4. Run it with phase context: `make task-run TASK=refactor-ingest CONTEXT="Tech debt sprint"`.

### Scenario 3 – Run a full multi-phase project autonomously
1. Bootstrap the environment: `make setup PLAN_NAME=roadmap`.
2. Launch the orchestrator with a goal: `make run GOAL="Ship analytics MVP" CONTEXT="Q4 OKR"`.
3. Watch the streaming `[abracapocus][phase:*]` logs as each phase executes.
4. Inspect the final state and report: `make state-show` and `make report-show`.

### Scenario 4 – Debug a failing task using verification profiles
1. Upgrade verification rigor: `make verification-set PROFILE=strict`.
2. Re-run the suspect task: `make task-run TASK=api-orders`.
3. If the `verification` block in the report fails, re-run just the checks locally with `make task-verify PROFILE=strict`, fix the code/tests, and run the task again.

### Scenario 5 – Use human checkpoints for a sensitive production change
1. Enable checkpoints globally: `export HUMAN_CHECKPOINTS=true`.
2. (Optional) Mark specific phases by editing `plans/master.json` and setting `"human_checkpoint": true` on the relevant `PlanPhase`.
3. Run `make run GOAL="Patch billing bug" CONTEXT="hotfix"` and approve the prompt `Phase '<name>' completed. Confirm to continue.` after each phase.
4. Permanently record the change via `make report-show` and store the approval notes externally if required.

## 8. Human-in-the-loop checkpoints
- **Global toggle**: Set `HUMAN_CHECKPOINTS=true` (or `1/yes/on`) before running `make run` or `make task-run`. After each phase, the supervisor pauses with `[abracapocus] Human checkpoint: ...` and waits for Enter to resume.
- **Per-phase control**: Set `"human_checkpoint": true` or `false` on any `PlanPhase` in `plans/<version>.json`. The supervisor respects explicit per-phase settings even if the global toggle is off.
- LangGraph persists checkpoint state in `state/checkpoints.db`, so acknowledgments survive restarts—resume by re-running the original command and responding to the prompt.

## 9. Reading the output
- **Streaming terminal logs**: `_task_node` emits `[abracapocus][phase:<name>][task:<id>]` lines that show routing decisions, backend exit codes, and verification status. `_verification_node` reports `[abracapocus][verification:<phase>] status=...`. Human checkpoints print `[abracapocus] Human checkpoint: ...`.
- **Structured run output**: Commands such as `make run` first print `{"run_id": "...", "backend": "..."}` and then the full `OrchestrationReport` JSON. Each run automatically writes `reports/run-<uuid>.json`.
- **Viewing reports later**: `make report-show` prints the latest report (or pass `RUN_ID=<uuid>` to `python -m scripts.ops report-show --run-id <uuid>`). Inspect `backend_executions`, `review`, `verification`, and `metadata` sections to understand routing reasons and change summaries.
- **State traces**: `state/runtime_state.json` records active/default backends, overrides, completed phases, and run history so long-running programs can resume safely.

## 10. Troubleshooting
### Mock mode vs. real execution
- By default `DEEP_AGENT_MOCK_MODE=true`, so agent calls stub out LLM traffic and backends can still operate deterministically.
- To run against real Deep Agents, set `DEEP_AGENT_MOCK_MODE=false`, provide `DEEP_AGENT_MODEL` plus the necessary API keys, and ensure secrets are loaded in `.env`.

### Backend not found or dry-run only
- `CodingBackend` checks `shutil.which(executable)`; if the CLI is missing or `supports_direct_execution` is `False`, the orchestrator runs in dry-run mode and only logs the command and context JSON.
- Install the CLI, ensure it is on `PATH`, and rerun the task. For one-off overrides, run `BACKEND_OVERRIDE=codex_cli make run ...` to ensure a direct-capable backend is selected.

### Verification failures
- Failures appear in the `verification` section of the report and cause the phase status to be `failed`.
- Rerun the checks directly with `make task-verify PROFILE=<profile>` to reproduce locally, fix the offending code/tests, and rerun the task. Adjust the default profile (`make verification-set PROFILE=default`) if failures stem from an overly strict profile for exploratory work.

### Checkpoint database issues
- LangGraph stores resumable state in `state/checkpoints.db`. If a crash corrupts the SQLite file, stop the run, remove/rename the file (it will be recreated automatically), or run `make state-reset` to clear both runtime state and checkpoints.
- After clearing, rerun `make run` or `make task-run`—plans and task files remain untouched.

### OpenRouter model selection
- `runtime/router.select_openrouter_model` consults `OPENROUTER_PREFERRED_MODELS` first. Ensure the environment variable lists models present in `backends/openrouter_models.py`.
- When unset, the router chooses models based on task type tags (`coding`, `quick`, etc.). If the selected model is unavailable, set `OPENROUTER_PREFERRED_MODELS` or adjust your task’s `acceptance_criteria`/`phase` to influence routing heuristics.

With these workflows, abracapocus_2 can plan, execute, verify, and report on complex software efforts using whichever backend best fits each task.
