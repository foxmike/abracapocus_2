# Extensibility Guide

## Deep Agents

- Update `skills/` markdown files to document new skills and wiring expectations.
- Create new prompt files under `prompts/` for additional agents or backend personas.
- Set `DEEP_AGENT_MOCK_MODE=false` + credentials to switch from the deterministic fallback to real Deep Agents.

## Additional agents

Add a new agent module under `agents/`, register it inside `orchestrator/supervisor.py`, and provide prompt + skills. Use `BaseAgent` + `DeepAgentFactory` to guarantee compatibility.

## Coding backend integrations

1. Subclass `CodingBackend`.
2. Implement `build_command` to emit the CLI invocation.
3. Register the backend in `backends/registry.py`.
4. Update `Makefile`/docs if operational commands change.

## Routing policies

`BackendRouter` exposes `_rules_based` and `_auto_placeholder`. Extend or replace these methods, or integrate telemetry-driven decisions by consuming execution history from `state/runtime_state.json`.

## Verification

`VerifierAgent.verify` currently runs `py_compile`. Replace or augment `_compile_check` with your real verification commands (tests, linters, builds). Add new Makefile targets to run those checks in isolation.

## Multi-machine orchestration

The JSON state format includes operator overrides and can be extended with connection metadata. Introduce new runtime modules under `runtime/` for RPC/queue management when you're ready to scale beyond a single machine.
