# Repo Inspection Skill

- **Purpose**: Walk the repository, summarize relevant files, detect constraints, and surface prior work.
- **Inputs**: target directories, focus areas, dependency hints.
- **Outputs**: `ContextPackage` entries describing files, summaries, and notes for downstream agents.
- **Usage**: Research agent uses this skill before any coding backend is invoked.
- **Future Work**: attach sandbox-aware shell commands (e.g., `rg`, `ls`, `git status`) using Deep Agents filesystem tools.
