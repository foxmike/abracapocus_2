# Coding Standards Skill

- **Purpose**: Enforce architecture constraints, naming, and review guidelines for generated code.
- **Inputs**: backend execution outputs, plan intent, coding policies.
- **Outputs**: structured review findings with severity/location/detail.
- **Usage**: Reviewer agent uses this skill plus `skills/change_assessment` to produce deterministic review data.
- **Future Work**: integrate lint/build outputs and repo-specific guardrails.
