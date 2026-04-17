# Codex CLI Coding Instructions

- Operate non-interactively; shared header is loaded from `prompts/shared/non_interactive_header.md`.
- Use the `codex` CLI entrypoint.
- Accept task id, title, acceptance criteria, and context notes.
- Operate inside the repo root; respect `.gitignore` and local-first operation.
- Emit stdout/stderr suitable for deterministic review and verification.
