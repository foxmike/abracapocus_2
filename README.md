# abracapocus_2

A production-ready scaffold for a local-first LangChain Deep Agents orchestration system purpose-built for large autonomous software efforts. The project wires a supervisor-led multi-agent workflow that can ingest project briefs, create and manage multi-phase plans, route coding work across CLI backends, perform review and verification, and persist structured state for long-lived initiatives.

## Why Deep Agents

LangChain Deep Agents provide sandbox-aware execution, sub-agent coordination, reusable skills, and deterministic routing hooks. This repository keeps Deep Agents visible—`runtime/deep_agent_factory.py` loads `create_deep_agent(...)` when available and falls back to a deterministic local runner for offline development. Every specialist agent class binds to Deep Agents instructions and skills under `prompts/` and `skills/`, so swapping to a real LLM + Deep Agent runtime takes a configuration change rather than an architecture rewrite.

## High-level architecture

- **Supervisor orchestrator** (`orchestrator/supervisor.py`): accepts project requests, coordinates planning, research, management, backend routing, review, and verification, and emits structured reports.
- **Specialist agents** (`agents/`): planning, research, management, reviewer, and verifier agents each load Deep Agent instructions and expose typed methods that operate on shared models.
- **Coding backends** (`backends/`): adapters for Codex CLI, Claude Code CLI, Gemini CLI, and Aider CLI share a deterministic contract (`CodingBackend`), perform subprocess-ready command construction, and emit structured execution records. They currently simulate execution while capturing stdout/stderr/exit codes for traceability.
- **Routing + state** (`runtime/`): configuration, backend routing policies, Deep Agent loading, logging, and JSON-backed state persistence live here. Routing supports manual overrides, rule-based selection, and metadata for future model-assisted choices.
- **Models + documents** (`models/`, `plans/`, `phases/`, `tasks/`, `reports/`): strongly typed Pydantic models describe project requests, plans, tasks, execution history, reviews, and verification results. The filesystem mirrors those constructs so long-lived projects can accumulate documentation.
- **Operational surface** (`Makefile`, `scripts/ops.py`, `docs/`): a Makefile-first workflow exposes install, run, demo, plan/task management, backend selection, state inspection, and documentation helpers.

The scaffold already runs an end-to-end flow (`python main.py`) that:
1. Accepts a project request.
2. Builds a multi-phase plan via the planning agent.
3. Gathers current repo context via the research agent.
4. Registers the run through the management agent and state store.
5. Selects a coding backend via the routing policy and executes the task.
6. Runs reviewer and verifier agents to produce structured findings.
7. Persists an orchestration report under `reports/` and updates state for future iterations.

## Repository map

| Path | Purpose |
| --- | --- |
| `main.py` | Typer CLI entrypoint for running orchestration flows and quick demos. |
| `config.py` | Runtime configuration loader (env + defaults) for agents, routing, and persistence. |
| `orchestrator/` | Supervisor orchestration logic, including demo utilities and result serialization. |
| `agents/` | Specialist Deep Agent wrappers: planning, research, management, reviewer, verifier. |
| `backends/` | CLI backend adapters plus registry and execution result types. |
| `runtime/` | Deep Agent factory, router, logging helpers, and JSON-based state store. |
| `models/` | Typed data models for requests, plans, tasks, reports, and runtime state. |
| `skills/` | Deep Agents-aligned skill definitions with contracts and usage guidance. |
| `prompts/` | Instruction sets for supervisor, subagents, and coding backends. |
| `plans/`, `phases/`, `tasks/`, `reports/`, `state/` | File-backed documentation + state for real multi-phase projects. |
| `scripts/` | Operational scripts used by the Makefile (state tools, plan/task helpers, project tree). |
| `docs/` | Human-facing documentation for architecture, operations, routing, and extension paths. |
| `tests/` | Pytest suite covering orchestration flow, routing, backend adapters, and models. |

## Getting started

1. **Install dependencies**
   ```bash
   make install
   ```
2. **Run verification + tests**
   ```bash
   make test
   ```
3. **Run the demo orchestration**
   ```bash
   make demo
   ```
4. **Inspect runtime state**
   ```bash
   make state-show
   ```

## Deep Agents prompts and skills

Each agent loads instructions from `prompts/<role>.md` and a relevant set of skills under `skills/`. Skills document inputs, outputs, and extension notes so new Deep Agent actions can be created without code surgery. Supervisor, planning, research, management, reviewer, verifier, and every coding backend have dedicated prompt files that operators can iterate on without editing Python.

## Operational commands

The Makefile exposes a complete operator surface backed by `python -m scripts.ops`, so every target performs the documented action:

| Target | Description |
| --- | --- |
| `make run GOAL="..." CONTEXT="..."` | Run orchestration for an arbitrary goal. |
| `make demo` | Execute the demo orchestration. |
| `make test` | Run the pytest suite. |
| `make state-show` / `make state-reset` | Inspect or reset the JSON runtime state. |
| `make backend-list` / `make backend-set NAME=codex_cli` | List or override the active backend (stored in runtime state). |
| `make verification-set PROFILE=strict` | Override the verification profile used for all runs. |
| `make plan-show PLAN_NAME=master` / `make phase-show PHASE=phase-1` | Print stored plan/phase JSON. |
| `make task-list` / `make task-show TASK=build-widget` | List or inspect task documents. |
| `make task-run TASK=build-widget CONTEXT="bugfix"` | Run a specific task document through the supervisor. |
| `make task-verify PROFILE=strict` | Execute the configured verification profile (defaults to the active profile). |
| `make agent-set AGENT=reviewer ENABLED=false` | Enable/disable reviewer or verifier agents at runtime. |
| `make report-show` | Print the latest orchestration report. |
| `make config-show` | Display the effective runtime configuration. |

Additional helpers (`install`, `setup`, `docs`, `tree`, `prompt-show`, `skill-list`, etc.) remain available for day-to-day development.

### Verification profiles

Verification commands are grouped into named profiles:

- **minimal** – `python -m py_compile main.py`
- **default** – py_compile + `python scripts/selfcheck.py`
- **strict** – py_compile + `pytest -q` + `pytest -q --maxfail=1`

Set the default profile at runtime with `make verification-set PROFILE=strict` (stored in `state/runtime_state.json`). Tasks can override the default by setting `verification_profile` in their `TaskDocument`; the verifier resolves the task’s profile first, then falls back to the runtime default. Reports include `verification.profile`, so each run records the profile that was executed.

### Demo self-improvement

Running `python main.py demo` now performs a real, deterministic self-improvement task:

1. Planning agent seeds a plan that includes the demo task.
2. The `demo_cli` backend runs `scripts/demo_improvement.py`, which refreshes `docs/demo_status.md` with an entry for the current run.
3. Reviewer/verifier agents evaluate the run; verification executes `python -m py_compile main.py` and `python scripts/selfcheck.py` to ensure the log exists.
4. The resulting report captures changed files, the diff summary, and the change assessment block so operators can audit what happened.

## Extending the system

- Add new coding backends by subclassing `CodingBackend` and registering them in `backends/registry.py`.
- Define new skills or update instructions by editing the markdown files under `skills/` and `prompts/`.
- Integrate real LangChain Deep Agents by installing the official packages, supplying LLM credentials (see `.env.example`), and disabling mock mode in `config.py` or environment variables.
- Expand verification by extending `VerifierAgent` and wiring additional Makefile targets that call your real test/lint/build suites.
- Scale orchestration by adding new management hooks, multi-machine runners, or routing policies in `runtime/router.py`.

## Documentation

See the `docs/` directory for architecture diagrams, operational procedures, planning/task workflows, backend/routing references, and extension notes.

## Status

This is a first production-quality scaffold: real models, deterministic flow, and documented contracts exist today, while live LLM + CLI tool execution is intentionally stubbed until secure credentials and target environments are available.
