# Architecture Overview

abracapocus_2 is a supervisor-led LangChain Deep Agents system that keeps each component visible and configurable.

## Components

- **Supervisor (`orchestrator/supervisor.py`)**: central orchestrator, wires all specialist agents, routing, and persistence.
- **Planning Agent (`agents/planning_agent.py`)**: transforms a project request into a multi-phase plan using planning + phase progression skills.
- **Research Agent (`agents/research_agent.py`)**: inspects the repo, collects documentation/code files, and emits context packages.
- **Management Agent (`agents/management_agent.py`)**: maintains JSON-backed runtime state, plan versions, task registry, and execution history.
- **Reviewer Agent (`agents/reviewer_agent.py`)**: performs structured code review on backend outputs.
- **Verifier Agent (`agents/verifier_agent.py`)**: runs deterministic checks (e.g., py_compile) and stores verification reports.
- **Coding backends (`backends/*.py`)**: CLI adapters for Codex, Claude Code, Gemini, and Aider. Each defines command contracts, expected executables, timeout handling, and structured results.
- **Routing (`runtime/router.py`)**: policy layer supporting manual, rules-based, and auto routing strategies.
- **State + persistence (`runtime/state_store.py`)**: JSON state file + reports directory for reproducibility.

## Deep Agents integration

`runtime/deep_agent_factory.py` loads `create_deep_agent(...)` when LangChain Deep Agents + an LLM are available. In offline/mock mode, agents receive a deterministic `LocalDeepAgent` runner so unit tests succeed without credentials. The prompts under `prompts/` and the skills under `skills/` map directly to the Deep Agents concepts of instructions and skills.

## Data flow

1. **Request intake** – `main.py` captures CLI arguments and instantiates `ProjectRequest`.
2. **Planning** – planning agent generates `Plan` models (phases + tasks).
3. **Context** – research agent scans repo, builds `ContextPackage`.
4. **State Sync** – management agent writes plan + tasks to `state/runtime_state.json`.
5. **Routing** – router selects backend, referencing `config.py` + runtime state.
6. **Execution** – backend adapter constructs CLI command and (currently) simulates execution for deterministic results.
7. **Review** – reviewer consumes backend output and emits `ReviewReport`.
8. **Verification** – verifier runs deterministic command(s) and emits `VerificationReport`.
9. **Persistence** – management agent records run metadata; orchestrator saves `reports/run-<id>.json`.

## Filesystem layout

```
orchestrator/        Supervisor orchestration code
agents/             Specialist agents bound to Deep Agents prompts/skills
backends/           CLI coding backend adapters + registry
runtime/            Deep Agent factory, router, state store, logging
models/             Typed models for plans, tasks, reports, and state
plans/, phases/, tasks/, reports/  Documentation/state directories
scripts/            Operator scripts for plan/task/state maintenance
docs/               Architecture + operations guides
```

## Extensibility hooks

- Add new skills/prompt files to update agent behavior without touching Python.
- Register new CLI backends and extend `runtime/router.py` for richer routing policies.
- Swap `DeepAgentSettings.mock_mode` to `false` and provide credentials to run real Deep Agents.
- Expand `VerifierAgent` with real build/test/lint flows for production readiness.
