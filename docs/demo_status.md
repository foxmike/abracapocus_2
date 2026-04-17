# Demo Self-Improvement Log

This file is updated automatically when `python main.py demo` runs.

## Run bootstrap
- Task ID: bootstrap
- Title: Initial demo status
- Phase: implementation
- Goal: Seed log for future demo runs
## Run 2026-04-12T19:15:33
- Task ID: demo-self-improve
- Title: Refresh demo status log
- Phase: implementation
- Goal: Update docs/demo_status.md with the latest demo guidance
- Context: Collected 25 documentation/code files
## Run 2026-04-12T19:18:58
- Task ID: demo-self-improve
- Title: Refresh demo status log
- Phase: implementation
- Goal: Update docs/demo_status.md with the latest demo guidance
- Context: Collected 25 documentation/code files
## Run 2026-04-12T19:21:34
- Task ID: demo-self-improve
- Title: Refresh demo status log
- Phase: implementation
- Goal: Update docs/demo_status.md with the latest demo guidance
- Context: Collected 25 documentation/code files
## Run 2026-04-12T19:22:30
- Task ID: demo-self-improve
- Title: Refresh demo status log
- Phase: implementation
- Goal: Update docs/demo_status.md with the latest demo guidance
- Context: Collected 25 documentation/code files
## Run 2026-04-12T19:23:01
- Task ID: demo-self-improve
- Title: Refresh demo status log
- Phase: implementation
- Goal: Update docs/demo_status.md with the latest demo guidance
- Context: Collected 25 documentation/code files
## Run 2026-04-12T19:25:53
- Task ID: demo-self-improve
- Title: Refresh demo status log
- Phase: implementation
- Goal: Update docs/demo_status.md with the latest demo guidance
- Context: Collected 25 documentation/code files
## Run 2026-04-12T19:28:05
- Task ID: demo-self-improve
- Title: Refresh demo status log
- Phase: implementation
- Goal: Update docs/demo_status.md with the latest demo guidance
- Context: Collected 25 documentation/code files
## Run 2026-04-12T19:33:09
- Task ID: demo-self-improve
- Title: Refresh demo status log
- Phase: implementation
- Goal: Update docs/demo_status.md with the latest demo guidance
- Context: Collected 25 documentation/code files
## Run 2026-04-12T19:33:41
- Task ID: demo-self-improve
- Title: Refresh demo status log
- Phase: implementation
- Goal: Update docs/demo_status.md with the latest demo guidance
- Context: Collected 25 documentation/code files
## Run 2026-04-12T19:38:55
- Task ID: demo-self-improve
- Title: Refresh demo status log
- Phase: implementation
- Goal: Update docs/demo_status.md with the latest demo guidance
- Context: Collected 25 documentation/code files
## Run 2026-04-16T20:08:46
- Task ID: demo-self-improve
- Title: Refresh demo status log
- Phase: implementation
- Goal: Update docs/demo_status.md with the latest demo guidance
- Context: Collected 8 semantically relevant files; AGENTS.md guidance:
# AGENTS.md
## Purpose
This repository is operated by an autonomous multi-agent system (abracapocus_2).
All agents must follow these rules when modifying the codebase.
---
## Core Principles
- Minimal blast radius: only modify what is required for the task
- Deterministic verification: all changes must be verifiable via code (tests, compile, scripts)
- No architecture drift: do not introduce new frameworks or major design changes unless explicitly required
- No unrelated refactors
- All changes must be reproducible from a clean clone
---
## Project Structure
- docs/ → design, plans, architecture constraints
- plans/ → master plans
- phases/ → phase definitions
- tasks/ → executable task documents
- backends/ → CLI backend adapters
- agents/ → specialist agents
- runtime/ → orchestration, routing, state
...(truncated)

AGENTS.md guidance:
# AGENTS.md

## Purpose

This repository is operated by an autonomous multi-agent system (abracapocus_2).
All agents must follow these rules when modifying the codebase.

---

## Core Principles

- Minimal blast radius: only modify what is required for the task
- Deterministic verification: all changes must be verifiable via code (tests, compile, scripts)
- No architecture drift: do not introduce new frameworks or major design changes unless explicitly required
- No unrelated refactors
- All changes must be reproducible from a clean clone

---

## Project Structure

- docs/ → design, plans, architecture constraints
- plans/ → master plans
- phases/ → phase definitions
- tasks/ → executable task documents
- backends/ → CLI backend adapters
- agents/ → specialist agents
- runtime/ → orchestration, routing, state
- reports/ → execution reports (DO NOT MODIFY MANUALLY)
- state/runtime_state.json → runtime state (DO NOT COMMIT)

---

## Task Execution Rules

- Always operate from a task document when available
- Respect:
  - selected_backend
  - verification_profile
  - acceptance_criteria
- If a task conflicts with architecture constraints or phase scope:
  - STOP and report conflict

---

## Backend Rules

- Backends must:
  - execute commands deterministically
  - capture stdout, stderr, exit_code
  - not silently fail
- Do not invent backend interfaces; use existing adapters
- Codex CLI, Aider, Gemini, Claude Code should be invoked through backends only

---

## Verification Rules

- Verification must be deterministic
- Preferred checks:
  - pytest
  - python -m py_compile
- Do not rely on model self-evaluation

---

## Git Rules

- Do not commit:
  - runtime_state.json
  - reports/
  - logs/
  - virtual environments
- Do not modify .gitignore unless required by task
- Do not create excessive commits; prefer grouped logical commits

---

## Allowed Changes

- Implement task requirements
- Fix failing verification
- Update relevant tests
- Improve documentation tied to the task

---

## Forbidden Changes

- Changing architecture without explicit instruction
- Adding dependencies without justification
- Modifying unrelated files
- Deleting important files
- Bypassing verification

---

## Planning Rules

- Plans are multi-phase
- Completed sections are immutable
- Remaining sections may be updated
- Tasks must align with:
  - project brief
  - architecture constraints
  - active phase

---

## Reporting

- All executions must produce structured reports
- Reports must include:
  - changed files
  - verification results
  - assessment

---

## Behavior

- Do not ask unnecessary questions
- Do not stall execution
- Do not perform broad scans unless required
- Prefer direct action over analysis

---

## Priority Order

1. Architecture constraints
2. Task definition
3. Verification results
4. Plan guidance

If conflicts occur, follow this order.

## Run 2026-04-16T20:09:11
- Task ID: demo-self-improve
- Title: Refresh demo status log
- Phase: implementation
- Goal: Update docs/demo_status.md with the latest demo guidance
- Context: Collected 4 semantically relevant files; AGENTS.md guidance:
# AGENTS.md
## Purpose
This repository is operated by an autonomous multi-agent system (abracapocus_2).
All agents must follow these rules when modifying the codebase.
---
## Core Principles
- Minimal blast radius: only modify what is required for the task
- Deterministic verification: all changes must be verifiable via code (tests, compile, scripts)
- No architecture drift: do not introduce new frameworks or major design changes unless explicitly required
- No unrelated refactors
- All changes must be reproducible from a clean clone
---
## Project Structure
- docs/ → design, plans, architecture constraints
- plans/ → master plans
- phases/ → phase definitions
- tasks/ → executable task documents
- backends/ → CLI backend adapters
- agents/ → specialist agents
- runtime/ → orchestration, routing, state
...(truncated)

AGENTS.md guidance:
# AGENTS.md

## Purpose

This repository is operated by an autonomous multi-agent system (abracapocus_2).
All agents must follow these rules when modifying the codebase.

---

## Core Principles

- Minimal blast radius: only modify what is required for the task
- Deterministic verification: all changes must be verifiable via code (tests, compile, scripts)
- No architecture drift: do not introduce new frameworks or major design changes unless explicitly required
- No unrelated refactors
- All changes must be reproducible from a clean clone

---

## Project Structure

- docs/ → design, plans, architecture constraints
- plans/ → master plans
- phases/ → phase definitions
- tasks/ → executable task documents
- backends/ → CLI backend adapters
- agents/ → specialist agents
- runtime/ → orchestration, routing, state
- reports/ → execution reports (DO NOT MODIFY MANUALLY)
- state/runtime_state.json → runtime state (DO NOT COMMIT)

---

## Task Execution Rules

- Always operate from a task document when available
- Respect:
  - selected_backend
  - verification_profile
  - acceptance_criteria
- If a task conflicts with architecture constraints or phase scope:
  - STOP and report conflict

---

## Backend Rules

- Backends must:
  - execute commands deterministically
  - capture stdout, stderr, exit_code
  - not silently fail
- Do not invent backend interfaces; use existing adapters
- Codex CLI, Aider, Gemini, Claude Code should be invoked through backends only

---

## Verification Rules

- Verification must be deterministic
- Preferred checks:
  - pytest
  - python -m py_compile
- Do not rely on model self-evaluation

---

## Git Rules

- Do not commit:
  - runtime_state.json
  - reports/
  - logs/
  - virtual environments
- Do not modify .gitignore unless required by task
- Do not create excessive commits; prefer grouped logical commits

---

## Allowed Changes

- Implement task requirements
- Fix failing verification
- Update relevant tests
- Improve documentation tied to the task

---

## Forbidden Changes

- Changing architecture without explicit instruction
- Adding dependencies without justification
- Modifying unrelated files
- Deleting important files
- Bypassing verification

---

## Planning Rules

- Plans are multi-phase
- Completed sections are immutable
- Remaining sections may be updated
- Tasks must align with:
  - project brief
  - architecture constraints
  - active phase

---

## Reporting

- All executions must produce structured reports
- Reports must include:
  - changed files
  - verification results
  - assessment

---

## Behavior

- Do not ask unnecessary questions
- Do not stall execution
- Do not perform broad scans unless required
- Prefer direct action over analysis

---

## Priority Order

1. Architecture constraints
2. Task definition
3. Verification results
4. Plan guidance

If conflicts occur, follow this order.

## Run 2026-04-16T20:09:27
- Task ID: demo-self-improve
- Title: Refresh demo status log
- Phase: implementation
- Goal: Update docs/demo_status.md with the latest demo guidance
- Context: Collected 5 semantically relevant files; AGENTS.md guidance:
# AGENTS.md
## Purpose
This repository is operated by an autonomous multi-agent system (abracapocus_2).
All agents must follow these rules when modifying the codebase.
---
## Core Principles
- Minimal blast radius: only modify what is required for the task
- Deterministic verification: all changes must be verifiable via code (tests, compile, scripts)
- No architecture drift: do not introduce new frameworks or major design changes unless explicitly required
- No unrelated refactors
- All changes must be reproducible from a clean clone
---
## Project Structure
- docs/ → design, plans, architecture constraints
- plans/ → master plans
- phases/ → phase definitions
- tasks/ → executable task documents
- backends/ → CLI backend adapters
- agents/ → specialist agents
- runtime/ → orchestration, routing, state
...(truncated)

AGENTS.md guidance:
# AGENTS.md

## Purpose

This repository is operated by an autonomous multi-agent system (abracapocus_2).
All agents must follow these rules when modifying the codebase.

---

## Core Principles

- Minimal blast radius: only modify what is required for the task
- Deterministic verification: all changes must be verifiable via code (tests, compile, scripts)
- No architecture drift: do not introduce new frameworks or major design changes unless explicitly required
- No unrelated refactors
- All changes must be reproducible from a clean clone

---

## Project Structure

- docs/ → design, plans, architecture constraints
- plans/ → master plans
- phases/ → phase definitions
- tasks/ → executable task documents
- backends/ → CLI backend adapters
- agents/ → specialist agents
- runtime/ → orchestration, routing, state
- reports/ → execution reports (DO NOT MODIFY MANUALLY)
- state/runtime_state.json → runtime state (DO NOT COMMIT)

---

## Task Execution Rules

- Always operate from a task document when available
- Respect:
  - selected_backend
  - verification_profile
  - acceptance_criteria
- If a task conflicts with architecture constraints or phase scope:
  - STOP and report conflict

---

## Backend Rules

- Backends must:
  - execute commands deterministically
  - capture stdout, stderr, exit_code
  - not silently fail
- Do not invent backend interfaces; use existing adapters
- Codex CLI, Aider, Gemini, Claude Code should be invoked through backends only

---

## Verification Rules

- Verification must be deterministic
- Preferred checks:
  - pytest
  - python -m py_compile
- Do not rely on model self-evaluation

---

## Git Rules

- Do not commit:
  - runtime_state.json
  - reports/
  - logs/
  - virtual environments
- Do not modify .gitignore unless required by task
- Do not create excessive commits; prefer grouped logical commits

---

## Allowed Changes

- Implement task requirements
- Fix failing verification
- Update relevant tests
- Improve documentation tied to the task

---

## Forbidden Changes

- Changing architecture without explicit instruction
- Adding dependencies without justification
- Modifying unrelated files
- Deleting important files
- Bypassing verification

---

## Planning Rules

- Plans are multi-phase
- Completed sections are immutable
- Remaining sections may be updated
- Tasks must align with:
  - project brief
  - architecture constraints
  - active phase

---

## Reporting

- All executions must produce structured reports
- Reports must include:
  - changed files
  - verification results
  - assessment

---

## Behavior

- Do not ask unnecessary questions
- Do not stall execution
- Do not perform broad scans unless required
- Prefer direct action over analysis

---

## Priority Order

1. Architecture constraints
2. Task definition
3. Verification results
4. Plan guidance

If conflicts occur, follow this order.

## Run 2026-04-16T20:11:06
- Task ID: demo-self-improve
- Title: Refresh demo status log
- Phase: implementation
- Goal: Update docs/demo_status.md with the latest demo guidance
- Context: Collected 6 semantically relevant files; AGENTS.md guidance:
# AGENTS.md
## Purpose
This repository is operated by an autonomous multi-agent system (abracapocus_2).
All agents must follow these rules when modifying the codebase.
---
## Core Principles
- Minimal blast radius: only modify what is required for the task
- Deterministic verification: all changes must be verifiable via code (tests, compile, scripts)
- No architecture drift: do not introduce new frameworks or major design changes unless explicitly required
- No unrelated refactors
- All changes must be reproducible from a clean clone
---
## Project Structure
- docs/ → design, plans, architecture constraints
- plans/ → master plans
- phases/ → phase definitions
- tasks/ → executable task documents
- backends/ → CLI backend adapters
- agents/ → specialist agents
- runtime/ → orchestration, routing, state
...(truncated)

AGENTS.md guidance:
# AGENTS.md

## Purpose

This repository is operated by an autonomous multi-agent system (abracapocus_2).
All agents must follow these rules when modifying the codebase.

---

## Core Principles

- Minimal blast radius: only modify what is required for the task
- Deterministic verification: all changes must be verifiable via code (tests, compile, scripts)
- No architecture drift: do not introduce new frameworks or major design changes unless explicitly required
- No unrelated refactors
- All changes must be reproducible from a clean clone

---

## Project Structure

- docs/ → design, plans, architecture constraints
- plans/ → master plans
- phases/ → phase definitions
- tasks/ → executable task documents
- backends/ → CLI backend adapters
- agents/ → specialist agents
- runtime/ → orchestration, routing, state
- reports/ → execution reports (DO NOT MODIFY MANUALLY)
- state/runtime_state.json → runtime state (DO NOT COMMIT)

---

## Task Execution Rules

- Always operate from a task document when available
- Respect:
  - selected_backend
  - verification_profile
  - acceptance_criteria
- If a task conflicts with architecture constraints or phase scope:
  - STOP and report conflict

---

## Backend Rules

- Backends must:
  - execute commands deterministically
  - capture stdout, stderr, exit_code
  - not silently fail
- Do not invent backend interfaces; use existing adapters
- Codex CLI, Aider, Gemini, Claude Code should be invoked through backends only

---

## Verification Rules

- Verification must be deterministic
- Preferred checks:
  - pytest
  - python -m py_compile
- Do not rely on model self-evaluation

---

## Git Rules

- Do not commit:
  - runtime_state.json
  - reports/
  - logs/
  - virtual environments
- Do not modify .gitignore unless required by task
- Do not create excessive commits; prefer grouped logical commits

---

## Allowed Changes

- Implement task requirements
- Fix failing verification
- Update relevant tests
- Improve documentation tied to the task

---

## Forbidden Changes

- Changing architecture without explicit instruction
- Adding dependencies without justification
- Modifying unrelated files
- Deleting important files
- Bypassing verification

---

## Planning Rules

- Plans are multi-phase
- Completed sections are immutable
- Remaining sections may be updated
- Tasks must align with:
  - project brief
  - architecture constraints
  - active phase

---

## Reporting

- All executions must produce structured reports
- Reports must include:
  - changed files
  - verification results
  - assessment

---

## Behavior

- Do not ask unnecessary questions
- Do not stall execution
- Do not perform broad scans unless required
- Prefer direct action over analysis

---

## Priority Order

1. Architecture constraints
2. Task definition
3. Verification results
4. Plan guidance

If conflicts occur, follow this order.

## Run 2026-04-16T20:11:44
- Task ID: demo-self-improve
- Title: Refresh demo status log
- Phase: implementation
- Goal: Update docs/demo_status.md with the latest demo guidance
- Context: Collected 3 semantically relevant files; AGENTS.md guidance:
# AGENTS.md
## Purpose
This repository is operated by an autonomous multi-agent system (abracapocus_2).
All agents must follow these rules when modifying the codebase.
---
## Core Principles
- Minimal blast radius: only modify what is required for the task
- Deterministic verification: all changes must be verifiable via code (tests, compile, scripts)
- No architecture drift: do not introduce new frameworks or major design changes unless explicitly required
- No unrelated refactors
- All changes must be reproducible from a clean clone
---
## Project Structure
- docs/ → design, plans, architecture constraints
- plans/ → master plans
- phases/ → phase definitions
- tasks/ → executable task documents
- backends/ → CLI backend adapters
- agents/ → specialist agents
- runtime/ → orchestration, routing, state
...(truncated)

AGENTS.md guidance:
# AGENTS.md

## Purpose

This repository is operated by an autonomous multi-agent system (abracapocus_2).
All agents must follow these rules when modifying the codebase.

---

## Core Principles

- Minimal blast radius: only modify what is required for the task
- Deterministic verification: all changes must be verifiable via code (tests, compile, scripts)
- No architecture drift: do not introduce new frameworks or major design changes unless explicitly required
- No unrelated refactors
- All changes must be reproducible from a clean clone

---

## Project Structure

- docs/ → design, plans, architecture constraints
- plans/ → master plans
- phases/ → phase definitions
- tasks/ → executable task documents
- backends/ → CLI backend adapters
- agents/ → specialist agents
- runtime/ → orchestration, routing, state
- reports/ → execution reports (DO NOT MODIFY MANUALLY)
- state/runtime_state.json → runtime state (DO NOT COMMIT)

---

## Task Execution Rules

- Always operate from a task document when available
- Respect:
  - selected_backend
  - verification_profile
  - acceptance_criteria
- If a task conflicts with architecture constraints or phase scope:
  - STOP and report conflict

---

## Backend Rules

- Backends must:
  - execute commands deterministically
  - capture stdout, stderr, exit_code
  - not silently fail
- Do not invent backend interfaces; use existing adapters
- Codex CLI, Aider, Gemini, Claude Code should be invoked through backends only

---

## Verification Rules

- Verification must be deterministic
- Preferred checks:
  - pytest
  - python -m py_compile
- Do not rely on model self-evaluation

---

## Git Rules

- Do not commit:
  - runtime_state.json
  - reports/
  - logs/
  - virtual environments
- Do not modify .gitignore unless required by task
- Do not create excessive commits; prefer grouped logical commits

---

## Allowed Changes

- Implement task requirements
- Fix failing verification
- Update relevant tests
- Improve documentation tied to the task

---

## Forbidden Changes

- Changing architecture without explicit instruction
- Adding dependencies without justification
- Modifying unrelated files
- Deleting important files
- Bypassing verification

---

## Planning Rules

- Plans are multi-phase
- Completed sections are immutable
- Remaining sections may be updated
- Tasks must align with:
  - project brief
  - architecture constraints
  - active phase

---

## Reporting

- All executions must produce structured reports
- Reports must include:
  - changed files
  - verification results
  - assessment

---

## Behavior

- Do not ask unnecessary questions
- Do not stall execution
- Do not perform broad scans unless required
- Prefer direct action over analysis

---

## Priority Order

1. Architecture constraints
2. Task definition
3. Verification results
4. Plan guidance

If conflicts occur, follow this order.

## Run 2026-04-16T20:12:03
- Task ID: demo-self-improve
- Title: Refresh demo status log
- Phase: implementation
- Goal: Update docs/demo_status.md with the latest demo guidance
- Context: Collected 6 semantically relevant files; AGENTS.md guidance:
# AGENTS.md
## Purpose
This repository is operated by an autonomous multi-agent system (abracapocus_2).
All agents must follow these rules when modifying the codebase.
---
## Core Principles
- Minimal blast radius: only modify what is required for the task
- Deterministic verification: all changes must be verifiable via code (tests, compile, scripts)
- No architecture drift: do not introduce new frameworks or major design changes unless explicitly required
- No unrelated refactors
- All changes must be reproducible from a clean clone
---
## Project Structure
- docs/ → design, plans, architecture constraints
- plans/ → master plans
- phases/ → phase definitions
- tasks/ → executable task documents
- backends/ → CLI backend adapters
- agents/ → specialist agents
- runtime/ → orchestration, routing, state
...(truncated)

AGENTS.md guidance:
# AGENTS.md

## Purpose

This repository is operated by an autonomous multi-agent system (abracapocus_2).
All agents must follow these rules when modifying the codebase.

---

## Core Principles

- Minimal blast radius: only modify what is required for the task
- Deterministic verification: all changes must be verifiable via code (tests, compile, scripts)
- No architecture drift: do not introduce new frameworks or major design changes unless explicitly required
- No unrelated refactors
- All changes must be reproducible from a clean clone

---

## Project Structure

- docs/ → design, plans, architecture constraints
- plans/ → master plans
- phases/ → phase definitions
- tasks/ → executable task documents
- backends/ → CLI backend adapters
- agents/ → specialist agents
- runtime/ → orchestration, routing, state
- reports/ → execution reports (DO NOT MODIFY MANUALLY)
- state/runtime_state.json → runtime state (DO NOT COMMIT)

---

## Task Execution Rules

- Always operate from a task document when available
- Respect:
  - selected_backend
  - verification_profile
  - acceptance_criteria
- If a task conflicts with architecture constraints or phase scope:
  - STOP and report conflict

---

## Backend Rules

- Backends must:
  - execute commands deterministically
  - capture stdout, stderr, exit_code
  - not silently fail
- Do not invent backend interfaces; use existing adapters
- Codex CLI, Aider, Gemini, Claude Code should be invoked through backends only

---

## Verification Rules

- Verification must be deterministic
- Preferred checks:
  - pytest
  - python -m py_compile
- Do not rely on model self-evaluation

---

## Git Rules

- Do not commit:
  - runtime_state.json
  - reports/
  - logs/
  - virtual environments
- Do not modify .gitignore unless required by task
- Do not create excessive commits; prefer grouped logical commits

---

## Allowed Changes

- Implement task requirements
- Fix failing verification
- Update relevant tests
- Improve documentation tied to the task

---

## Forbidden Changes

- Changing architecture without explicit instruction
- Adding dependencies without justification
- Modifying unrelated files
- Deleting important files
- Bypassing verification

---

## Planning Rules

- Plans are multi-phase
- Completed sections are immutable
- Remaining sections may be updated
- Tasks must align with:
  - project brief
  - architecture constraints
  - active phase

---

## Reporting

- All executions must produce structured reports
- Reports must include:
  - changed files
  - verification results
  - assessment

---

## Behavior

- Do not ask unnecessary questions
- Do not stall execution
- Do not perform broad scans unless required
- Prefer direct action over analysis

---

## Priority Order

1. Architecture constraints
2. Task definition
3. Verification results
4. Plan guidance

If conflicts occur, follow this order.

## Run 2026-04-16T20:15:56
- Task ID: demo-self-improve
- Title: Refresh demo status log
- Phase: implementation
- Goal: Update docs/demo_status.md with the latest demo guidance
- Context: Collected 4 semantically relevant files; AGENTS.md guidance:
# AGENTS.md
## Purpose
This repository is operated by an autonomous multi-agent system (abracapocus_2).
All agents must follow these rules when modifying the codebase.
---
## Core Principles
- Minimal blast radius: only modify what is required for the task
- Deterministic verification: all changes must be verifiable via code (tests, compile, scripts)
- No architecture drift: do not introduce new frameworks or major design changes unless explicitly required
- No unrelated refactors
- All changes must be reproducible from a clean clone
---
## Project Structure
- docs/ → design, plans, architecture constraints
- plans/ → master plans
- phases/ → phase definitions
- tasks/ → executable task documents
- backends/ → CLI backend adapters
- agents/ → specialist agents
- runtime/ → orchestration, routing, state
...(truncated)

AGENTS.md guidance:
# AGENTS.md

## Purpose

This repository is operated by an autonomous multi-agent system (abracapocus_2).
All agents must follow these rules when modifying the codebase.

---

## Core Principles

- Minimal blast radius: only modify what is required for the task
- Deterministic verification: all changes must be verifiable via code (tests, compile, scripts)
- No architecture drift: do not introduce new frameworks or major design changes unless explicitly required
- No unrelated refactors
- All changes must be reproducible from a clean clone

---

## Project Structure

- docs/ → design, plans, architecture constraints
- plans/ → master plans
- phases/ → phase definitions
- tasks/ → executable task documents
- backends/ → CLI backend adapters
- agents/ → specialist agents
- runtime/ → orchestration, routing, state
- reports/ → execution reports (DO NOT MODIFY MANUALLY)
- state/runtime_state.json → runtime state (DO NOT COMMIT)

---

## Task Execution Rules

- Always operate from a task document when available
- Respect:
  - selected_backend
  - verification_profile
  - acceptance_criteria
- If a task conflicts with architecture constraints or phase scope:
  - STOP and report conflict

---

## Backend Rules

- Backends must:
  - execute commands deterministically
  - capture stdout, stderr, exit_code
  - not silently fail
- Do not invent backend interfaces; use existing adapters
- Codex CLI, Aider, Gemini, Claude Code should be invoked through backends only

---

## Verification Rules

- Verification must be deterministic
- Preferred checks:
  - pytest
  - python -m py_compile
- Do not rely on model self-evaluation

---

## Git Rules

- Do not commit:
  - runtime_state.json
  - reports/
  - logs/
  - virtual environments
- Do not modify .gitignore unless required by task
- Do not create excessive commits; prefer grouped logical commits

---

## Allowed Changes

- Implement task requirements
- Fix failing verification
- Update relevant tests
- Improve documentation tied to the task

---

## Forbidden Changes

- Changing architecture without explicit instruction
- Adding dependencies without justification
- Modifying unrelated files
- Deleting important files
- Bypassing verification

---

## Planning Rules

- Plans are multi-phase
- Completed sections are immutable
- Remaining sections may be updated
- Tasks must align with:
  - project brief
  - architecture constraints
  - active phase

---

## Reporting

- All executions must produce structured reports
- Reports must include:
  - changed files
  - verification results
  - assessment

---

## Behavior

- Do not ask unnecessary questions
- Do not stall execution
- Do not perform broad scans unless required
- Prefer direct action over analysis

---

## Priority Order

1. Architecture constraints
2. Task definition
3. Verification results
4. Plan guidance

If conflicts occur, follow this order.

## Run 2026-04-16T20:24:47
- Task ID: demo-self-improve
- Title: Refresh demo status log
- Phase: implementation
- Goal: Update docs/demo_status.md with the latest demo guidance
- Context: Collected 3 semantically relevant files; AGENTS.md guidance:
# AGENTS.md
## Purpose
This repository is operated by an autonomous multi-agent system (abracapocus_2).
All agents must follow these rules when modifying the codebase.
---
## Core Principles
- Minimal blast radius: only modify what is required for the task
- Deterministic verification: all changes must be verifiable via code (tests, compile, scripts)
- No architecture drift: do not introduce new frameworks or major design changes unless explicitly required
- No unrelated refactors
- All changes must be reproducible from a clean clone
---
## Project Structure
- docs/ → design, plans, architecture constraints
- plans/ → master plans
- phases/ → phase definitions
- tasks/ → executable task documents
- backends/ → CLI backend adapters
- agents/ → specialist agents
- runtime/ → orchestration, routing, state
...(truncated)

AGENTS.md guidance:
# AGENTS.md

## Purpose

This repository is operated by an autonomous multi-agent system (abracapocus_2).
All agents must follow these rules when modifying the codebase.

---

## Core Principles

- Minimal blast radius: only modify what is required for the task
- Deterministic verification: all changes must be verifiable via code (tests, compile, scripts)
- No architecture drift: do not introduce new frameworks or major design changes unless explicitly required
- No unrelated refactors
- All changes must be reproducible from a clean clone

---

## Project Structure

- docs/ → design, plans, architecture constraints
- plans/ → master plans
- phases/ → phase definitions
- tasks/ → executable task documents
- backends/ → CLI backend adapters
- agents/ → specialist agents
- runtime/ → orchestration, routing, state
- reports/ → execution reports (DO NOT MODIFY MANUALLY)
- state/runtime_state.json → runtime state (DO NOT COMMIT)

---

## Task Execution Rules

- Always operate from a task document when available
- Respect:
  - selected_backend
  - verification_profile
  - acceptance_criteria
- If a task conflicts with architecture constraints or phase scope:
  - STOP and report conflict

---

## Backend Rules

- Backends must:
  - execute commands deterministically
  - capture stdout, stderr, exit_code
  - not silently fail
- Do not invent backend interfaces; use existing adapters
- Codex CLI, Aider, Gemini, Claude Code should be invoked through backends only

---

## Verification Rules

- Verification must be deterministic
- Preferred checks:
  - pytest
  - python -m py_compile
- Do not rely on model self-evaluation

---

## Git Rules

- Do not commit:
  - runtime_state.json
  - reports/
  - logs/
  - virtual environments
- Do not modify .gitignore unless required by task
- Do not create excessive commits; prefer grouped logical commits

---

## Allowed Changes

- Implement task requirements
- Fix failing verification
- Update relevant tests
- Improve documentation tied to the task

---

## Forbidden Changes

- Changing architecture without explicit instruction
- Adding dependencies without justification
- Modifying unrelated files
- Deleting important files
- Bypassing verification

---

## Planning Rules

- Plans are multi-phase
- Completed sections are immutable
- Remaining sections may be updated
- Tasks must align with:
  - project brief
  - architecture constraints
  - active phase

---

## Reporting

- All executions must produce structured reports
- Reports must include:
  - changed files
  - verification results
  - assessment

---

## Behavior

- Do not ask unnecessary questions
- Do not stall execution
- Do not perform broad scans unless required
- Prefer direct action over analysis

---

## Priority Order

1. Architecture constraints
2. Task definition
3. Verification results
4. Plan guidance

If conflicts occur, follow this order.

## Run 2026-04-16T20:25:04
- Task ID: demo-self-improve
- Title: Refresh demo status log
- Phase: implementation
- Goal: Update docs/demo_status.md with the latest demo guidance
- Context: Collected 3 semantically relevant files; AGENTS.md guidance:
# AGENTS.md
## Purpose
This repository is operated by an autonomous multi-agent system (abracapocus_2).
All agents must follow these rules when modifying the codebase.
---
## Core Principles
- Minimal blast radius: only modify what is required for the task
- Deterministic verification: all changes must be verifiable via code (tests, compile, scripts)
- No architecture drift: do not introduce new frameworks or major design changes unless explicitly required
- No unrelated refactors
- All changes must be reproducible from a clean clone
---
## Project Structure
- docs/ → design, plans, architecture constraints
- plans/ → master plans
- phases/ → phase definitions
- tasks/ → executable task documents
- backends/ → CLI backend adapters
- agents/ → specialist agents
- runtime/ → orchestration, routing, state
...(truncated)

AGENTS.md guidance:
# AGENTS.md

## Purpose

This repository is operated by an autonomous multi-agent system (abracapocus_2).
All agents must follow these rules when modifying the codebase.

---

## Core Principles

- Minimal blast radius: only modify what is required for the task
- Deterministic verification: all changes must be verifiable via code (tests, compile, scripts)
- No architecture drift: do not introduce new frameworks or major design changes unless explicitly required
- No unrelated refactors
- All changes must be reproducible from a clean clone

---

## Project Structure

- docs/ → design, plans, architecture constraints
- plans/ → master plans
- phases/ → phase definitions
- tasks/ → executable task documents
- backends/ → CLI backend adapters
- agents/ → specialist agents
- runtime/ → orchestration, routing, state
- reports/ → execution reports (DO NOT MODIFY MANUALLY)
- state/runtime_state.json → runtime state (DO NOT COMMIT)

---

## Task Execution Rules

- Always operate from a task document when available
- Respect:
  - selected_backend
  - verification_profile
  - acceptance_criteria
- If a task conflicts with architecture constraints or phase scope:
  - STOP and report conflict

---

## Backend Rules

- Backends must:
  - execute commands deterministically
  - capture stdout, stderr, exit_code
  - not silently fail
- Do not invent backend interfaces; use existing adapters
- Codex CLI, Aider, Gemini, Claude Code should be invoked through backends only

---

## Verification Rules

- Verification must be deterministic
- Preferred checks:
  - pytest
  - python -m py_compile
- Do not rely on model self-evaluation

---

## Git Rules

- Do not commit:
  - runtime_state.json
  - reports/
  - logs/
  - virtual environments
- Do not modify .gitignore unless required by task
- Do not create excessive commits; prefer grouped logical commits

---

## Allowed Changes

- Implement task requirements
- Fix failing verification
- Update relevant tests
- Improve documentation tied to the task

---

## Forbidden Changes

- Changing architecture without explicit instruction
- Adding dependencies without justification
- Modifying unrelated files
- Deleting important files
- Bypassing verification

---

## Planning Rules

- Plans are multi-phase
- Completed sections are immutable
- Remaining sections may be updated
- Tasks must align with:
  - project brief
  - architecture constraints
  - active phase

---

## Reporting

- All executions must produce structured reports
- Reports must include:
  - changed files
  - verification results
  - assessment

---

## Behavior

- Do not ask unnecessary questions
- Do not stall execution
- Do not perform broad scans unless required
- Prefer direct action over analysis

---

## Priority Order

1. Architecture constraints
2. Task definition
3. Verification results
4. Plan guidance

If conflicts occur, follow this order.

## Run 2026-04-16T20:26:04
- Task ID: demo-self-improve
- Title: Refresh demo status log
- Phase: implementation
- Goal: Update docs/demo_status.md with the latest demo guidance
- Context: Collected 5 semantically relevant files; AGENTS.md guidance:
# AGENTS.md
## Purpose
This repository is operated by an autonomous multi-agent system (abracapocus_2).
All agents must follow these rules when modifying the codebase.
---
## Core Principles
- Minimal blast radius: only modify what is required for the task
- Deterministic verification: all changes must be verifiable via code (tests, compile, scripts)
- No architecture drift: do not introduce new frameworks or major design changes unless explicitly required
- No unrelated refactors
- All changes must be reproducible from a clean clone
---
## Project Structure
- docs/ → design, plans, architecture constraints
- plans/ → master plans
- phases/ → phase definitions
- tasks/ → executable task documents
- backends/ → CLI backend adapters
- agents/ → specialist agents
- runtime/ → orchestration, routing, state
...(truncated)

AGENTS.md guidance:
# AGENTS.md

## Purpose

This repository is operated by an autonomous multi-agent system (abracapocus_2).
All agents must follow these rules when modifying the codebase.

---

## Core Principles

- Minimal blast radius: only modify what is required for the task
- Deterministic verification: all changes must be verifiable via code (tests, compile, scripts)
- No architecture drift: do not introduce new frameworks or major design changes unless explicitly required
- No unrelated refactors
- All changes must be reproducible from a clean clone

---

## Project Structure

- docs/ → design, plans, architecture constraints
- plans/ → master plans
- phases/ → phase definitions
- tasks/ → executable task documents
- backends/ → CLI backend adapters
- agents/ → specialist agents
- runtime/ → orchestration, routing, state
- reports/ → execution reports (DO NOT MODIFY MANUALLY)
- state/runtime_state.json → runtime state (DO NOT COMMIT)

---

## Task Execution Rules

- Always operate from a task document when available
- Respect:
  - selected_backend
  - verification_profile
  - acceptance_criteria
- If a task conflicts with architecture constraints or phase scope:
  - STOP and report conflict

---

## Backend Rules

- Backends must:
  - execute commands deterministically
  - capture stdout, stderr, exit_code
  - not silently fail
- Do not invent backend interfaces; use existing adapters
- Codex CLI, Aider, Gemini, Claude Code should be invoked through backends only

---

## Verification Rules

- Verification must be deterministic
- Preferred checks:
  - pytest
  - python -m py_compile
- Do not rely on model self-evaluation

---

## Git Rules

- Do not commit:
  - runtime_state.json
  - reports/
  - logs/
  - virtual environments
- Do not modify .gitignore unless required by task
- Do not create excessive commits; prefer grouped logical commits

---

## Allowed Changes

- Implement task requirements
- Fix failing verification
- Update relevant tests
- Improve documentation tied to the task

---

## Forbidden Changes

- Changing architecture without explicit instruction
- Adding dependencies without justification
- Modifying unrelated files
- Deleting important files
- Bypassing verification

---

## Planning Rules

- Plans are multi-phase
- Completed sections are immutable
- Remaining sections may be updated
- Tasks must align with:
  - project brief
  - architecture constraints
  - active phase

---

## Reporting

- All executions must produce structured reports
- Reports must include:
  - changed files
  - verification results
  - assessment

---

## Behavior

- Do not ask unnecessary questions
- Do not stall execution
- Do not perform broad scans unless required
- Prefer direct action over analysis

---

## Priority Order

1. Architecture constraints
2. Task definition
3. Verification results
4. Plan guidance

If conflicts occur, follow this order.

## Run 2026-04-16T20:26:27
- Task ID: demo-self-improve
- Title: Refresh demo status log
- Phase: implementation
- Goal: Update docs/demo_status.md with the latest demo guidance
- Context: Collected 3 semantically relevant files; AGENTS.md guidance:
# AGENTS.md
## Purpose
This repository is operated by an autonomous multi-agent system (abracapocus_2).
All agents must follow these rules when modifying the codebase.
---
## Core Principles
- Minimal blast radius: only modify what is required for the task
- Deterministic verification: all changes must be verifiable via code (tests, compile, scripts)
- No architecture drift: do not introduce new frameworks or major design changes unless explicitly required
- No unrelated refactors
- All changes must be reproducible from a clean clone
---
## Project Structure
- docs/ → design, plans, architecture constraints
- plans/ → master plans
- phases/ → phase definitions
- tasks/ → executable task documents
- backends/ → CLI backend adapters
- agents/ → specialist agents
- runtime/ → orchestration, routing, state
...(truncated)

AGENTS.md guidance:
# AGENTS.md

## Purpose

This repository is operated by an autonomous multi-agent system (abracapocus_2).
All agents must follow these rules when modifying the codebase.

---

## Core Principles

- Minimal blast radius: only modify what is required for the task
- Deterministic verification: all changes must be verifiable via code (tests, compile, scripts)
- No architecture drift: do not introduce new frameworks or major design changes unless explicitly required
- No unrelated refactors
- All changes must be reproducible from a clean clone

---

## Project Structure

- docs/ → design, plans, architecture constraints
- plans/ → master plans
- phases/ → phase definitions
- tasks/ → executable task documents
- backends/ → CLI backend adapters
- agents/ → specialist agents
- runtime/ → orchestration, routing, state
- reports/ → execution reports (DO NOT MODIFY MANUALLY)
- state/runtime_state.json → runtime state (DO NOT COMMIT)

---

## Task Execution Rules

- Always operate from a task document when available
- Respect:
  - selected_backend
  - verification_profile
  - acceptance_criteria
- If a task conflicts with architecture constraints or phase scope:
  - STOP and report conflict

---

## Backend Rules

- Backends must:
  - execute commands deterministically
  - capture stdout, stderr, exit_code
  - not silently fail
- Do not invent backend interfaces; use existing adapters
- Codex CLI, Aider, Gemini, Claude Code should be invoked through backends only

---

## Verification Rules

- Verification must be deterministic
- Preferred checks:
  - pytest
  - python -m py_compile
- Do not rely on model self-evaluation

---

## Git Rules

- Do not commit:
  - runtime_state.json
  - reports/
  - logs/
  - virtual environments
- Do not modify .gitignore unless required by task
- Do not create excessive commits; prefer grouped logical commits

---

## Allowed Changes

- Implement task requirements
- Fix failing verification
- Update relevant tests
- Improve documentation tied to the task

---

## Forbidden Changes

- Changing architecture without explicit instruction
- Adding dependencies without justification
- Modifying unrelated files
- Deleting important files
- Bypassing verification

---

## Planning Rules

- Plans are multi-phase
- Completed sections are immutable
- Remaining sections may be updated
- Tasks must align with:
  - project brief
  - architecture constraints
  - active phase

---

## Reporting

- All executions must produce structured reports
- Reports must include:
  - changed files
  - verification results
  - assessment

---

## Behavior

- Do not ask unnecessary questions
- Do not stall execution
- Do not perform broad scans unless required
- Prefer direct action over analysis

---

## Priority Order

1. Architecture constraints
2. Task definition
3. Verification results
4. Plan guidance

If conflicts occur, follow this order.

## Run 2026-04-16T20:41:05
- Task ID: demo-self-improve
- Title: Refresh demo status log
- Phase: implementation
- Goal: Update docs/demo_status.md with the latest demo guidance
- Context: Collected 2 semantically relevant files; AGENTS.md guidance:
# AGENTS.md
## Purpose
This repository is operated by an autonomous multi-agent system (abracapocus_2).
All agents must follow these rules when modifying the codebase.
---
## Core Principles
- Minimal blast radius: only modify what is required for the task
- Deterministic verification: all changes must be verifiable via code (tests, compile, scripts)
- No architecture drift: do not introduce new frameworks or major design changes unless explicitly required
- No unrelated refactors
- All changes must be reproducible from a clean clone
---
## Project Structure
- docs/ → design, plans, architecture constraints
- plans/ → master plans
- phases/ → phase definitions
- tasks/ → executable task documents
- backends/ → CLI backend adapters
- agents/ → specialist agents
- runtime/ → orchestration, routing, state
...(truncated)

AGENTS.md guidance:
# AGENTS.md

## Purpose

This repository is operated by an autonomous multi-agent system (abracapocus_2).
All agents must follow these rules when modifying the codebase.

---

## Core Principles

- Minimal blast radius: only modify what is required for the task
- Deterministic verification: all changes must be verifiable via code (tests, compile, scripts)
- No architecture drift: do not introduce new frameworks or major design changes unless explicitly required
- No unrelated refactors
- All changes must be reproducible from a clean clone

---

## Project Structure

- docs/ → design, plans, architecture constraints
- plans/ → master plans
- phases/ → phase definitions
- tasks/ → executable task documents
- backends/ → CLI backend adapters
- agents/ → specialist agents
- runtime/ → orchestration, routing, state
- reports/ → execution reports (DO NOT MODIFY MANUALLY)
- state/runtime_state.json → runtime state (DO NOT COMMIT)

---

## Task Execution Rules

- Always operate from a task document when available
- Respect:
  - selected_backend
  - verification_profile
  - acceptance_criteria
- If a task conflicts with architecture constraints or phase scope:
  - STOP and report conflict

---

## Backend Rules

- Backends must:
  - execute commands deterministically
  - capture stdout, stderr, exit_code
  - not silently fail
- Do not invent backend interfaces; use existing adapters
- Codex CLI, Aider, Gemini, Claude Code should be invoked through backends only

---

## Verification Rules

- Verification must be deterministic
- Preferred checks:
  - pytest
  - python -m py_compile
- Do not rely on model self-evaluation

---

## Git Rules

- Do not commit:
  - runtime_state.json
  - reports/
  - logs/
  - virtual environments
- Do not modify .gitignore unless required by task
- Do not create excessive commits; prefer grouped logical commits

---

## Allowed Changes

- Implement task requirements
- Fix failing verification
- Update relevant tests
- Improve documentation tied to the task

---

## Forbidden Changes

- Changing architecture without explicit instruction
- Adding dependencies without justification
- Modifying unrelated files
- Deleting important files
- Bypassing verification

---

## Planning Rules

- Plans are multi-phase
- Completed sections are immutable
- Remaining sections may be updated
- Tasks must align with:
  - project brief
  - architecture constraints
  - active phase

---

## Reporting

- All executions must produce structured reports
- Reports must include:
  - changed files
  - verification results
  - assessment

---

## Behavior

- Do not ask unnecessary questions
- Do not stall execution
- Do not perform broad scans unless required
- Prefer direct action over analysis

---

## Priority Order

1. Architecture constraints
2. Task definition
3. Verification results
4. Plan guidance

If conflicts occur, follow this order.

## Run 2026-04-16T20:41:33
- Task ID: demo-self-improve
- Title: Refresh demo status log
- Phase: implementation
- Goal: Update docs/demo_status.md with the latest demo guidance
- Context: Collected 4 semantically relevant files; AGENTS.md guidance:
# AGENTS.md
## Purpose
This repository is operated by an autonomous multi-agent system (abracapocus_2).
All agents must follow these rules when modifying the codebase.
---
## Core Principles
- Minimal blast radius: only modify what is required for the task
- Deterministic verification: all changes must be verifiable via code (tests, compile, scripts)
- No architecture drift: do not introduce new frameworks or major design changes unless explicitly required
- No unrelated refactors
- All changes must be reproducible from a clean clone
---
## Project Structure
- docs/ → design, plans, architecture constraints
- plans/ → master plans
- phases/ → phase definitions
- tasks/ → executable task documents
- backends/ → CLI backend adapters
- agents/ → specialist agents
- runtime/ → orchestration, routing, state
...(truncated)

AGENTS.md guidance:
# AGENTS.md

## Purpose

This repository is operated by an autonomous multi-agent system (abracapocus_2).
All agents must follow these rules when modifying the codebase.

---

## Core Principles

- Minimal blast radius: only modify what is required for the task
- Deterministic verification: all changes must be verifiable via code (tests, compile, scripts)
- No architecture drift: do not introduce new frameworks or major design changes unless explicitly required
- No unrelated refactors
- All changes must be reproducible from a clean clone

---

## Project Structure

- docs/ → design, plans, architecture constraints
- plans/ → master plans
- phases/ → phase definitions
- tasks/ → executable task documents
- backends/ → CLI backend adapters
- agents/ → specialist agents
- runtime/ → orchestration, routing, state
- reports/ → execution reports (DO NOT MODIFY MANUALLY)
- state/runtime_state.json → runtime state (DO NOT COMMIT)

---

## Task Execution Rules

- Always operate from a task document when available
- Respect:
  - selected_backend
  - verification_profile
  - acceptance_criteria
- If a task conflicts with architecture constraints or phase scope:
  - STOP and report conflict

---

## Backend Rules

- Backends must:
  - execute commands deterministically
  - capture stdout, stderr, exit_code
  - not silently fail
- Do not invent backend interfaces; use existing adapters
- Codex CLI, Aider, Gemini, Claude Code should be invoked through backends only

---

## Verification Rules

- Verification must be deterministic
- Preferred checks:
  - pytest
  - python -m py_compile
- Do not rely on model self-evaluation

---

## Git Rules

- Do not commit:
  - runtime_state.json
  - reports/
  - logs/
  - virtual environments
- Do not modify .gitignore unless required by task
- Do not create excessive commits; prefer grouped logical commits

---

## Allowed Changes

- Implement task requirements
- Fix failing verification
- Update relevant tests
- Improve documentation tied to the task

---

## Forbidden Changes

- Changing architecture without explicit instruction
- Adding dependencies without justification
- Modifying unrelated files
- Deleting important files
- Bypassing verification

---

## Planning Rules

- Plans are multi-phase
- Completed sections are immutable
- Remaining sections may be updated
- Tasks must align with:
  - project brief
  - architecture constraints
  - active phase

---

## Reporting

- All executions must produce structured reports
- Reports must include:
  - changed files
  - verification results
  - assessment

---

## Behavior

- Do not ask unnecessary questions
- Do not stall execution
- Do not perform broad scans unless required
- Prefer direct action over analysis

---

## Priority Order

1. Architecture constraints
2. Task definition
3. Verification results
4. Plan guidance

If conflicts occur, follow this order.

## Run 2026-04-16T20:41:49
- Task ID: demo-self-improve
- Title: Refresh demo status log
- Phase: implementation
- Goal: Update docs/demo_status.md with the latest demo guidance
- Context: Collected 3 semantically relevant files; AGENTS.md guidance:
# AGENTS.md
## Purpose
This repository is operated by an autonomous multi-agent system (abracapocus_2).
All agents must follow these rules when modifying the codebase.
---
## Core Principles
- Minimal blast radius: only modify what is required for the task
- Deterministic verification: all changes must be verifiable via code (tests, compile, scripts)
- No architecture drift: do not introduce new frameworks or major design changes unless explicitly required
- No unrelated refactors
- All changes must be reproducible from a clean clone
---
## Project Structure
- docs/ → design, plans, architecture constraints
- plans/ → master plans
- phases/ → phase definitions
- tasks/ → executable task documents
- backends/ → CLI backend adapters
- agents/ → specialist agents
- runtime/ → orchestration, routing, state
...(truncated)

AGENTS.md guidance:
# AGENTS.md

## Purpose

This repository is operated by an autonomous multi-agent system (abracapocus_2).
All agents must follow these rules when modifying the codebase.

---

## Core Principles

- Minimal blast radius: only modify what is required for the task
- Deterministic verification: all changes must be verifiable via code (tests, compile, scripts)
- No architecture drift: do not introduce new frameworks or major design changes unless explicitly required
- No unrelated refactors
- All changes must be reproducible from a clean clone

---

## Project Structure

- docs/ → design, plans, architecture constraints
- plans/ → master plans
- phases/ → phase definitions
- tasks/ → executable task documents
- backends/ → CLI backend adapters
- agents/ → specialist agents
- runtime/ → orchestration, routing, state
- reports/ → execution reports (DO NOT MODIFY MANUALLY)
- state/runtime_state.json → runtime state (DO NOT COMMIT)

---

## Task Execution Rules

- Always operate from a task document when available
- Respect:
  - selected_backend
  - verification_profile
  - acceptance_criteria
- If a task conflicts with architecture constraints or phase scope:
  - STOP and report conflict

---

## Backend Rules

- Backends must:
  - execute commands deterministically
  - capture stdout, stderr, exit_code
  - not silently fail
- Do not invent backend interfaces; use existing adapters
- Codex CLI, Aider, Gemini, Claude Code should be invoked through backends only

---

## Verification Rules

- Verification must be deterministic
- Preferred checks:
  - pytest
  - python -m py_compile
- Do not rely on model self-evaluation

---

## Git Rules

- Do not commit:
  - runtime_state.json
  - reports/
  - logs/
  - virtual environments
- Do not modify .gitignore unless required by task
- Do not create excessive commits; prefer grouped logical commits

---

## Allowed Changes

- Implement task requirements
- Fix failing verification
- Update relevant tests
- Improve documentation tied to the task

---

## Forbidden Changes

- Changing architecture without explicit instruction
- Adding dependencies without justification
- Modifying unrelated files
- Deleting important files
- Bypassing verification

---

## Planning Rules

- Plans are multi-phase
- Completed sections are immutable
- Remaining sections may be updated
- Tasks must align with:
  - project brief
  - architecture constraints
  - active phase

---

## Reporting

- All executions must produce structured reports
- Reports must include:
  - changed files
  - verification results
  - assessment

---

## Behavior

- Do not ask unnecessary questions
- Do not stall execution
- Do not perform broad scans unless required
- Prefer direct action over analysis

---

## Priority Order

1. Architecture constraints
2. Task definition
3. Verification results
4. Plan guidance

If conflicts occur, follow this order.

## Run 2026-04-16T20:43:35
- Task ID: demo-self-improve
- Title: Refresh demo status log
- Phase: implementation
- Goal: Update docs/demo_status.md with the latest demo guidance
- Context: Collected 2 semantically relevant files; AGENTS.md guidance:
# AGENTS.md
## Purpose
This repository is operated by an autonomous multi-agent system (abracapocus_2).
All agents must follow these rules when modifying the codebase.
---
## Core Principles
- Minimal blast radius: only modify what is required for the task
- Deterministic verification: all changes must be verifiable via code (tests, compile, scripts)
- No architecture drift: do not introduce new frameworks or major design changes unless explicitly required
- No unrelated refactors
- All changes must be reproducible from a clean clone
---
## Project Structure
- docs/ → design, plans, architecture constraints
- plans/ → master plans
- phases/ → phase definitions
- tasks/ → executable task documents
- backends/ → CLI backend adapters
- agents/ → specialist agents
- runtime/ → orchestration, routing, state
...(truncated)

AGENTS.md guidance:
# AGENTS.md

## Purpose

This repository is operated by an autonomous multi-agent system (abracapocus_2).
All agents must follow these rules when modifying the codebase.

---

## Core Principles

- Minimal blast radius: only modify what is required for the task
- Deterministic verification: all changes must be verifiable via code (tests, compile, scripts)
- No architecture drift: do not introduce new frameworks or major design changes unless explicitly required
- No unrelated refactors
- All changes must be reproducible from a clean clone

---

## Project Structure

- docs/ → design, plans, architecture constraints
- plans/ → master plans
- phases/ → phase definitions
- tasks/ → executable task documents
- backends/ → CLI backend adapters
- agents/ → specialist agents
- runtime/ → orchestration, routing, state
- reports/ → execution reports (DO NOT MODIFY MANUALLY)
- state/runtime_state.json → runtime state (DO NOT COMMIT)

---

## Task Execution Rules

- Always operate from a task document when available
- Respect:
  - selected_backend
  - verification_profile
  - acceptance_criteria
- If a task conflicts with architecture constraints or phase scope:
  - STOP and report conflict

---

## Backend Rules

- Backends must:
  - execute commands deterministically
  - capture stdout, stderr, exit_code
  - not silently fail
- Do not invent backend interfaces; use existing adapters
- Codex CLI, Aider, Gemini, Claude Code should be invoked through backends only

---

## Verification Rules

- Verification must be deterministic
- Preferred checks:
  - pytest
  - python -m py_compile
- Do not rely on model self-evaluation

---

## Git Rules

- Do not commit:
  - runtime_state.json
  - reports/
  - logs/
  - virtual environments
- Do not modify .gitignore unless required by task
- Do not create excessive commits; prefer grouped logical commits

---

## Allowed Changes

- Implement task requirements
- Fix failing verification
- Update relevant tests
- Improve documentation tied to the task

---

## Forbidden Changes

- Changing architecture without explicit instruction
- Adding dependencies without justification
- Modifying unrelated files
- Deleting important files
- Bypassing verification

---

## Planning Rules

- Plans are multi-phase
- Completed sections are immutable
- Remaining sections may be updated
- Tasks must align with:
  - project brief
  - architecture constraints
  - active phase

---

## Reporting

- All executions must produce structured reports
- Reports must include:
  - changed files
  - verification results
  - assessment

---

## Behavior

- Do not ask unnecessary questions
- Do not stall execution
- Do not perform broad scans unless required
- Prefer direct action over analysis

---

## Priority Order

1. Architecture constraints
2. Task definition
3. Verification results
4. Plan guidance

If conflicts occur, follow this order.

## Run 2026-04-16T20:44:07
- Task ID: demo-self-improve
- Title: Refresh demo status log
- Phase: implementation
- Goal: Update docs/demo_status.md with the latest demo guidance
- Context: Collected 2 semantically relevant files; AGENTS.md guidance:
# AGENTS.md
## Purpose
This repository is operated by an autonomous multi-agent system (abracapocus_2).
All agents must follow these rules when modifying the codebase.
---
## Core Principles
- Minimal blast radius: only modify what is required for the task
- Deterministic verification: all changes must be verifiable via code (tests, compile, scripts)
- No architecture drift: do not introduce new frameworks or major design changes unless explicitly required
- No unrelated refactors
- All changes must be reproducible from a clean clone
---
## Project Structure
- docs/ → design, plans, architecture constraints
- plans/ → master plans
- phases/ → phase definitions
- tasks/ → executable task documents
- backends/ → CLI backend adapters
- agents/ → specialist agents
- runtime/ → orchestration, routing, state
...(truncated)

AGENTS.md guidance:
# AGENTS.md

## Purpose

This repository is operated by an autonomous multi-agent system (abracapocus_2).
All agents must follow these rules when modifying the codebase.

---

## Core Principles

- Minimal blast radius: only modify what is required for the task
- Deterministic verification: all changes must be verifiable via code (tests, compile, scripts)
- No architecture drift: do not introduce new frameworks or major design changes unless explicitly required
- No unrelated refactors
- All changes must be reproducible from a clean clone

---

## Project Structure

- docs/ → design, plans, architecture constraints
- plans/ → master plans
- phases/ → phase definitions
- tasks/ → executable task documents
- backends/ → CLI backend adapters
- agents/ → specialist agents
- runtime/ → orchestration, routing, state
- reports/ → execution reports (DO NOT MODIFY MANUALLY)
- state/runtime_state.json → runtime state (DO NOT COMMIT)

---

## Task Execution Rules

- Always operate from a task document when available
- Respect:
  - selected_backend
  - verification_profile
  - acceptance_criteria
- If a task conflicts with architecture constraints or phase scope:
  - STOP and report conflict

---

## Backend Rules

- Backends must:
  - execute commands deterministically
  - capture stdout, stderr, exit_code
  - not silently fail
- Do not invent backend interfaces; use existing adapters
- Codex CLI, Aider, Gemini, Claude Code should be invoked through backends only

---

## Verification Rules

- Verification must be deterministic
- Preferred checks:
  - pytest
  - python -m py_compile
- Do not rely on model self-evaluation

---

## Git Rules

- Do not commit:
  - runtime_state.json
  - reports/
  - logs/
  - virtual environments
- Do not modify .gitignore unless required by task
- Do not create excessive commits; prefer grouped logical commits

---

## Allowed Changes

- Implement task requirements
- Fix failing verification
- Update relevant tests
- Improve documentation tied to the task

---

## Forbidden Changes

- Changing architecture without explicit instruction
- Adding dependencies without justification
- Modifying unrelated files
- Deleting important files
- Bypassing verification

---

## Planning Rules

- Plans are multi-phase
- Completed sections are immutable
- Remaining sections may be updated
- Tasks must align with:
  - project brief
  - architecture constraints
  - active phase

---

## Reporting

- All executions must produce structured reports
- Reports must include:
  - changed files
  - verification results
  - assessment

---

## Behavior

- Do not ask unnecessary questions
- Do not stall execution
- Do not perform broad scans unless required
- Prefer direct action over analysis

---

## Priority Order

1. Architecture constraints
2. Task definition
3. Verification results
4. Plan guidance

If conflicts occur, follow this order.

## Run 2026-04-16T20:44:29
- Task ID: demo-self-improve
- Title: Refresh demo status log
- Phase: implementation
- Goal: Update docs/demo_status.md with the latest demo guidance
- Context: Collected 2 semantically relevant files; AGENTS.md guidance:
# AGENTS.md
## Purpose
This repository is operated by an autonomous multi-agent system (abracapocus_2).
All agents must follow these rules when modifying the codebase.
---
## Core Principles
- Minimal blast radius: only modify what is required for the task
- Deterministic verification: all changes must be verifiable via code (tests, compile, scripts)
- No architecture drift: do not introduce new frameworks or major design changes unless explicitly required
- No unrelated refactors
- All changes must be reproducible from a clean clone
---
## Project Structure
- docs/ → design, plans, architecture constraints
- plans/ → master plans
- phases/ → phase definitions
- tasks/ → executable task documents
- backends/ → CLI backend adapters
- agents/ → specialist agents
- runtime/ → orchestration, routing, state
...(truncated)

AGENTS.md guidance:
# AGENTS.md

## Purpose

This repository is operated by an autonomous multi-agent system (abracapocus_2).
All agents must follow these rules when modifying the codebase.

---

## Core Principles

- Minimal blast radius: only modify what is required for the task
- Deterministic verification: all changes must be verifiable via code (tests, compile, scripts)
- No architecture drift: do not introduce new frameworks or major design changes unless explicitly required
- No unrelated refactors
- All changes must be reproducible from a clean clone

---

## Project Structure

- docs/ → design, plans, architecture constraints
- plans/ → master plans
- phases/ → phase definitions
- tasks/ → executable task documents
- backends/ → CLI backend adapters
- agents/ → specialist agents
- runtime/ → orchestration, routing, state
- reports/ → execution reports (DO NOT MODIFY MANUALLY)
- state/runtime_state.json → runtime state (DO NOT COMMIT)

---

## Task Execution Rules

- Always operate from a task document when available
- Respect:
  - selected_backend
  - verification_profile
  - acceptance_criteria
- If a task conflicts with architecture constraints or phase scope:
  - STOP and report conflict

---

## Backend Rules

- Backends must:
  - execute commands deterministically
  - capture stdout, stderr, exit_code
  - not silently fail
- Do not invent backend interfaces; use existing adapters
- Codex CLI, Aider, Gemini, Claude Code should be invoked through backends only

---

## Verification Rules

- Verification must be deterministic
- Preferred checks:
  - pytest
  - python -m py_compile
- Do not rely on model self-evaluation

---

## Git Rules

- Do not commit:
  - runtime_state.json
  - reports/
  - logs/
  - virtual environments
- Do not modify .gitignore unless required by task
- Do not create excessive commits; prefer grouped logical commits

---

## Allowed Changes

- Implement task requirements
- Fix failing verification
- Update relevant tests
- Improve documentation tied to the task

---

## Forbidden Changes

- Changing architecture without explicit instruction
- Adding dependencies without justification
- Modifying unrelated files
- Deleting important files
- Bypassing verification

---

## Planning Rules

- Plans are multi-phase
- Completed sections are immutable
- Remaining sections may be updated
- Tasks must align with:
  - project brief
  - architecture constraints
  - active phase

---

## Reporting

- All executions must produce structured reports
- Reports must include:
  - changed files
  - verification results
  - assessment

---

## Behavior

- Do not ask unnecessary questions
- Do not stall execution
- Do not perform broad scans unless required
- Prefer direct action over analysis

---

## Priority Order

1. Architecture constraints
2. Task definition
3. Verification results
4. Plan guidance

If conflicts occur, follow this order.

## Run 2026-04-16T20:57:33
- Task ID: demo-self-improve
- Title: Refresh demo status log
- Phase: implementation
- Goal: Update docs/demo_status.md with the latest demo guidance
- Context: Collected 2 semantically relevant files; AGENTS.md guidance:
# AGENTS.md
## Purpose
This repository is operated by an autonomous multi-agent system (abracapocus_2).
All agents must follow these rules when modifying the codebase.
---
## Core Principles
- Minimal blast radius: only modify what is required for the task
- Deterministic verification: all changes must be verifiable via code (tests, compile, scripts)
- No architecture drift: do not introduce new frameworks or major design changes unless explicitly required
- No unrelated refactors
- All changes must be reproducible from a clean clone
---
## Project Structure
- docs/ → design, plans, architecture constraints
- plans/ → master plans
- phases/ → phase definitions
- tasks/ → executable task documents
- backends/ → CLI backend adapters
- agents/ → specialist agents
- runtime/ → orchestration, routing, state
...(truncated)

AGENTS.md guidance:
# AGENTS.md

## Purpose

This repository is operated by an autonomous multi-agent system (abracapocus_2).
All agents must follow these rules when modifying the codebase.

---

## Core Principles

- Minimal blast radius: only modify what is required for the task
- Deterministic verification: all changes must be verifiable via code (tests, compile, scripts)
- No architecture drift: do not introduce new frameworks or major design changes unless explicitly required
- No unrelated refactors
- All changes must be reproducible from a clean clone

---

## Project Structure

- docs/ → design, plans, architecture constraints
- plans/ → master plans
- phases/ → phase definitions
- tasks/ → executable task documents
- backends/ → CLI backend adapters
- agents/ → specialist agents
- runtime/ → orchestration, routing, state
- reports/ → execution reports (DO NOT MODIFY MANUALLY)
- state/runtime_state.json → runtime state (DO NOT COMMIT)

---

## Task Execution Rules

- Always operate from a task document when available
- Respect:
  - selected_backend
  - verification_profile
  - acceptance_criteria
- If a task conflicts with architecture constraints or phase scope:
  - STOP and report conflict

---

## Backend Rules

- Backends must:
  - execute commands deterministically
  - capture stdout, stderr, exit_code
  - not silently fail
- Do not invent backend interfaces; use existing adapters
- Codex CLI, Aider, Gemini, Claude Code should be invoked through backends only

---

## Verification Rules

- Verification must be deterministic
- Preferred checks:
  - pytest
  - python -m py_compile
- Do not rely on model self-evaluation

---

## Git Rules

- Do not commit:
  - runtime_state.json
  - reports/
  - logs/
  - virtual environments
- Do not modify .gitignore unless required by task
- Do not create excessive commits; prefer grouped logical commits

---

## Allowed Changes

- Implement task requirements
- Fix failing verification
- Update relevant tests
- Improve documentation tied to the task

---

## Forbidden Changes

- Changing architecture without explicit instruction
- Adding dependencies without justification
- Modifying unrelated files
- Deleting important files
- Bypassing verification

---

## Planning Rules

- Plans are multi-phase
- Completed sections are immutable
- Remaining sections may be updated
- Tasks must align with:
  - project brief
  - architecture constraints
  - active phase

---

## Reporting

- All executions must produce structured reports
- Reports must include:
  - changed files
  - verification results
  - assessment

---

## Behavior

- Do not ask unnecessary questions
- Do not stall execution
- Do not perform broad scans unless required
- Prefer direct action over analysis

---

## Priority Order

1. Architecture constraints
2. Task definition
3. Verification results
4. Plan guidance

If conflicts occur, follow this order.

## Run 2026-04-16T20:58:06
- Task ID: demo-self-improve
- Title: Refresh demo status log
- Phase: implementation
- Goal: Update docs/demo_status.md with the latest demo guidance
- Context: Collected 2 semantically relevant files; AGENTS.md guidance:
# AGENTS.md
## Purpose
This repository is operated by an autonomous multi-agent system (abracapocus_2).
All agents must follow these rules when modifying the codebase.
---
## Core Principles
- Minimal blast radius: only modify what is required for the task
- Deterministic verification: all changes must be verifiable via code (tests, compile, scripts)
- No architecture drift: do not introduce new frameworks or major design changes unless explicitly required
- No unrelated refactors
- All changes must be reproducible from a clean clone
---
## Project Structure
- docs/ → design, plans, architecture constraints
- plans/ → master plans
- phases/ → phase definitions
- tasks/ → executable task documents
- backends/ → CLI backend adapters
- agents/ → specialist agents
- runtime/ → orchestration, routing, state
...(truncated)

AGENTS.md guidance:
# AGENTS.md

## Purpose

This repository is operated by an autonomous multi-agent system (abracapocus_2).
All agents must follow these rules when modifying the codebase.

---

## Core Principles

- Minimal blast radius: only modify what is required for the task
- Deterministic verification: all changes must be verifiable via code (tests, compile, scripts)
- No architecture drift: do not introduce new frameworks or major design changes unless explicitly required
- No unrelated refactors
- All changes must be reproducible from a clean clone

---

## Project Structure

- docs/ → design, plans, architecture constraints
- plans/ → master plans
- phases/ → phase definitions
- tasks/ → executable task documents
- backends/ → CLI backend adapters
- agents/ → specialist agents
- runtime/ → orchestration, routing, state
- reports/ → execution reports (DO NOT MODIFY MANUALLY)
- state/runtime_state.json → runtime state (DO NOT COMMIT)

---

## Task Execution Rules

- Always operate from a task document when available
- Respect:
  - selected_backend
  - verification_profile
  - acceptance_criteria
- If a task conflicts with architecture constraints or phase scope:
  - STOP and report conflict

---

## Backend Rules

- Backends must:
  - execute commands deterministically
  - capture stdout, stderr, exit_code
  - not silently fail
- Do not invent backend interfaces; use existing adapters
- Codex CLI, Aider, Gemini, Claude Code should be invoked through backends only

---

## Verification Rules

- Verification must be deterministic
- Preferred checks:
  - pytest
  - python -m py_compile
- Do not rely on model self-evaluation

---

## Git Rules

- Do not commit:
  - runtime_state.json
  - reports/
  - logs/
  - virtual environments
- Do not modify .gitignore unless required by task
- Do not create excessive commits; prefer grouped logical commits

---

## Allowed Changes

- Implement task requirements
- Fix failing verification
- Update relevant tests
- Improve documentation tied to the task

---

## Forbidden Changes

- Changing architecture without explicit instruction
- Adding dependencies without justification
- Modifying unrelated files
- Deleting important files
- Bypassing verification

---

## Planning Rules

- Plans are multi-phase
- Completed sections are immutable
- Remaining sections may be updated
- Tasks must align with:
  - project brief
  - architecture constraints
  - active phase

---

## Reporting

- All executions must produce structured reports
- Reports must include:
  - changed files
  - verification results
  - assessment

---

## Behavior

- Do not ask unnecessary questions
- Do not stall execution
- Do not perform broad scans unless required
- Prefer direct action over analysis

---

## Priority Order

1. Architecture constraints
2. Task definition
3. Verification results
4. Plan guidance

If conflicts occur, follow this order.

## Run 2026-04-16T20:58:24
- Task ID: demo-self-improve
- Title: Refresh demo status log
- Phase: implementation
- Goal: Update docs/demo_status.md with the latest demo guidance
- Context: Collected 3 semantically relevant files; AGENTS.md guidance:
# AGENTS.md
## Purpose
This repository is operated by an autonomous multi-agent system (abracapocus_2).
All agents must follow these rules when modifying the codebase.
---
## Core Principles
- Minimal blast radius: only modify what is required for the task
- Deterministic verification: all changes must be verifiable via code (tests, compile, scripts)
- No architecture drift: do not introduce new frameworks or major design changes unless explicitly required
- No unrelated refactors
- All changes must be reproducible from a clean clone
---
## Project Structure
- docs/ → design, plans, architecture constraints
- plans/ → master plans
- phases/ → phase definitions
- tasks/ → executable task documents
- backends/ → CLI backend adapters
- agents/ → specialist agents
- runtime/ → orchestration, routing, state
...(truncated)

AGENTS.md guidance:
# AGENTS.md

## Purpose

This repository is operated by an autonomous multi-agent system (abracapocus_2).
All agents must follow these rules when modifying the codebase.

---

## Core Principles

- Minimal blast radius: only modify what is required for the task
- Deterministic verification: all changes must be verifiable via code (tests, compile, scripts)
- No architecture drift: do not introduce new frameworks or major design changes unless explicitly required
- No unrelated refactors
- All changes must be reproducible from a clean clone

---

## Project Structure

- docs/ → design, plans, architecture constraints
- plans/ → master plans
- phases/ → phase definitions
- tasks/ → executable task documents
- backends/ → CLI backend adapters
- agents/ → specialist agents
- runtime/ → orchestration, routing, state
- reports/ → execution reports (DO NOT MODIFY MANUALLY)
- state/runtime_state.json → runtime state (DO NOT COMMIT)

---

## Task Execution Rules

- Always operate from a task document when available
- Respect:
  - selected_backend
  - verification_profile
  - acceptance_criteria
- If a task conflicts with architecture constraints or phase scope:
  - STOP and report conflict

---

## Backend Rules

- Backends must:
  - execute commands deterministically
  - capture stdout, stderr, exit_code
  - not silently fail
- Do not invent backend interfaces; use existing adapters
- Codex CLI, Aider, Gemini, Claude Code should be invoked through backends only

---

## Verification Rules

- Verification must be deterministic
- Preferred checks:
  - pytest
  - python -m py_compile
- Do not rely on model self-evaluation

---

## Git Rules

- Do not commit:
  - runtime_state.json
  - reports/
  - logs/
  - virtual environments
- Do not modify .gitignore unless required by task
- Do not create excessive commits; prefer grouped logical commits

---

## Allowed Changes

- Implement task requirements
- Fix failing verification
- Update relevant tests
- Improve documentation tied to the task

---

## Forbidden Changes

- Changing architecture without explicit instruction
- Adding dependencies without justification
- Modifying unrelated files
- Deleting important files
- Bypassing verification

---

## Planning Rules

- Plans are multi-phase
- Completed sections are immutable
- Remaining sections may be updated
- Tasks must align with:
  - project brief
  - architecture constraints
  - active phase

---

## Reporting

- All executions must produce structured reports
- Reports must include:
  - changed files
  - verification results
  - assessment

---

## Behavior

- Do not ask unnecessary questions
- Do not stall execution
- Do not perform broad scans unless required
- Prefer direct action over analysis

---

## Priority Order

1. Architecture constraints
2. Task definition
3. Verification results
4. Plan guidance

If conflicts occur, follow this order.

## Run 2026-04-16T21:01:09
- Task ID: demo-self-improve
- Title: Refresh demo status log
- Phase: implementation
- Goal: Update docs/demo_status.md with the latest demo guidance
- Context: Collected 3 semantically relevant files; AGENTS.md guidance:
# AGENTS.md
## Purpose
This repository is operated by an autonomous multi-agent system (abracapocus_2).
All agents must follow these rules when modifying the codebase.
---
## Core Principles
- Minimal blast radius: only modify what is required for the task
- Deterministic verification: all changes must be verifiable via code (tests, compile, scripts)
- No architecture drift: do not introduce new frameworks or major design changes unless explicitly required
- No unrelated refactors
- All changes must be reproducible from a clean clone
---
## Project Structure
- docs/ → design, plans, architecture constraints
- plans/ → master plans
- phases/ → phase definitions
- tasks/ → executable task documents
- backends/ → CLI backend adapters
- agents/ → specialist agents
- runtime/ → orchestration, routing, state
...(truncated)

AGENTS.md guidance:
# AGENTS.md

## Purpose

This repository is operated by an autonomous multi-agent system (abracapocus_2).
All agents must follow these rules when modifying the codebase.

---

## Core Principles

- Minimal blast radius: only modify what is required for the task
- Deterministic verification: all changes must be verifiable via code (tests, compile, scripts)
- No architecture drift: do not introduce new frameworks or major design changes unless explicitly required
- No unrelated refactors
- All changes must be reproducible from a clean clone

---

## Project Structure

- docs/ → design, plans, architecture constraints
- plans/ → master plans
- phases/ → phase definitions
- tasks/ → executable task documents
- backends/ → CLI backend adapters
- agents/ → specialist agents
- runtime/ → orchestration, routing, state
- reports/ → execution reports (DO NOT MODIFY MANUALLY)
- state/runtime_state.json → runtime state (DO NOT COMMIT)

---

## Task Execution Rules

- Always operate from a task document when available
- Respect:
  - selected_backend
  - verification_profile
  - acceptance_criteria
- If a task conflicts with architecture constraints or phase scope:
  - STOP and report conflict

---

## Backend Rules

- Backends must:
  - execute commands deterministically
  - capture stdout, stderr, exit_code
  - not silently fail
- Do not invent backend interfaces; use existing adapters
- Codex CLI, Aider, Gemini, Claude Code should be invoked through backends only

---

## Verification Rules

- Verification must be deterministic
- Preferred checks:
  - pytest
  - python -m py_compile
- Do not rely on model self-evaluation

---

## Git Rules

- Do not commit:
  - runtime_state.json
  - reports/
  - logs/
  - virtual environments
- Do not modify .gitignore unless required by task
- Do not create excessive commits; prefer grouped logical commits

---

## Allowed Changes

- Implement task requirements
- Fix failing verification
- Update relevant tests
- Improve documentation tied to the task

---

## Forbidden Changes

- Changing architecture without explicit instruction
- Adding dependencies without justification
- Modifying unrelated files
- Deleting important files
- Bypassing verification

---

## Planning Rules

- Plans are multi-phase
- Completed sections are immutable
- Remaining sections may be updated
- Tasks must align with:
  - project brief
  - architecture constraints
  - active phase

---

## Reporting

- All executions must produce structured reports
- Reports must include:
  - changed files
  - verification results
  - assessment

---

## Behavior

- Do not ask unnecessary questions
- Do not stall execution
- Do not perform broad scans unless required
- Prefer direct action over analysis

---

## Priority Order

1. Architecture constraints
2. Task definition
3. Verification results
4. Plan guidance

If conflicts occur, follow this order.

## Run 2026-04-16T21:01:40
- Task ID: demo-self-improve
- Title: Refresh demo status log
- Phase: implementation
- Goal: Update docs/demo_status.md with the latest demo guidance
- Context: Collected 3 semantically relevant files; AGENTS.md guidance:
# AGENTS.md
## Purpose
This repository is operated by an autonomous multi-agent system (abracapocus_2).
All agents must follow these rules when modifying the codebase.
---
## Core Principles
- Minimal blast radius: only modify what is required for the task
- Deterministic verification: all changes must be verifiable via code (tests, compile, scripts)
- No architecture drift: do not introduce new frameworks or major design changes unless explicitly required
- No unrelated refactors
- All changes must be reproducible from a clean clone
---
## Project Structure
- docs/ → design, plans, architecture constraints
- plans/ → master plans
- phases/ → phase definitions
- tasks/ → executable task documents
- backends/ → CLI backend adapters
- agents/ → specialist agents
- runtime/ → orchestration, routing, state
...(truncated)

AGENTS.md guidance:
# AGENTS.md

## Purpose

This repository is operated by an autonomous multi-agent system (abracapocus_2).
All agents must follow these rules when modifying the codebase.

---

## Core Principles

- Minimal blast radius: only modify what is required for the task
- Deterministic verification: all changes must be verifiable via code (tests, compile, scripts)
- No architecture drift: do not introduce new frameworks or major design changes unless explicitly required
- No unrelated refactors
- All changes must be reproducible from a clean clone

---

## Project Structure

- docs/ → design, plans, architecture constraints
- plans/ → master plans
- phases/ → phase definitions
- tasks/ → executable task documents
- backends/ → CLI backend adapters
- agents/ → specialist agents
- runtime/ → orchestration, routing, state
- reports/ → execution reports (DO NOT MODIFY MANUALLY)
- state/runtime_state.json → runtime state (DO NOT COMMIT)

---

## Task Execution Rules

- Always operate from a task document when available
- Respect:
  - selected_backend
  - verification_profile
  - acceptance_criteria
- If a task conflicts with architecture constraints or phase scope:
  - STOP and report conflict

---

## Backend Rules

- Backends must:
  - execute commands deterministically
  - capture stdout, stderr, exit_code
  - not silently fail
- Do not invent backend interfaces; use existing adapters
- Codex CLI, Aider, Gemini, Claude Code should be invoked through backends only

---

## Verification Rules

- Verification must be deterministic
- Preferred checks:
  - pytest
  - python -m py_compile
- Do not rely on model self-evaluation

---

## Git Rules

- Do not commit:
  - runtime_state.json
  - reports/
  - logs/
  - virtual environments
- Do not modify .gitignore unless required by task
- Do not create excessive commits; prefer grouped logical commits

---

## Allowed Changes

- Implement task requirements
- Fix failing verification
- Update relevant tests
- Improve documentation tied to the task

---

## Forbidden Changes

- Changing architecture without explicit instruction
- Adding dependencies without justification
- Modifying unrelated files
- Deleting important files
- Bypassing verification

---

## Planning Rules

- Plans are multi-phase
- Completed sections are immutable
- Remaining sections may be updated
- Tasks must align with:
  - project brief
  - architecture constraints
  - active phase

---

## Reporting

- All executions must produce structured reports
- Reports must include:
  - changed files
  - verification results
  - assessment

---

## Behavior

- Do not ask unnecessary questions
- Do not stall execution
- Do not perform broad scans unless required
- Prefer direct action over analysis

---

## Priority Order

1. Architecture constraints
2. Task definition
3. Verification results
4. Plan guidance

If conflicts occur, follow this order.

## Run 2026-04-16T21:02:07
- Task ID: demo-self-improve
- Title: Refresh demo status log
- Phase: implementation
- Goal: Update docs/demo_status.md with the latest demo guidance
- Context: Collected 3 semantically relevant files; AGENTS.md guidance:
# AGENTS.md
## Purpose
This repository is operated by an autonomous multi-agent system (abracapocus_2).
All agents must follow these rules when modifying the codebase.
---
## Core Principles
- Minimal blast radius: only modify what is required for the task
- Deterministic verification: all changes must be verifiable via code (tests, compile, scripts)
- No architecture drift: do not introduce new frameworks or major design changes unless explicitly required
- No unrelated refactors
- All changes must be reproducible from a clean clone
---
## Project Structure
- docs/ → design, plans, architecture constraints
- plans/ → master plans
- phases/ → phase definitions
- tasks/ → executable task documents
- backends/ → CLI backend adapters
- agents/ → specialist agents
- runtime/ → orchestration, routing, state
...(truncated)

AGENTS.md guidance:
# AGENTS.md

## Purpose

This repository is operated by an autonomous multi-agent system (abracapocus_2).
All agents must follow these rules when modifying the codebase.

---

## Core Principles

- Minimal blast radius: only modify what is required for the task
- Deterministic verification: all changes must be verifiable via code (tests, compile, scripts)
- No architecture drift: do not introduce new frameworks or major design changes unless explicitly required
- No unrelated refactors
- All changes must be reproducible from a clean clone

---

## Project Structure

- docs/ → design, plans, architecture constraints
- plans/ → master plans
- phases/ → phase definitions
- tasks/ → executable task documents
- backends/ → CLI backend adapters
- agents/ → specialist agents
- runtime/ → orchestration, routing, state
- reports/ → execution reports (DO NOT MODIFY MANUALLY)
- state/runtime_state.json → runtime state (DO NOT COMMIT)

---

## Task Execution Rules

- Always operate from a task document when available
- Respect:
  - selected_backend
  - verification_profile
  - acceptance_criteria
- If a task conflicts with architecture constraints or phase scope:
  - STOP and report conflict

---

## Backend Rules

- Backends must:
  - execute commands deterministically
  - capture stdout, stderr, exit_code
  - not silently fail
- Do not invent backend interfaces; use existing adapters
- Codex CLI, Aider, Gemini, Claude Code should be invoked through backends only

---

## Verification Rules

- Verification must be deterministic
- Preferred checks:
  - pytest
  - python -m py_compile
- Do not rely on model self-evaluation

---

## Git Rules

- Do not commit:
  - runtime_state.json
  - reports/
  - logs/
  - virtual environments
- Do not modify .gitignore unless required by task
- Do not create excessive commits; prefer grouped logical commits

---

## Allowed Changes

- Implement task requirements
- Fix failing verification
- Update relevant tests
- Improve documentation tied to the task

---

## Forbidden Changes

- Changing architecture without explicit instruction
- Adding dependencies without justification
- Modifying unrelated files
- Deleting important files
- Bypassing verification

---

## Planning Rules

- Plans are multi-phase
- Completed sections are immutable
- Remaining sections may be updated
- Tasks must align with:
  - project brief
  - architecture constraints
  - active phase

---

## Reporting

- All executions must produce structured reports
- Reports must include:
  - changed files
  - verification results
  - assessment

---

## Behavior

- Do not ask unnecessary questions
- Do not stall execution
- Do not perform broad scans unless required
- Prefer direct action over analysis

---

## Priority Order

1. Architecture constraints
2. Task definition
3. Verification results
4. Plan guidance

If conflicts occur, follow this order.

## Run 2026-04-16T21:09:35
- Task ID: demo-self-improve
- Title: Refresh demo status log
- Phase: implementation
- Goal: Update docs/demo_status.md with the latest demo guidance
- Context: Collected 2 semantically relevant files; AGENTS.md guidance:
# AGENTS.md
## Purpose
This repository is operated by an autonomous multi-agent system (abracapocus_2).
All agents must follow these rules when modifying the codebase.
---
## Core Principles
- Minimal blast radius: only modify what is required for the task
- Deterministic verification: all changes must be verifiable via code (tests, compile, scripts)
- No architecture drift: do not introduce new frameworks or major design changes unless explicitly required
- No unrelated refactors
- All changes must be reproducible from a clean clone
---
## Project Structure
- docs/ → design, plans, architecture constraints
- plans/ → master plans
- phases/ → phase definitions
- tasks/ → executable task documents
- backends/ → CLI backend adapters
- agents/ → specialist agents
- runtime/ → orchestration, routing, state
...(truncated)

AGENTS.md guidance:
# AGENTS.md

## Purpose

This repository is operated by an autonomous multi-agent system (abracapocus_2).
All agents must follow these rules when modifying the codebase.

---

## Core Principles

- Minimal blast radius: only modify what is required for the task
- Deterministic verification: all changes must be verifiable via code (tests, compile, scripts)
- No architecture drift: do not introduce new frameworks or major design changes unless explicitly required
- No unrelated refactors
- All changes must be reproducible from a clean clone

---

## Project Structure

- docs/ → design, plans, architecture constraints
- plans/ → master plans
- phases/ → phase definitions
- tasks/ → executable task documents
- backends/ → CLI backend adapters
- agents/ → specialist agents
- runtime/ → orchestration, routing, state
- reports/ → execution reports (DO NOT MODIFY MANUALLY)
- state/runtime_state.json → runtime state (DO NOT COMMIT)

---

## Task Execution Rules

- Always operate from a task document when available
- Respect:
  - selected_backend
  - verification_profile
  - acceptance_criteria
- If a task conflicts with architecture constraints or phase scope:
  - STOP and report conflict

---

## Backend Rules

- Backends must:
  - execute commands deterministically
  - capture stdout, stderr, exit_code
  - not silently fail
- Do not invent backend interfaces; use existing adapters
- Codex CLI, Aider, Gemini, Claude Code should be invoked through backends only

---

## Verification Rules

- Verification must be deterministic
- Preferred checks:
  - pytest
  - python -m py_compile
- Do not rely on model self-evaluation

---

## Git Rules

- Do not commit:
  - runtime_state.json
  - reports/
  - logs/
  - virtual environments
- Do not modify .gitignore unless required by task
- Do not create excessive commits; prefer grouped logical commits

---

## Allowed Changes

- Implement task requirements
- Fix failing verification
- Update relevant tests
- Improve documentation tied to the task

---

## Forbidden Changes

- Changing architecture without explicit instruction
- Adding dependencies without justification
- Modifying unrelated files
- Deleting important files
- Bypassing verification

---

## Planning Rules

- Plans are multi-phase
- Completed sections are immutable
- Remaining sections may be updated
- Tasks must align with:
  - project brief
  - architecture constraints
  - active phase

---

## Reporting

- All executions must produce structured reports
- Reports must include:
  - changed files
  - verification results
  - assessment

---

## Behavior

- Do not ask unnecessary questions
- Do not stall execution
- Do not perform broad scans unless required
- Prefer direct action over analysis

---

## Priority Order

1. Architecture constraints
2. Task definition
3. Verification results
4. Plan guidance

If conflicts occur, follow this order.

## Run 2026-04-16T21:10:04
- Task ID: demo-self-improve
- Title: Refresh demo status log
- Phase: implementation
- Goal: Update docs/demo_status.md with the latest demo guidance
- Context: Collected 3 semantically relevant files; AGENTS.md guidance:
# AGENTS.md
## Purpose
This repository is operated by an autonomous multi-agent system (abracapocus_2).
All agents must follow these rules when modifying the codebase.
---
## Core Principles
- Minimal blast radius: only modify what is required for the task
- Deterministic verification: all changes must be verifiable via code (tests, compile, scripts)
- No architecture drift: do not introduce new frameworks or major design changes unless explicitly required
- No unrelated refactors
- All changes must be reproducible from a clean clone
---
## Project Structure
- docs/ → design, plans, architecture constraints
- plans/ → master plans
- phases/ → phase definitions
- tasks/ → executable task documents
- backends/ → CLI backend adapters
- agents/ → specialist agents
- runtime/ → orchestration, routing, state
...(truncated)

AGENTS.md guidance:
# AGENTS.md

## Purpose

This repository is operated by an autonomous multi-agent system (abracapocus_2).
All agents must follow these rules when modifying the codebase.

---

## Core Principles

- Minimal blast radius: only modify what is required for the task
- Deterministic verification: all changes must be verifiable via code (tests, compile, scripts)
- No architecture drift: do not introduce new frameworks or major design changes unless explicitly required
- No unrelated refactors
- All changes must be reproducible from a clean clone

---

## Project Structure

- docs/ → design, plans, architecture constraints
- plans/ → master plans
- phases/ → phase definitions
- tasks/ → executable task documents
- backends/ → CLI backend adapters
- agents/ → specialist agents
- runtime/ → orchestration, routing, state
- reports/ → execution reports (DO NOT MODIFY MANUALLY)
- state/runtime_state.json → runtime state (DO NOT COMMIT)

---

## Task Execution Rules

- Always operate from a task document when available
- Respect:
  - selected_backend
  - verification_profile
  - acceptance_criteria
- If a task conflicts with architecture constraints or phase scope:
  - STOP and report conflict

---

## Backend Rules

- Backends must:
  - execute commands deterministically
  - capture stdout, stderr, exit_code
  - not silently fail
- Do not invent backend interfaces; use existing adapters
- Codex CLI, Aider, Gemini, Claude Code should be invoked through backends only

---

## Verification Rules

- Verification must be deterministic
- Preferred checks:
  - pytest
  - python -m py_compile
- Do not rely on model self-evaluation

---

## Git Rules

- Do not commit:
  - runtime_state.json
  - reports/
  - logs/
  - virtual environments
- Do not modify .gitignore unless required by task
- Do not create excessive commits; prefer grouped logical commits

---

## Allowed Changes

- Implement task requirements
- Fix failing verification
- Update relevant tests
- Improve documentation tied to the task

---

## Forbidden Changes

- Changing architecture without explicit instruction
- Adding dependencies without justification
- Modifying unrelated files
- Deleting important files
- Bypassing verification

---

## Planning Rules

- Plans are multi-phase
- Completed sections are immutable
- Remaining sections may be updated
- Tasks must align with:
  - project brief
  - architecture constraints
  - active phase

---

## Reporting

- All executions must produce structured reports
- Reports must include:
  - changed files
  - verification results
  - assessment

---

## Behavior

- Do not ask unnecessary questions
- Do not stall execution
- Do not perform broad scans unless required
- Prefer direct action over analysis

---

## Priority Order

1. Architecture constraints
2. Task definition
3. Verification results
4. Plan guidance

If conflicts occur, follow this order.

## Run 2026-04-16T21:10:22
- Task ID: demo-self-improve
- Title: Refresh demo status log
- Phase: implementation
- Goal: Update docs/demo_status.md with the latest demo guidance
- Context: Collected 3 semantically relevant files; AGENTS.md guidance:
# AGENTS.md
## Purpose
This repository is operated by an autonomous multi-agent system (abracapocus_2).
All agents must follow these rules when modifying the codebase.
---
## Core Principles
- Minimal blast radius: only modify what is required for the task
- Deterministic verification: all changes must be verifiable via code (tests, compile, scripts)
- No architecture drift: do not introduce new frameworks or major design changes unless explicitly required
- No unrelated refactors
- All changes must be reproducible from a clean clone
---
## Project Structure
- docs/ → design, plans, architecture constraints
- plans/ → master plans
- phases/ → phase definitions
- tasks/ → executable task documents
- backends/ → CLI backend adapters
- agents/ → specialist agents
- runtime/ → orchestration, routing, state
...(truncated)

AGENTS.md guidance:
# AGENTS.md

## Purpose

This repository is operated by an autonomous multi-agent system (abracapocus_2).
All agents must follow these rules when modifying the codebase.

---

## Core Principles

- Minimal blast radius: only modify what is required for the task
- Deterministic verification: all changes must be verifiable via code (tests, compile, scripts)
- No architecture drift: do not introduce new frameworks or major design changes unless explicitly required
- No unrelated refactors
- All changes must be reproducible from a clean clone

---

## Project Structure

- docs/ → design, plans, architecture constraints
- plans/ → master plans
- phases/ → phase definitions
- tasks/ → executable task documents
- backends/ → CLI backend adapters
- agents/ → specialist agents
- runtime/ → orchestration, routing, state
- reports/ → execution reports (DO NOT MODIFY MANUALLY)
- state/runtime_state.json → runtime state (DO NOT COMMIT)

---

## Task Execution Rules

- Always operate from a task document when available
- Respect:
  - selected_backend
  - verification_profile
  - acceptance_criteria
- If a task conflicts with architecture constraints or phase scope:
  - STOP and report conflict

---

## Backend Rules

- Backends must:
  - execute commands deterministically
  - capture stdout, stderr, exit_code
  - not silently fail
- Do not invent backend interfaces; use existing adapters
- Codex CLI, Aider, Gemini, Claude Code should be invoked through backends only

---

## Verification Rules

- Verification must be deterministic
- Preferred checks:
  - pytest
  - python -m py_compile
- Do not rely on model self-evaluation

---

## Git Rules

- Do not commit:
  - runtime_state.json
  - reports/
  - logs/
  - virtual environments
- Do not modify .gitignore unless required by task
- Do not create excessive commits; prefer grouped logical commits

---

## Allowed Changes

- Implement task requirements
- Fix failing verification
- Update relevant tests
- Improve documentation tied to the task

---

## Forbidden Changes

- Changing architecture without explicit instruction
- Adding dependencies without justification
- Modifying unrelated files
- Deleting important files
- Bypassing verification

---

## Planning Rules

- Plans are multi-phase
- Completed sections are immutable
- Remaining sections may be updated
- Tasks must align with:
  - project brief
  - architecture constraints
  - active phase

---

## Reporting

- All executions must produce structured reports
- Reports must include:
  - changed files
  - verification results
  - assessment

---

## Behavior

- Do not ask unnecessary questions
- Do not stall execution
- Do not perform broad scans unless required
- Prefer direct action over analysis

---

## Priority Order

1. Architecture constraints
2. Task definition
3. Verification results
4. Plan guidance

If conflicts occur, follow this order.

## Run 2026-04-16T21:13:23
- Task ID: demo-self-improve
- Title: Refresh demo status log
- Phase: implementation
- Goal: Update docs/demo_status.md with the latest demo guidance
- Context: Collected 2 semantically relevant files; AGENTS.md guidance:
# AGENTS.md
## Purpose
This repository is operated by an autonomous multi-agent system (abracapocus_2).
All agents must follow these rules when modifying the codebase.
---
## Core Principles
- Minimal blast radius: only modify what is required for the task
- Deterministic verification: all changes must be verifiable via code (tests, compile, scripts)
- No architecture drift: do not introduce new frameworks or major design changes unless explicitly required
- No unrelated refactors
- All changes must be reproducible from a clean clone
---
## Project Structure
- docs/ → design, plans, architecture constraints
- plans/ → master plans
- phases/ → phase definitions
- tasks/ → executable task documents
- backends/ → CLI backend adapters
- agents/ → specialist agents
- runtime/ → orchestration, routing, state
...(truncated)

AGENTS.md guidance:
# AGENTS.md

## Purpose

This repository is operated by an autonomous multi-agent system (abracapocus_2).
All agents must follow these rules when modifying the codebase.

---

## Core Principles

- Minimal blast radius: only modify what is required for the task
- Deterministic verification: all changes must be verifiable via code (tests, compile, scripts)
- No architecture drift: do not introduce new frameworks or major design changes unless explicitly required
- No unrelated refactors
- All changes must be reproducible from a clean clone

---

## Project Structure

- docs/ → design, plans, architecture constraints
- plans/ → master plans
- phases/ → phase definitions
- tasks/ → executable task documents
- backends/ → CLI backend adapters
- agents/ → specialist agents
- runtime/ → orchestration, routing, state
- reports/ → execution reports (DO NOT MODIFY MANUALLY)
- state/runtime_state.json → runtime state (DO NOT COMMIT)

---

## Task Execution Rules

- Always operate from a task document when available
- Respect:
  - selected_backend
  - verification_profile
  - acceptance_criteria
- If a task conflicts with architecture constraints or phase scope:
  - STOP and report conflict

---

## Backend Rules

- Backends must:
  - execute commands deterministically
  - capture stdout, stderr, exit_code
  - not silently fail
- Do not invent backend interfaces; use existing adapters
- Codex CLI, Aider, Gemini, Claude Code should be invoked through backends only

---

## Verification Rules

- Verification must be deterministic
- Preferred checks:
  - pytest
  - python -m py_compile
- Do not rely on model self-evaluation

---

## Git Rules

- Do not commit:
  - runtime_state.json
  - reports/
  - logs/
  - virtual environments
- Do not modify .gitignore unless required by task
- Do not create excessive commits; prefer grouped logical commits

---

## Allowed Changes

- Implement task requirements
- Fix failing verification
- Update relevant tests
- Improve documentation tied to the task

---

## Forbidden Changes

- Changing architecture without explicit instruction
- Adding dependencies without justification
- Modifying unrelated files
- Deleting important files
- Bypassing verification

---

## Planning Rules

- Plans are multi-phase
- Completed sections are immutable
- Remaining sections may be updated
- Tasks must align with:
  - project brief
  - architecture constraints
  - active phase

---

## Reporting

- All executions must produce structured reports
- Reports must include:
  - changed files
  - verification results
  - assessment

---

## Behavior

- Do not ask unnecessary questions
- Do not stall execution
- Do not perform broad scans unless required
- Prefer direct action over analysis

---

## Priority Order

1. Architecture constraints
2. Task definition
3. Verification results
4. Plan guidance

If conflicts occur, follow this order.

## Run 2026-04-16T21:14:22
- Task ID: demo-self-improve
- Title: Refresh demo status log
- Phase: implementation
- Goal: Update docs/demo_status.md with the latest demo guidance
- Context: Collected 3 semantically relevant files; AGENTS.md guidance:
# AGENTS.md
## Purpose
This repository is operated by an autonomous multi-agent system (abracapocus_2).
All agents must follow these rules when modifying the codebase.
---
## Core Principles
- Minimal blast radius: only modify what is required for the task
- Deterministic verification: all changes must be verifiable via code (tests, compile, scripts)
- No architecture drift: do not introduce new frameworks or major design changes unless explicitly required
- No unrelated refactors
- All changes must be reproducible from a clean clone
---
## Project Structure
- docs/ → design, plans, architecture constraints
- plans/ → master plans
- phases/ → phase definitions
- tasks/ → executable task documents
- backends/ → CLI backend adapters
- agents/ → specialist agents
- runtime/ → orchestration, routing, state
...(truncated)

AGENTS.md guidance:
# AGENTS.md

## Purpose

This repository is operated by an autonomous multi-agent system (abracapocus_2).
All agents must follow these rules when modifying the codebase.

---

## Core Principles

- Minimal blast radius: only modify what is required for the task
- Deterministic verification: all changes must be verifiable via code (tests, compile, scripts)
- No architecture drift: do not introduce new frameworks or major design changes unless explicitly required
- No unrelated refactors
- All changes must be reproducible from a clean clone

---

## Project Structure

- docs/ → design, plans, architecture constraints
- plans/ → master plans
- phases/ → phase definitions
- tasks/ → executable task documents
- backends/ → CLI backend adapters
- agents/ → specialist agents
- runtime/ → orchestration, routing, state
- reports/ → execution reports (DO NOT MODIFY MANUALLY)
- state/runtime_state.json → runtime state (DO NOT COMMIT)

---

## Task Execution Rules

- Always operate from a task document when available
- Respect:
  - selected_backend
  - verification_profile
  - acceptance_criteria
- If a task conflicts with architecture constraints or phase scope:
  - STOP and report conflict

---

## Backend Rules

- Backends must:
  - execute commands deterministically
  - capture stdout, stderr, exit_code
  - not silently fail
- Do not invent backend interfaces; use existing adapters
- Codex CLI, Aider, Gemini, Claude Code should be invoked through backends only

---

## Verification Rules

- Verification must be deterministic
- Preferred checks:
  - pytest
  - python -m py_compile
- Do not rely on model self-evaluation

---

## Git Rules

- Do not commit:
  - runtime_state.json
  - reports/
  - logs/
  - virtual environments
- Do not modify .gitignore unless required by task
- Do not create excessive commits; prefer grouped logical commits

---

## Allowed Changes

- Implement task requirements
- Fix failing verification
- Update relevant tests
- Improve documentation tied to the task

---

## Forbidden Changes

- Changing architecture without explicit instruction
- Adding dependencies without justification
- Modifying unrelated files
- Deleting important files
- Bypassing verification

---

## Planning Rules

- Plans are multi-phase
- Completed sections are immutable
- Remaining sections may be updated
- Tasks must align with:
  - project brief
  - architecture constraints
  - active phase

---

## Reporting

- All executions must produce structured reports
- Reports must include:
  - changed files
  - verification results
  - assessment

---

## Behavior

- Do not ask unnecessary questions
- Do not stall execution
- Do not perform broad scans unless required
- Prefer direct action over analysis

---

## Priority Order

1. Architecture constraints
2. Task definition
3. Verification results
4. Plan guidance

If conflicts occur, follow this order.

## Run 2026-04-16T21:14:53
- Task ID: demo-self-improve
- Title: Refresh demo status log
- Phase: implementation
- Goal: Update docs/demo_status.md with the latest demo guidance
- Context: Collected 3 semantically relevant files; AGENTS.md guidance:
# AGENTS.md
## Purpose
This repository is operated by an autonomous multi-agent system (abracapocus_2).
All agents must follow these rules when modifying the codebase.
---
## Core Principles
- Minimal blast radius: only modify what is required for the task
- Deterministic verification: all changes must be verifiable via code (tests, compile, scripts)
- No architecture drift: do not introduce new frameworks or major design changes unless explicitly required
- No unrelated refactors
- All changes must be reproducible from a clean clone
---
## Project Structure
- docs/ → design, plans, architecture constraints
- plans/ → master plans
- phases/ → phase definitions
- tasks/ → executable task documents
- backends/ → CLI backend adapters
- agents/ → specialist agents
- runtime/ → orchestration, routing, state
...(truncated)

AGENTS.md guidance:
# AGENTS.md

## Purpose

This repository is operated by an autonomous multi-agent system (abracapocus_2).
All agents must follow these rules when modifying the codebase.

---

## Core Principles

- Minimal blast radius: only modify what is required for the task
- Deterministic verification: all changes must be verifiable via code (tests, compile, scripts)
- No architecture drift: do not introduce new frameworks or major design changes unless explicitly required
- No unrelated refactors
- All changes must be reproducible from a clean clone

---

## Project Structure

- docs/ → design, plans, architecture constraints
- plans/ → master plans
- phases/ → phase definitions
- tasks/ → executable task documents
- backends/ → CLI backend adapters
- agents/ → specialist agents
- runtime/ → orchestration, routing, state
- reports/ → execution reports (DO NOT MODIFY MANUALLY)
- state/runtime_state.json → runtime state (DO NOT COMMIT)

---

## Task Execution Rules

- Always operate from a task document when available
- Respect:
  - selected_backend
  - verification_profile
  - acceptance_criteria
- If a task conflicts with architecture constraints or phase scope:
  - STOP and report conflict

---

## Backend Rules

- Backends must:
  - execute commands deterministically
  - capture stdout, stderr, exit_code
  - not silently fail
- Do not invent backend interfaces; use existing adapters
- Codex CLI, Aider, Gemini, Claude Code should be invoked through backends only

---

## Verification Rules

- Verification must be deterministic
- Preferred checks:
  - pytest
  - python -m py_compile
- Do not rely on model self-evaluation

---

## Git Rules

- Do not commit:
  - runtime_state.json
  - reports/
  - logs/
  - virtual environments
- Do not modify .gitignore unless required by task
- Do not create excessive commits; prefer grouped logical commits

---

## Allowed Changes

- Implement task requirements
- Fix failing verification
- Update relevant tests
- Improve documentation tied to the task

---

## Forbidden Changes

- Changing architecture without explicit instruction
- Adding dependencies without justification
- Modifying unrelated files
- Deleting important files
- Bypassing verification

---

## Planning Rules

- Plans are multi-phase
- Completed sections are immutable
- Remaining sections may be updated
- Tasks must align with:
  - project brief
  - architecture constraints
  - active phase

---

## Reporting

- All executions must produce structured reports
- Reports must include:
  - changed files
  - verification results
  - assessment

---

## Behavior

- Do not ask unnecessary questions
- Do not stall execution
- Do not perform broad scans unless required
- Prefer direct action over analysis

---

## Priority Order

1. Architecture constraints
2. Task definition
3. Verification results
4. Plan guidance

If conflicts occur, follow this order.

## Run 2026-04-16T21:15:16
- Task ID: demo-self-improve
- Title: Refresh demo status log
- Phase: implementation
- Goal: Update docs/demo_status.md with the latest demo guidance
- Context: Collected 2 semantically relevant files; AGENTS.md guidance:
# AGENTS.md
## Purpose
This repository is operated by an autonomous multi-agent system (abracapocus_2).
All agents must follow these rules when modifying the codebase.
---
## Core Principles
- Minimal blast radius: only modify what is required for the task
- Deterministic verification: all changes must be verifiable via code (tests, compile, scripts)
- No architecture drift: do not introduce new frameworks or major design changes unless explicitly required
- No unrelated refactors
- All changes must be reproducible from a clean clone
---
## Project Structure
- docs/ → design, plans, architecture constraints
- plans/ → master plans
- phases/ → phase definitions
- tasks/ → executable task documents
- backends/ → CLI backend adapters
- agents/ → specialist agents
- runtime/ → orchestration, routing, state
...(truncated)

AGENTS.md guidance:
# AGENTS.md

## Purpose

This repository is operated by an autonomous multi-agent system (abracapocus_2).
All agents must follow these rules when modifying the codebase.

---

## Core Principles

- Minimal blast radius: only modify what is required for the task
- Deterministic verification: all changes must be verifiable via code (tests, compile, scripts)
- No architecture drift: do not introduce new frameworks or major design changes unless explicitly required
- No unrelated refactors
- All changes must be reproducible from a clean clone

---

## Project Structure

- docs/ → design, plans, architecture constraints
- plans/ → master plans
- phases/ → phase definitions
- tasks/ → executable task documents
- backends/ → CLI backend adapters
- agents/ → specialist agents
- runtime/ → orchestration, routing, state
- reports/ → execution reports (DO NOT MODIFY MANUALLY)
- state/runtime_state.json → runtime state (DO NOT COMMIT)

---

## Task Execution Rules

- Always operate from a task document when available
- Respect:
  - selected_backend
  - verification_profile
  - acceptance_criteria
- If a task conflicts with architecture constraints or phase scope:
  - STOP and report conflict

---

## Backend Rules

- Backends must:
  - execute commands deterministically
  - capture stdout, stderr, exit_code
  - not silently fail
- Do not invent backend interfaces; use existing adapters
- Codex CLI, Aider, Gemini, Claude Code should be invoked through backends only

---

## Verification Rules

- Verification must be deterministic
- Preferred checks:
  - pytest
  - python -m py_compile
- Do not rely on model self-evaluation

---

## Git Rules

- Do not commit:
  - runtime_state.json
  - reports/
  - logs/
  - virtual environments
- Do not modify .gitignore unless required by task
- Do not create excessive commits; prefer grouped logical commits

---

## Allowed Changes

- Implement task requirements
- Fix failing verification
- Update relevant tests
- Improve documentation tied to the task

---

## Forbidden Changes

- Changing architecture without explicit instruction
- Adding dependencies without justification
- Modifying unrelated files
- Deleting important files
- Bypassing verification

---

## Planning Rules

- Plans are multi-phase
- Completed sections are immutable
- Remaining sections may be updated
- Tasks must align with:
  - project brief
  - architecture constraints
  - active phase

---

## Reporting

- All executions must produce structured reports
- Reports must include:
  - changed files
  - verification results
  - assessment

---

## Behavior

- Do not ask unnecessary questions
- Do not stall execution
- Do not perform broad scans unless required
- Prefer direct action over analysis

---

## Priority Order

1. Architecture constraints
2. Task definition
3. Verification results
4. Plan guidance

If conflicts occur, follow this order.

## Run 2026-04-16T21:22:13
- Task ID: demo-self-improve
- Title: Refresh demo status log
- Phase: implementation
- Goal: Update docs/demo_status.md with the latest demo guidance
- Context: Collected 2 semantically relevant files; AGENTS.md guidance:
# AGENTS.md
## Purpose
This repository is operated by an autonomous multi-agent system (abracapocus_2).
All agents must follow these rules when modifying the codebase.
---
## Core Principles
- Minimal blast radius: only modify what is required for the task
- Deterministic verification: all changes must be verifiable via code (tests, compile, scripts)
- No architecture drift: do not introduce new frameworks or major design changes unless explicitly required
- No unrelated refactors
- All changes must be reproducible from a clean clone
---
## Project Structure
- docs/ → design, plans, architecture constraints
- plans/ → master plans
- phases/ → phase definitions
- tasks/ → executable task documents
- backends/ → CLI backend adapters
- agents/ → specialist agents
- runtime/ → orchestration, routing, state
...(truncated)

AGENTS.md guidance:
# AGENTS.md

## Purpose

This repository is operated by an autonomous multi-agent system (abracapocus_2).
All agents must follow these rules when modifying the codebase.

---

## Core Principles

- Minimal blast radius: only modify what is required for the task
- Deterministic verification: all changes must be verifiable via code (tests, compile, scripts)
- No architecture drift: do not introduce new frameworks or major design changes unless explicitly required
- No unrelated refactors
- All changes must be reproducible from a clean clone

---

## Project Structure

- docs/ → design, plans, architecture constraints
- plans/ → master plans
- phases/ → phase definitions
- tasks/ → executable task documents
- backends/ → CLI backend adapters
- agents/ → specialist agents
- runtime/ → orchestration, routing, state
- reports/ → execution reports (DO NOT MODIFY MANUALLY)
- state/runtime_state.json → runtime state (DO NOT COMMIT)

---

## Task Execution Rules

- Always operate from a task document when available
- Respect:
  - selected_backend
  - verification_profile
  - acceptance_criteria
- If a task conflicts with architecture constraints or phase scope:
  - STOP and report conflict

---

## Backend Rules

- Backends must:
  - execute commands deterministically
  - capture stdout, stderr, exit_code
  - not silently fail
- Do not invent backend interfaces; use existing adapters
- Codex CLI, Aider, Gemini, Claude Code should be invoked through backends only

---

## Verification Rules

- Verification must be deterministic
- Preferred checks:
  - pytest
  - python -m py_compile
- Do not rely on model self-evaluation

---

## Git Rules

- Do not commit:
  - runtime_state.json
  - reports/
  - logs/
  - virtual environments
- Do not modify .gitignore unless required by task
- Do not create excessive commits; prefer grouped logical commits

---

## Allowed Changes

- Implement task requirements
- Fix failing verification
- Update relevant tests
- Improve documentation tied to the task

---

## Forbidden Changes

- Changing architecture without explicit instruction
- Adding dependencies without justification
- Modifying unrelated files
- Deleting important files
- Bypassing verification

---

## Planning Rules

- Plans are multi-phase
- Completed sections are immutable
- Remaining sections may be updated
- Tasks must align with:
  - project brief
  - architecture constraints
  - active phase

---

## Reporting

- All executions must produce structured reports
- Reports must include:
  - changed files
  - verification results
  - assessment

---

## Behavior

- Do not ask unnecessary questions
- Do not stall execution
- Do not perform broad scans unless required
- Prefer direct action over analysis

---

## Priority Order

1. Architecture constraints
2. Task definition
3. Verification results
4. Plan guidance

If conflicts occur, follow this order.

## Run 2026-04-16T21:22:44
- Task ID: demo-self-improve
- Title: Refresh demo status log
- Phase: implementation
- Goal: Update docs/demo_status.md with the latest demo guidance
- Context: Collected 3 semantically relevant files; AGENTS.md guidance:
# AGENTS.md
## Purpose
This repository is operated by an autonomous multi-agent system (abracapocus_2).
All agents must follow these rules when modifying the codebase.
---
## Core Principles
- Minimal blast radius: only modify what is required for the task
- Deterministic verification: all changes must be verifiable via code (tests, compile, scripts)
- No architecture drift: do not introduce new frameworks or major design changes unless explicitly required
- No unrelated refactors
- All changes must be reproducible from a clean clone
---
## Project Structure
- docs/ → design, plans, architecture constraints
- plans/ → master plans
- phases/ → phase definitions
- tasks/ → executable task documents
- backends/ → CLI backend adapters
- agents/ → specialist agents
- runtime/ → orchestration, routing, state
...(truncated)

AGENTS.md guidance:
# AGENTS.md

## Purpose

This repository is operated by an autonomous multi-agent system (abracapocus_2).
All agents must follow these rules when modifying the codebase.

---

## Core Principles

- Minimal blast radius: only modify what is required for the task
- Deterministic verification: all changes must be verifiable via code (tests, compile, scripts)
- No architecture drift: do not introduce new frameworks or major design changes unless explicitly required
- No unrelated refactors
- All changes must be reproducible from a clean clone

---

## Project Structure

- docs/ → design, plans, architecture constraints
- plans/ → master plans
- phases/ → phase definitions
- tasks/ → executable task documents
- backends/ → CLI backend adapters
- agents/ → specialist agents
- runtime/ → orchestration, routing, state
- reports/ → execution reports (DO NOT MODIFY MANUALLY)
- state/runtime_state.json → runtime state (DO NOT COMMIT)

---

## Task Execution Rules

- Always operate from a task document when available
- Respect:
  - selected_backend
  - verification_profile
  - acceptance_criteria
- If a task conflicts with architecture constraints or phase scope:
  - STOP and report conflict

---

## Backend Rules

- Backends must:
  - execute commands deterministically
  - capture stdout, stderr, exit_code
  - not silently fail
- Do not invent backend interfaces; use existing adapters
- Codex CLI, Aider, Gemini, Claude Code should be invoked through backends only

---

## Verification Rules

- Verification must be deterministic
- Preferred checks:
  - pytest
  - python -m py_compile
- Do not rely on model self-evaluation

---

## Git Rules

- Do not commit:
  - runtime_state.json
  - reports/
  - logs/
  - virtual environments
- Do not modify .gitignore unless required by task
- Do not create excessive commits; prefer grouped logical commits

---

## Allowed Changes

- Implement task requirements
- Fix failing verification
- Update relevant tests
- Improve documentation tied to the task

---

## Forbidden Changes

- Changing architecture without explicit instruction
- Adding dependencies without justification
- Modifying unrelated files
- Deleting important files
- Bypassing verification

---

## Planning Rules

- Plans are multi-phase
- Completed sections are immutable
- Remaining sections may be updated
- Tasks must align with:
  - project brief
  - architecture constraints
  - active phase

---

## Reporting

- All executions must produce structured reports
- Reports must include:
  - changed files
  - verification results
  - assessment

---

## Behavior

- Do not ask unnecessary questions
- Do not stall execution
- Do not perform broad scans unless required
- Prefer direct action over analysis

---

## Priority Order

1. Architecture constraints
2. Task definition
3. Verification results
4. Plan guidance

If conflicts occur, follow this order.

## Run 2026-04-16T21:23:04
- Task ID: demo-self-improve
- Title: Refresh demo status log
- Phase: implementation
- Goal: Update docs/demo_status.md with the latest demo guidance
- Context: Collected 2 semantically relevant files; AGENTS.md guidance:
# AGENTS.md
## Purpose
This repository is operated by an autonomous multi-agent system (abracapocus_2).
All agents must follow these rules when modifying the codebase.
---
## Core Principles
- Minimal blast radius: only modify what is required for the task
- Deterministic verification: all changes must be verifiable via code (tests, compile, scripts)
- No architecture drift: do not introduce new frameworks or major design changes unless explicitly required
- No unrelated refactors
- All changes must be reproducible from a clean clone
---
## Project Structure
- docs/ → design, plans, architecture constraints
- plans/ → master plans
- phases/ → phase definitions
- tasks/ → executable task documents
- backends/ → CLI backend adapters
- agents/ → specialist agents
- runtime/ → orchestration, routing, state
...(truncated)

AGENTS.md guidance:
# AGENTS.md

## Purpose

This repository is operated by an autonomous multi-agent system (abracapocus_2).
All agents must follow these rules when modifying the codebase.

---

## Core Principles

- Minimal blast radius: only modify what is required for the task
- Deterministic verification: all changes must be verifiable via code (tests, compile, scripts)
- No architecture drift: do not introduce new frameworks or major design changes unless explicitly required
- No unrelated refactors
- All changes must be reproducible from a clean clone

---

## Project Structure

- docs/ → design, plans, architecture constraints
- plans/ → master plans
- phases/ → phase definitions
- tasks/ → executable task documents
- backends/ → CLI backend adapters
- agents/ → specialist agents
- runtime/ → orchestration, routing, state
- reports/ → execution reports (DO NOT MODIFY MANUALLY)
- state/runtime_state.json → runtime state (DO NOT COMMIT)

---

## Task Execution Rules

- Always operate from a task document when available
- Respect:
  - selected_backend
  - verification_profile
  - acceptance_criteria
- If a task conflicts with architecture constraints or phase scope:
  - STOP and report conflict

---

## Backend Rules

- Backends must:
  - execute commands deterministically
  - capture stdout, stderr, exit_code
  - not silently fail
- Do not invent backend interfaces; use existing adapters
- Codex CLI, Aider, Gemini, Claude Code should be invoked through backends only

---

## Verification Rules

- Verification must be deterministic
- Preferred checks:
  - pytest
  - python -m py_compile
- Do not rely on model self-evaluation

---

## Git Rules

- Do not commit:
  - runtime_state.json
  - reports/
  - logs/
  - virtual environments
- Do not modify .gitignore unless required by task
- Do not create excessive commits; prefer grouped logical commits

---

## Allowed Changes

- Implement task requirements
- Fix failing verification
- Update relevant tests
- Improve documentation tied to the task

---

## Forbidden Changes

- Changing architecture without explicit instruction
- Adding dependencies without justification
- Modifying unrelated files
- Deleting important files
- Bypassing verification

---

## Planning Rules

- Plans are multi-phase
- Completed sections are immutable
- Remaining sections may be updated
- Tasks must align with:
  - project brief
  - architecture constraints
  - active phase

---

## Reporting

- All executions must produce structured reports
- Reports must include:
  - changed files
  - verification results
  - assessment

---

## Behavior

- Do not ask unnecessary questions
- Do not stall execution
- Do not perform broad scans unless required
- Prefer direct action over analysis

---

## Priority Order

1. Architecture constraints
2. Task definition
3. Verification results
4. Plan guidance

If conflicts occur, follow this order.

## Run 2026-04-16T21:24:09
- Task ID: demo-self-improve
- Title: Refresh demo status log
- Phase: implementation
- Goal: Update docs/demo_status.md with the latest demo guidance
- Context: Collected 4 semantically relevant files; AGENTS.md guidance:
# AGENTS.md
## Purpose
This repository is operated by an autonomous multi-agent system (abracapocus_2).
All agents must follow these rules when modifying the codebase.
---
## Core Principles
- Minimal blast radius: only modify what is required for the task
- Deterministic verification: all changes must be verifiable via code (tests, compile, scripts)
- No architecture drift: do not introduce new frameworks or major design changes unless explicitly required
- No unrelated refactors
- All changes must be reproducible from a clean clone
---
## Project Structure
- docs/ → design, plans, architecture constraints
- plans/ → master plans
- phases/ → phase definitions
- tasks/ → executable task documents
- backends/ → CLI backend adapters
- agents/ → specialist agents
- runtime/ → orchestration, routing, state
...(truncated)

AGENTS.md guidance:
# AGENTS.md

## Purpose

This repository is operated by an autonomous multi-agent system (abracapocus_2).
All agents must follow these rules when modifying the codebase.

---

## Core Principles

- Minimal blast radius: only modify what is required for the task
- Deterministic verification: all changes must be verifiable via code (tests, compile, scripts)
- No architecture drift: do not introduce new frameworks or major design changes unless explicitly required
- No unrelated refactors
- All changes must be reproducible from a clean clone

---

## Project Structure

- docs/ → design, plans, architecture constraints
- plans/ → master plans
- phases/ → phase definitions
- tasks/ → executable task documents
- backends/ → CLI backend adapters
- agents/ → specialist agents
- runtime/ → orchestration, routing, state
- reports/ → execution reports (DO NOT MODIFY MANUALLY)
- state/runtime_state.json → runtime state (DO NOT COMMIT)

---

## Task Execution Rules

- Always operate from a task document when available
- Respect:
  - selected_backend
  - verification_profile
  - acceptance_criteria
- If a task conflicts with architecture constraints or phase scope:
  - STOP and report conflict

---

## Backend Rules

- Backends must:
  - execute commands deterministically
  - capture stdout, stderr, exit_code
  - not silently fail
- Do not invent backend interfaces; use existing adapters
- Codex CLI, Aider, Gemini, Claude Code should be invoked through backends only

---

## Verification Rules

- Verification must be deterministic
- Preferred checks:
  - pytest
  - python -m py_compile
- Do not rely on model self-evaluation

---

## Git Rules

- Do not commit:
  - runtime_state.json
  - reports/
  - logs/
  - virtual environments
- Do not modify .gitignore unless required by task
- Do not create excessive commits; prefer grouped logical commits

---

## Allowed Changes

- Implement task requirements
- Fix failing verification
- Update relevant tests
- Improve documentation tied to the task

---

## Forbidden Changes

- Changing architecture without explicit instruction
- Adding dependencies without justification
- Modifying unrelated files
- Deleting important files
- Bypassing verification

---

## Planning Rules

- Plans are multi-phase
- Completed sections are immutable
- Remaining sections may be updated
- Tasks must align with:
  - project brief
  - architecture constraints
  - active phase

---

## Reporting

- All executions must produce structured reports
- Reports must include:
  - changed files
  - verification results
  - assessment

---

## Behavior

- Do not ask unnecessary questions
- Do not stall execution
- Do not perform broad scans unless required
- Prefer direct action over analysis

---

## Priority Order

1. Architecture constraints
2. Task definition
3. Verification results
4. Plan guidance

If conflicts occur, follow this order.

## Run 2026-04-16T21:24:53
- Task ID: demo-self-improve
- Title: Refresh demo status log
- Phase: implementation
- Goal: Update docs/demo_status.md with the latest demo guidance
- Context: Collected 2 semantically relevant files; AGENTS.md guidance:
# AGENTS.md
## Purpose
This repository is operated by an autonomous multi-agent system (abracapocus_2).
All agents must follow these rules when modifying the codebase.
---
## Core Principles
- Minimal blast radius: only modify what is required for the task
- Deterministic verification: all changes must be verifiable via code (tests, compile, scripts)
- No architecture drift: do not introduce new frameworks or major design changes unless explicitly required
- No unrelated refactors
- All changes must be reproducible from a clean clone
---
## Project Structure
- docs/ → design, plans, architecture constraints
- plans/ → master plans
- phases/ → phase definitions
- tasks/ → executable task documents
- backends/ → CLI backend adapters
- agents/ → specialist agents
- runtime/ → orchestration, routing, state
...(truncated)

AGENTS.md guidance:
# AGENTS.md

## Purpose

This repository is operated by an autonomous multi-agent system (abracapocus_2).
All agents must follow these rules when modifying the codebase.

---

## Core Principles

- Minimal blast radius: only modify what is required for the task
- Deterministic verification: all changes must be verifiable via code (tests, compile, scripts)
- No architecture drift: do not introduce new frameworks or major design changes unless explicitly required
- No unrelated refactors
- All changes must be reproducible from a clean clone

---

## Project Structure

- docs/ → design, plans, architecture constraints
- plans/ → master plans
- phases/ → phase definitions
- tasks/ → executable task documents
- backends/ → CLI backend adapters
- agents/ → specialist agents
- runtime/ → orchestration, routing, state
- reports/ → execution reports (DO NOT MODIFY MANUALLY)
- state/runtime_state.json → runtime state (DO NOT COMMIT)

---

## Task Execution Rules

- Always operate from a task document when available
- Respect:
  - selected_backend
  - verification_profile
  - acceptance_criteria
- If a task conflicts with architecture constraints or phase scope:
  - STOP and report conflict

---

## Backend Rules

- Backends must:
  - execute commands deterministically
  - capture stdout, stderr, exit_code
  - not silently fail
- Do not invent backend interfaces; use existing adapters
- Codex CLI, Aider, Gemini, Claude Code should be invoked through backends only

---

## Verification Rules

- Verification must be deterministic
- Preferred checks:
  - pytest
  - python -m py_compile
- Do not rely on model self-evaluation

---

## Git Rules

- Do not commit:
  - runtime_state.json
  - reports/
  - logs/
  - virtual environments
- Do not modify .gitignore unless required by task
- Do not create excessive commits; prefer grouped logical commits

---

## Allowed Changes

- Implement task requirements
- Fix failing verification
- Update relevant tests
- Improve documentation tied to the task

---

## Forbidden Changes

- Changing architecture without explicit instruction
- Adding dependencies without justification
- Modifying unrelated files
- Deleting important files
- Bypassing verification

---

## Planning Rules

- Plans are multi-phase
- Completed sections are immutable
- Remaining sections may be updated
- Tasks must align with:
  - project brief
  - architecture constraints
  - active phase

---

## Reporting

- All executions must produce structured reports
- Reports must include:
  - changed files
  - verification results
  - assessment

---

## Behavior

- Do not ask unnecessary questions
- Do not stall execution
- Do not perform broad scans unless required
- Prefer direct action over analysis

---

## Priority Order

1. Architecture constraints
2. Task definition
3. Verification results
4. Plan guidance

If conflicts occur, follow this order.

## Run 2026-04-16T21:25:17
- Task ID: demo-self-improve
- Title: Refresh demo status log
- Phase: implementation
- Goal: Update docs/demo_status.md with the latest demo guidance
- Context: Collected 2 semantically relevant files; AGENTS.md guidance:
# AGENTS.md
## Purpose
This repository is operated by an autonomous multi-agent system (abracapocus_2).
All agents must follow these rules when modifying the codebase.
---
## Core Principles
- Minimal blast radius: only modify what is required for the task
- Deterministic verification: all changes must be verifiable via code (tests, compile, scripts)
- No architecture drift: do not introduce new frameworks or major design changes unless explicitly required
- No unrelated refactors
- All changes must be reproducible from a clean clone
---
## Project Structure
- docs/ → design, plans, architecture constraints
- plans/ → master plans
- phases/ → phase definitions
- tasks/ → executable task documents
- backends/ → CLI backend adapters
- agents/ → specialist agents
- runtime/ → orchestration, routing, state
...(truncated)

AGENTS.md guidance:
# AGENTS.md

## Purpose

This repository is operated by an autonomous multi-agent system (abracapocus_2).
All agents must follow these rules when modifying the codebase.

---

## Core Principles

- Minimal blast radius: only modify what is required for the task
- Deterministic verification: all changes must be verifiable via code (tests, compile, scripts)
- No architecture drift: do not introduce new frameworks or major design changes unless explicitly required
- No unrelated refactors
- All changes must be reproducible from a clean clone

---

## Project Structure

- docs/ → design, plans, architecture constraints
- plans/ → master plans
- phases/ → phase definitions
- tasks/ → executable task documents
- backends/ → CLI backend adapters
- agents/ → specialist agents
- runtime/ → orchestration, routing, state
- reports/ → execution reports (DO NOT MODIFY MANUALLY)
- state/runtime_state.json → runtime state (DO NOT COMMIT)

---

## Task Execution Rules

- Always operate from a task document when available
- Respect:
  - selected_backend
  - verification_profile
  - acceptance_criteria
- If a task conflicts with architecture constraints or phase scope:
  - STOP and report conflict

---

## Backend Rules

- Backends must:
  - execute commands deterministically
  - capture stdout, stderr, exit_code
  - not silently fail
- Do not invent backend interfaces; use existing adapters
- Codex CLI, Aider, Gemini, Claude Code should be invoked through backends only

---

## Verification Rules

- Verification must be deterministic
- Preferred checks:
  - pytest
  - python -m py_compile
- Do not rely on model self-evaluation

---

## Git Rules

- Do not commit:
  - runtime_state.json
  - reports/
  - logs/
  - virtual environments
- Do not modify .gitignore unless required by task
- Do not create excessive commits; prefer grouped logical commits

---

## Allowed Changes

- Implement task requirements
- Fix failing verification
- Update relevant tests
- Improve documentation tied to the task

---

## Forbidden Changes

- Changing architecture without explicit instruction
- Adding dependencies without justification
- Modifying unrelated files
- Deleting important files
- Bypassing verification

---

## Planning Rules

- Plans are multi-phase
- Completed sections are immutable
- Remaining sections may be updated
- Tasks must align with:
  - project brief
  - architecture constraints
  - active phase

---

## Reporting

- All executions must produce structured reports
- Reports must include:
  - changed files
  - verification results
  - assessment

---

## Behavior

- Do not ask unnecessary questions
- Do not stall execution
- Do not perform broad scans unless required
- Prefer direct action over analysis

---

## Priority Order

1. Architecture constraints
2. Task definition
3. Verification results
4. Plan guidance

If conflicts occur, follow this order.

## Run 2026-04-16T23:32:07
- Task ID: demo-self-improve
- Title: Refresh demo status log
- Phase: implementation
- Goal: Update docs/demo_status.md with the latest demo guidance
- Context: Collected 2 semantically relevant files; AGENTS.md guidance:
# AGENTS.md
## Purpose
This repository is operated by an autonomous multi-agent system (abracapocus_2).
All agents must follow these rules when modifying the codebase.
---
## Core Principles
- Minimal blast radius: only modify what is required for the task
- Deterministic verification: all changes must be verifiable via code (tests, compile, scripts)
- No architecture drift: do not introduce new frameworks or major design changes unless explicitly required
- No unrelated refactors
- All changes must be reproducible from a clean clone
---
## Project Structure
- docs/ → design, plans, architecture constraints
- plans/ → master plans
- phases/ → phase definitions
- tasks/ → executable task documents
- backends/ → CLI backend adapters
- agents/ → specialist agents
- runtime/ → orchestration, routing, state
...(truncated)

AGENTS.md guidance:
# AGENTS.md

## Purpose

This repository is operated by an autonomous multi-agent system (abracapocus_2).
All agents must follow these rules when modifying the codebase.

---

## Core Principles

- Minimal blast radius: only modify what is required for the task
- Deterministic verification: all changes must be verifiable via code (tests, compile, scripts)
- No architecture drift: do not introduce new frameworks or major design changes unless explicitly required
- No unrelated refactors
- All changes must be reproducible from a clean clone

---

## Project Structure

- docs/ → design, plans, architecture constraints
- plans/ → master plans
- phases/ → phase definitions
- tasks/ → executable task documents
- backends/ → CLI backend adapters
- agents/ → specialist agents
- runtime/ → orchestration, routing, state
- reports/ → execution reports (DO NOT MODIFY MANUALLY)
- state/runtime_state.json → runtime state (DO NOT COMMIT)

---

## Task Execution Rules

- Always operate from a task document when available
- Respect:
  - selected_backend
  - verification_profile
  - acceptance_criteria
- If a task conflicts with architecture constraints or phase scope:
  - STOP and report conflict

---

## Backend Rules

- Backends must:
  - execute commands deterministically
  - capture stdout, stderr, exit_code
  - not silently fail
- Do not invent backend interfaces; use existing adapters
- Codex CLI, Aider, Gemini, Claude Code should be invoked through backends only

---

## Verification Rules

- Verification must be deterministic
- Preferred checks:
  - pytest
  - python -m py_compile
- Do not rely on model self-evaluation

---

## Git Rules

- Do not commit:
  - runtime_state.json
  - reports/
  - logs/
  - virtual environments
- Do not modify .gitignore unless required by task
- Do not create excessive commits; prefer grouped logical commits

---

## Allowed Changes

- Implement task requirements
- Fix failing verification
- Update relevant tests
- Improve documentation tied to the task

---

## Forbidden Changes

- Changing architecture without explicit instruction
- Adding dependencies without justification
- Modifying unrelated files
- Deleting important files
- Bypassing verification

---

## Planning Rules

- Plans are multi-phase
- Completed sections are immutable
- Remaining sections may be updated
- Tasks must align with:
  - project brief
  - architecture constraints
  - active phase

---

## Reporting

- All executions must produce structured reports
- Reports must include:
  - changed files
  - verification results
  - assessment

---

## Behavior

- Do not ask unnecessary questions
- Do not stall execution
- Do not perform broad scans unless required
- Prefer direct action over analysis

---

## Priority Order

1. Architecture constraints
2. Task definition
3. Verification results
4. Plan guidance

If conflicts occur, follow this order.

## Run 2026-04-16T23:32:59
- Task ID: demo-self-improve
- Title: Refresh demo status log
- Phase: implementation
- Goal: Update docs/demo_status.md with the latest demo guidance
- Context: Collected 3 semantically relevant files; AGENTS.md guidance:
# AGENTS.md
## Purpose
This repository is operated by an autonomous multi-agent system (abracapocus_2).
All agents must follow these rules when modifying the codebase.
---
## Core Principles
- Minimal blast radius: only modify what is required for the task
- Deterministic verification: all changes must be verifiable via code (tests, compile, scripts)
- No architecture drift: do not introduce new frameworks or major design changes unless explicitly required
- No unrelated refactors
- All changes must be reproducible from a clean clone
---
## Project Structure
- docs/ → design, plans, architecture constraints
- plans/ → master plans
- phases/ → phase definitions
- tasks/ → executable task documents
- backends/ → CLI backend adapters
- agents/ → specialist agents
- runtime/ → orchestration, routing, state
...(truncated)

AGENTS.md guidance:
# AGENTS.md

## Purpose

This repository is operated by an autonomous multi-agent system (abracapocus_2).
All agents must follow these rules when modifying the codebase.

---

## Core Principles

- Minimal blast radius: only modify what is required for the task
- Deterministic verification: all changes must be verifiable via code (tests, compile, scripts)
- No architecture drift: do not introduce new frameworks or major design changes unless explicitly required
- No unrelated refactors
- All changes must be reproducible from a clean clone

---

## Project Structure

- docs/ → design, plans, architecture constraints
- plans/ → master plans
- phases/ → phase definitions
- tasks/ → executable task documents
- backends/ → CLI backend adapters
- agents/ → specialist agents
- runtime/ → orchestration, routing, state
- reports/ → execution reports (DO NOT MODIFY MANUALLY)
- state/runtime_state.json → runtime state (DO NOT COMMIT)

---

## Task Execution Rules

- Always operate from a task document when available
- Respect:
  - selected_backend
  - verification_profile
  - acceptance_criteria
- If a task conflicts with architecture constraints or phase scope:
  - STOP and report conflict

---

## Backend Rules

- Backends must:
  - execute commands deterministically
  - capture stdout, stderr, exit_code
  - not silently fail
- Do not invent backend interfaces; use existing adapters
- Codex CLI, Aider, Gemini, Claude Code should be invoked through backends only

---

## Verification Rules

- Verification must be deterministic
- Preferred checks:
  - pytest
  - python -m py_compile
- Do not rely on model self-evaluation

---

## Git Rules

- Do not commit:
  - runtime_state.json
  - reports/
  - logs/
  - virtual environments
- Do not modify .gitignore unless required by task
- Do not create excessive commits; prefer grouped logical commits

---

## Allowed Changes

- Implement task requirements
- Fix failing verification
- Update relevant tests
- Improve documentation tied to the task

---

## Forbidden Changes

- Changing architecture without explicit instruction
- Adding dependencies without justification
- Modifying unrelated files
- Deleting important files
- Bypassing verification

---

## Planning Rules

- Plans are multi-phase
- Completed sections are immutable
- Remaining sections may be updated
- Tasks must align with:
  - project brief
  - architecture constraints
  - active phase

---

## Reporting

- All executions must produce structured reports
- Reports must include:
  - changed files
  - verification results
  - assessment

---

## Behavior

- Do not ask unnecessary questions
- Do not stall execution
- Do not perform broad scans unless required
- Prefer direct action over analysis

---

## Priority Order

1. Architecture constraints
2. Task definition
3. Verification results
4. Plan guidance

If conflicts occur, follow this order.

## Run 2026-04-16T23:33:31
- Task ID: demo-self-improve
- Title: Refresh demo status log
- Phase: implementation
- Goal: Update docs/demo_status.md with the latest demo guidance
- Context: Collected 2 semantically relevant files; AGENTS.md guidance:
# AGENTS.md
## Purpose
This repository is operated by an autonomous multi-agent system (abracapocus_2).
All agents must follow these rules when modifying the codebase.
---
## Core Principles
- Minimal blast radius: only modify what is required for the task
- Deterministic verification: all changes must be verifiable via code (tests, compile, scripts)
- No architecture drift: do not introduce new frameworks or major design changes unless explicitly required
- No unrelated refactors
- All changes must be reproducible from a clean clone
---
## Project Structure
- docs/ → design, plans, architecture constraints
- plans/ → master plans
- phases/ → phase definitions
- tasks/ → executable task documents
- backends/ → CLI backend adapters
- agents/ → specialist agents
- runtime/ → orchestration, routing, state
...(truncated)

AGENTS.md guidance:
# AGENTS.md

## Purpose

This repository is operated by an autonomous multi-agent system (abracapocus_2).
All agents must follow these rules when modifying the codebase.

---

## Core Principles

- Minimal blast radius: only modify what is required for the task
- Deterministic verification: all changes must be verifiable via code (tests, compile, scripts)
- No architecture drift: do not introduce new frameworks or major design changes unless explicitly required
- No unrelated refactors
- All changes must be reproducible from a clean clone

---

## Project Structure

- docs/ → design, plans, architecture constraints
- plans/ → master plans
- phases/ → phase definitions
- tasks/ → executable task documents
- backends/ → CLI backend adapters
- agents/ → specialist agents
- runtime/ → orchestration, routing, state
- reports/ → execution reports (DO NOT MODIFY MANUALLY)
- state/runtime_state.json → runtime state (DO NOT COMMIT)

---

## Task Execution Rules

- Always operate from a task document when available
- Respect:
  - selected_backend
  - verification_profile
  - acceptance_criteria
- If a task conflicts with architecture constraints or phase scope:
  - STOP and report conflict

---

## Backend Rules

- Backends must:
  - execute commands deterministically
  - capture stdout, stderr, exit_code
  - not silently fail
- Do not invent backend interfaces; use existing adapters
- Codex CLI, Aider, Gemini, Claude Code should be invoked through backends only

---

## Verification Rules

- Verification must be deterministic
- Preferred checks:
  - pytest
  - python -m py_compile
- Do not rely on model self-evaluation

---

## Git Rules

- Do not commit:
  - runtime_state.json
  - reports/
  - logs/
  - virtual environments
- Do not modify .gitignore unless required by task
- Do not create excessive commits; prefer grouped logical commits

---

## Allowed Changes

- Implement task requirements
- Fix failing verification
- Update relevant tests
- Improve documentation tied to the task

---

## Forbidden Changes

- Changing architecture without explicit instruction
- Adding dependencies without justification
- Modifying unrelated files
- Deleting important files
- Bypassing verification

---

## Planning Rules

- Plans are multi-phase
- Completed sections are immutable
- Remaining sections may be updated
- Tasks must align with:
  - project brief
  - architecture constraints
  - active phase

---

## Reporting

- All executions must produce structured reports
- Reports must include:
  - changed files
  - verification results
  - assessment

---

## Behavior

- Do not ask unnecessary questions
- Do not stall execution
- Do not perform broad scans unless required
- Prefer direct action over analysis

---

## Priority Order

1. Architecture constraints
2. Task definition
3. Verification results
4. Plan guidance

If conflicts occur, follow this order.

## Run 2026-04-16T23:35:00
- Task ID: demo-self-improve
- Title: Refresh demo status log
- Phase: implementation
- Goal: Update docs/demo_status.md with the latest demo guidance
- Context: Collected 2 semantically relevant files; AGENTS.md guidance:
# AGENTS.md
## Purpose
This repository is operated by an autonomous multi-agent system (abracapocus_2).
All agents must follow these rules when modifying the codebase.
---
## Core Principles
- Minimal blast radius: only modify what is required for the task
- Deterministic verification: all changes must be verifiable via code (tests, compile, scripts)
- No architecture drift: do not introduce new frameworks or major design changes unless explicitly required
- No unrelated refactors
- All changes must be reproducible from a clean clone
---
## Project Structure
- docs/ → design, plans, architecture constraints
- plans/ → master plans
- phases/ → phase definitions
- tasks/ → executable task documents
- backends/ → CLI backend adapters
- agents/ → specialist agents
- runtime/ → orchestration, routing, state
...(truncated)

AGENTS.md guidance:
# AGENTS.md

## Purpose

This repository is operated by an autonomous multi-agent system (abracapocus_2).
All agents must follow these rules when modifying the codebase.

---

## Core Principles

- Minimal blast radius: only modify what is required for the task
- Deterministic verification: all changes must be verifiable via code (tests, compile, scripts)
- No architecture drift: do not introduce new frameworks or major design changes unless explicitly required
- No unrelated refactors
- All changes must be reproducible from a clean clone

---

## Project Structure

- docs/ → design, plans, architecture constraints
- plans/ → master plans
- phases/ → phase definitions
- tasks/ → executable task documents
- backends/ → CLI backend adapters
- agents/ → specialist agents
- runtime/ → orchestration, routing, state
- reports/ → execution reports (DO NOT MODIFY MANUALLY)
- state/runtime_state.json → runtime state (DO NOT COMMIT)

---

## Task Execution Rules

- Always operate from a task document when available
- Respect:
  - selected_backend
  - verification_profile
  - acceptance_criteria
- If a task conflicts with architecture constraints or phase scope:
  - STOP and report conflict

---

## Backend Rules

- Backends must:
  - execute commands deterministically
  - capture stdout, stderr, exit_code
  - not silently fail
- Do not invent backend interfaces; use existing adapters
- Codex CLI, Aider, Gemini, Claude Code should be invoked through backends only

---

## Verification Rules

- Verification must be deterministic
- Preferred checks:
  - pytest
  - python -m py_compile
- Do not rely on model self-evaluation

---

## Git Rules

- Do not commit:
  - runtime_state.json
  - reports/
  - logs/
  - virtual environments
- Do not modify .gitignore unless required by task
- Do not create excessive commits; prefer grouped logical commits

---

## Allowed Changes

- Implement task requirements
- Fix failing verification
- Update relevant tests
- Improve documentation tied to the task

---

## Forbidden Changes

- Changing architecture without explicit instruction
- Adding dependencies without justification
- Modifying unrelated files
- Deleting important files
- Bypassing verification

---

## Planning Rules

- Plans are multi-phase
- Completed sections are immutable
- Remaining sections may be updated
- Tasks must align with:
  - project brief
  - architecture constraints
  - active phase

---

## Reporting

- All executions must produce structured reports
- Reports must include:
  - changed files
  - verification results
  - assessment

---

## Behavior

- Do not ask unnecessary questions
- Do not stall execution
- Do not perform broad scans unless required
- Prefer direct action over analysis

---

## Priority Order

1. Architecture constraints
2. Task definition
3. Verification results
4. Plan guidance

If conflicts occur, follow this order.

## Run 2026-04-16T23:35:53
- Task ID: demo-self-improve
- Title: Refresh demo status log
- Phase: implementation
- Goal: Update docs/demo_status.md with the latest demo guidance
- Context: Collected 1 semantically relevant files; AGENTS.md guidance:
# AGENTS.md
## Purpose
This repository is operated by an autonomous multi-agent system (abracapocus_2).
All agents must follow these rules when modifying the codebase.
---
## Core Principles
- Minimal blast radius: only modify what is required for the task
- Deterministic verification: all changes must be verifiable via code (tests, compile, scripts)
- No architecture drift: do not introduce new frameworks or major design changes unless explicitly required
- No unrelated refactors
- All changes must be reproducible from a clean clone
---
## Project Structure
- docs/ → design, plans, architecture constraints
- plans/ → master plans
- phases/ → phase definitions
- tasks/ → executable task documents
- backends/ → CLI backend adapters
- agents/ → specialist agents
- runtime/ → orchestration, routing, state
...(truncated)

AGENTS.md guidance:
# AGENTS.md

## Purpose

This repository is operated by an autonomous multi-agent system (abracapocus_2).
All agents must follow these rules when modifying the codebase.

---

## Core Principles

- Minimal blast radius: only modify what is required for the task
- Deterministic verification: all changes must be verifiable via code (tests, compile, scripts)
- No architecture drift: do not introduce new frameworks or major design changes unless explicitly required
- No unrelated refactors
- All changes must be reproducible from a clean clone

---

## Project Structure

- docs/ → design, plans, architecture constraints
- plans/ → master plans
- phases/ → phase definitions
- tasks/ → executable task documents
- backends/ → CLI backend adapters
- agents/ → specialist agents
- runtime/ → orchestration, routing, state
- reports/ → execution reports (DO NOT MODIFY MANUALLY)
- state/runtime_state.json → runtime state (DO NOT COMMIT)

---

## Task Execution Rules

- Always operate from a task document when available
- Respect:
  - selected_backend
  - verification_profile
  - acceptance_criteria
- If a task conflicts with architecture constraints or phase scope:
  - STOP and report conflict

---

## Backend Rules

- Backends must:
  - execute commands deterministically
  - capture stdout, stderr, exit_code
  - not silently fail
- Do not invent backend interfaces; use existing adapters
- Codex CLI, Aider, Gemini, Claude Code should be invoked through backends only

---

## Verification Rules

- Verification must be deterministic
- Preferred checks:
  - pytest
  - python -m py_compile
- Do not rely on model self-evaluation

---

## Git Rules

- Do not commit:
  - runtime_state.json
  - reports/
  - logs/
  - virtual environments
- Do not modify .gitignore unless required by task
- Do not create excessive commits; prefer grouped logical commits

---

## Allowed Changes

- Implement task requirements
- Fix failing verification
- Update relevant tests
- Improve documentation tied to the task

---

## Forbidden Changes

- Changing architecture without explicit instruction
- Adding dependencies without justification
- Modifying unrelated files
- Deleting important files
- Bypassing verification

---

## Planning Rules

- Plans are multi-phase
- Completed sections are immutable
- Remaining sections may be updated
- Tasks must align with:
  - project brief
  - architecture constraints
  - active phase

---

## Reporting

- All executions must produce structured reports
- Reports must include:
  - changed files
  - verification results
  - assessment

---

## Behavior

- Do not ask unnecessary questions
- Do not stall execution
- Do not perform broad scans unless required
- Prefer direct action over analysis

---

## Priority Order

1. Architecture constraints
2. Task definition
3. Verification results
4. Plan guidance

If conflicts occur, follow this order.

## Run 2026-04-16T23:36:33
- Task ID: demo-self-improve
- Title: Refresh demo status log
- Phase: implementation
- Goal: Update docs/demo_status.md with the latest demo guidance
- Context: Collected 2 semantically relevant files; AGENTS.md guidance:
# AGENTS.md
## Purpose
This repository is operated by an autonomous multi-agent system (abracapocus_2).
All agents must follow these rules when modifying the codebase.
---
## Core Principles
- Minimal blast radius: only modify what is required for the task
- Deterministic verification: all changes must be verifiable via code (tests, compile, scripts)
- No architecture drift: do not introduce new frameworks or major design changes unless explicitly required
- No unrelated refactors
- All changes must be reproducible from a clean clone
---
## Project Structure
- docs/ → design, plans, architecture constraints
- plans/ → master plans
- phases/ → phase definitions
- tasks/ → executable task documents
- backends/ → CLI backend adapters
- agents/ → specialist agents
- runtime/ → orchestration, routing, state
...(truncated)

AGENTS.md guidance:
# AGENTS.md

## Purpose

This repository is operated by an autonomous multi-agent system (abracapocus_2).
All agents must follow these rules when modifying the codebase.

---

## Core Principles

- Minimal blast radius: only modify what is required for the task
- Deterministic verification: all changes must be verifiable via code (tests, compile, scripts)
- No architecture drift: do not introduce new frameworks or major design changes unless explicitly required
- No unrelated refactors
- All changes must be reproducible from a clean clone

---

## Project Structure

- docs/ → design, plans, architecture constraints
- plans/ → master plans
- phases/ → phase definitions
- tasks/ → executable task documents
- backends/ → CLI backend adapters
- agents/ → specialist agents
- runtime/ → orchestration, routing, state
- reports/ → execution reports (DO NOT MODIFY MANUALLY)
- state/runtime_state.json → runtime state (DO NOT COMMIT)

---

## Task Execution Rules

- Always operate from a task document when available
- Respect:
  - selected_backend
  - verification_profile
  - acceptance_criteria
- If a task conflicts with architecture constraints or phase scope:
  - STOP and report conflict

---

## Backend Rules

- Backends must:
  - execute commands deterministically
  - capture stdout, stderr, exit_code
  - not silently fail
- Do not invent backend interfaces; use existing adapters
- Codex CLI, Aider, Gemini, Claude Code should be invoked through backends only

---

## Verification Rules

- Verification must be deterministic
- Preferred checks:
  - pytest
  - python -m py_compile
- Do not rely on model self-evaluation

---

## Git Rules

- Do not commit:
  - runtime_state.json
  - reports/
  - logs/
  - virtual environments
- Do not modify .gitignore unless required by task
- Do not create excessive commits; prefer grouped logical commits

---

## Allowed Changes

- Implement task requirements
- Fix failing verification
- Update relevant tests
- Improve documentation tied to the task

---

## Forbidden Changes

- Changing architecture without explicit instruction
- Adding dependencies without justification
- Modifying unrelated files
- Deleting important files
- Bypassing verification

---

## Planning Rules

- Plans are multi-phase
- Completed sections are immutable
- Remaining sections may be updated
- Tasks must align with:
  - project brief
  - architecture constraints
  - active phase

---

## Reporting

- All executions must produce structured reports
- Reports must include:
  - changed files
  - verification results
  - assessment

---

## Behavior

- Do not ask unnecessary questions
- Do not stall execution
- Do not perform broad scans unless required
- Prefer direct action over analysis

---

## Priority Order

1. Architecture constraints
2. Task definition
3. Verification results
4. Plan guidance

If conflicts occur, follow this order.

## Run 2026-04-16T23:37:52
- Task ID: demo-self-improve
- Title: Refresh demo status log
- Phase: implementation
- Goal: Update docs/demo_status.md with the latest demo guidance
- Context: Collected 5 semantically relevant files; AGENTS.md guidance:
# AGENTS.md
## Purpose
This repository is operated by an autonomous multi-agent system (abracapocus_2).
All agents must follow these rules when modifying the codebase.
---
## Core Principles
- Minimal blast radius: only modify what is required for the task
- Deterministic verification: all changes must be verifiable via code (tests, compile, scripts)
- No architecture drift: do not introduce new frameworks or major design changes unless explicitly required
- No unrelated refactors
- All changes must be reproducible from a clean clone
---
## Project Structure
- docs/ → design, plans, architecture constraints
- plans/ → master plans
- phases/ → phase definitions
- tasks/ → executable task documents
- backends/ → CLI backend adapters
- agents/ → specialist agents
- runtime/ → orchestration, routing, state
...(truncated)

AGENTS.md guidance:
# AGENTS.md

## Purpose

This repository is operated by an autonomous multi-agent system (abracapocus_2).
All agents must follow these rules when modifying the codebase.

---

## Core Principles

- Minimal blast radius: only modify what is required for the task
- Deterministic verification: all changes must be verifiable via code (tests, compile, scripts)
- No architecture drift: do not introduce new frameworks or major design changes unless explicitly required
- No unrelated refactors
- All changes must be reproducible from a clean clone

---

## Project Structure

- docs/ → design, plans, architecture constraints
- plans/ → master plans
- phases/ → phase definitions
- tasks/ → executable task documents
- backends/ → CLI backend adapters
- agents/ → specialist agents
- runtime/ → orchestration, routing, state
- reports/ → execution reports (DO NOT MODIFY MANUALLY)
- state/runtime_state.json → runtime state (DO NOT COMMIT)

---

## Task Execution Rules

- Always operate from a task document when available
- Respect:
  - selected_backend
  - verification_profile
  - acceptance_criteria
- If a task conflicts with architecture constraints or phase scope:
  - STOP and report conflict

---

## Backend Rules

- Backends must:
  - execute commands deterministically
  - capture stdout, stderr, exit_code
  - not silently fail
- Do not invent backend interfaces; use existing adapters
- Codex CLI, Aider, Gemini, Claude Code should be invoked through backends only

---

## Verification Rules

- Verification must be deterministic
- Preferred checks:
  - pytest
  - python -m py_compile
- Do not rely on model self-evaluation

---

## Git Rules

- Do not commit:
  - runtime_state.json
  - reports/
  - logs/
  - virtual environments
- Do not modify .gitignore unless required by task
- Do not create excessive commits; prefer grouped logical commits

---

## Allowed Changes

- Implement task requirements
- Fix failing verification
- Update relevant tests
- Improve documentation tied to the task

---

## Forbidden Changes

- Changing architecture without explicit instruction
- Adding dependencies without justification
- Modifying unrelated files
- Deleting important files
- Bypassing verification

---

## Planning Rules

- Plans are multi-phase
- Completed sections are immutable
- Remaining sections may be updated
- Tasks must align with:
  - project brief
  - architecture constraints
  - active phase

---

## Reporting

- All executions must produce structured reports
- Reports must include:
  - changed files
  - verification results
  - assessment

---

## Behavior

- Do not ask unnecessary questions
- Do not stall execution
- Do not perform broad scans unless required
- Prefer direct action over analysis

---

## Priority Order

1. Architecture constraints
2. Task definition
3. Verification results
4. Plan guidance

If conflicts occur, follow this order.

## Run 2026-04-16T23:38:52
- Task ID: demo-self-improve
- Title: Refresh demo status log
- Phase: implementation
- Goal: Update docs/demo_status.md with the latest demo guidance
- Context: Collected 2 semantically relevant files; AGENTS.md guidance:
# AGENTS.md
## Purpose
This repository is operated by an autonomous multi-agent system (abracapocus_2).
All agents must follow these rules when modifying the codebase.
---
## Core Principles
- Minimal blast radius: only modify what is required for the task
- Deterministic verification: all changes must be verifiable via code (tests, compile, scripts)
- No architecture drift: do not introduce new frameworks or major design changes unless explicitly required
- No unrelated refactors
- All changes must be reproducible from a clean clone
---
## Project Structure
- docs/ → design, plans, architecture constraints
- plans/ → master plans
- phases/ → phase definitions
- tasks/ → executable task documents
- backends/ → CLI backend adapters
- agents/ → specialist agents
- runtime/ → orchestration, routing, state
...(truncated)

AGENTS.md guidance:
# AGENTS.md

## Purpose

This repository is operated by an autonomous multi-agent system (abracapocus_2).
All agents must follow these rules when modifying the codebase.

---

## Core Principles

- Minimal blast radius: only modify what is required for the task
- Deterministic verification: all changes must be verifiable via code (tests, compile, scripts)
- No architecture drift: do not introduce new frameworks or major design changes unless explicitly required
- No unrelated refactors
- All changes must be reproducible from a clean clone

---

## Project Structure

- docs/ → design, plans, architecture constraints
- plans/ → master plans
- phases/ → phase definitions
- tasks/ → executable task documents
- backends/ → CLI backend adapters
- agents/ → specialist agents
- runtime/ → orchestration, routing, state
- reports/ → execution reports (DO NOT MODIFY MANUALLY)
- state/runtime_state.json → runtime state (DO NOT COMMIT)

---

## Task Execution Rules

- Always operate from a task document when available
- Respect:
  - selected_backend
  - verification_profile
  - acceptance_criteria
- If a task conflicts with architecture constraints or phase scope:
  - STOP and report conflict

---

## Backend Rules

- Backends must:
  - execute commands deterministically
  - capture stdout, stderr, exit_code
  - not silently fail
- Do not invent backend interfaces; use existing adapters
- Codex CLI, Aider, Gemini, Claude Code should be invoked through backends only

---

## Verification Rules

- Verification must be deterministic
- Preferred checks:
  - pytest
  - python -m py_compile
- Do not rely on model self-evaluation

---

## Git Rules

- Do not commit:
  - runtime_state.json
  - reports/
  - logs/
  - virtual environments
- Do not modify .gitignore unless required by task
- Do not create excessive commits; prefer grouped logical commits

---

## Allowed Changes

- Implement task requirements
- Fix failing verification
- Update relevant tests
- Improve documentation tied to the task

---

## Forbidden Changes

- Changing architecture without explicit instruction
- Adding dependencies without justification
- Modifying unrelated files
- Deleting important files
- Bypassing verification

---

## Planning Rules

- Plans are multi-phase
- Completed sections are immutable
- Remaining sections may be updated
- Tasks must align with:
  - project brief
  - architecture constraints
  - active phase

---

## Reporting

- All executions must produce structured reports
- Reports must include:
  - changed files
  - verification results
  - assessment

---

## Behavior

- Do not ask unnecessary questions
- Do not stall execution
- Do not perform broad scans unless required
- Prefer direct action over analysis

---

## Priority Order

1. Architecture constraints
2. Task definition
3. Verification results
4. Plan guidance

If conflicts occur, follow this order.

