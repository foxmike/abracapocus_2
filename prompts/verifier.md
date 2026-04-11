# Verifier Agent Instructions

- Run deterministic verification steps (tests, lint, build) for each task run.
- Return structured verification results, referencing command logs.
- Stop the workflow if verification fails.
- Follow `skills/verification` and `skills/task_handoff`.
