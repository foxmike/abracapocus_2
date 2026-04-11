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

The Makefile exposes a complete operator surface: install/setup, project tree, running orchestration, initializing/showing plans/phases/tasks, backend/agent introspection, state management, and deterministic verification hooks. These commands all delegate to Python scripts for composability and future automation.

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
