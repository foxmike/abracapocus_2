# Planning Skill

- **Purpose**: Translate project goals into multi-phase software plans with measurable tasks and acceptance criteria.
- **Inputs**: project goal, constraints, prior plan context, operator guidance.
- **Outputs**: structured `Plan` data (phases, tasks, dependencies) persisted to `plans/` and runtime state.
- **Usage**: Bound to the planning agent along with `skills/phase_progression`. Agents consuming this skill must emit deterministic JSON or bullet plans that `agents/planning_agent.py` can parse.
- **Future Work**: integrate Deep Agents file-system tools for referencing prior phases and editing plan documents directly.
