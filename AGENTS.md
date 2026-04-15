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
