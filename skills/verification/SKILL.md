# Verification Skill

- **Purpose**: Run deterministic tests/builds/lints and summarize the outcomes.
- **Inputs**: verification profiles, command lists, backend execution metadata.
- **Outputs**: `VerificationReport` entries with per-check status.
- **Usage**: Verifier agent consumes this skill to plan/rerun verification suites.
- **Future Work**: add configurable verification profiles, multi-backend support, and hooks into CI pipelines.
