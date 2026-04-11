# Coding Backends and Routing

## Backend adapters

| Name | Module | Executable | Description |
| --- | --- | --- | --- |
| `codex_cli` | `backends/codex_cli.py` | `codex` | CLI interface for OpenAI Codex-style coding agent. |
| `claude_code_cli` | `backends/claude_code_cli.py` | `claude-code` | Adapter for Anthropic Claude Code CLI workflows (not managed agents). |
| `gemini_cli` | `backends/gemini_cli.py` | `gemini` | Adapter for Google Gemini coding tools. |
| `aider_cli` | `backends/aider_cli.py` | `aider` | Adapter for Aider CLI pair-programming flows. |

Each backend inherits from `CodingBackend` and must implement `build_command(...)`. `execute(...)` already handles deterministic simulation vs. real subprocess execution. All adapters load dedicated prompts under `prompts/` to instruct downstream Deep Agents or CLI wrappers.

## Registry

`backends/registry.py` keeps a simple registry, enabling runtime discovery (`make backend-list`) and selection. Additions only require appending to that registry with a new descriptor.

## Routing policies

`runtime/router.py` implements manual, rules-based, and placeholder auto modes:
- **Manual**: respect `BACKEND_OVERRIDE` when set.
- **Rules**: route by task title/phase (e.g., refactors -> `aider_cli`).
- **Auto**: use heuristics on acceptance criteria counts for now; later can integrate with Deep Agents or telemetry-driven models.

The routing decision is saved into orchestration metadata and can be inspected after the fact.
