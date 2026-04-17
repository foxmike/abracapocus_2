# ABRACAPOCUS_PROJECT_SETUP.md

## Purpose

This repository is intended to be built through `abracapocus_2`, a supervisor-led autonomous development system.

Before `abracapocus_2` can build this project, the repository must contain a complete set of project-definition documents and executable task definitions.

This document defines the required planning structure, required files, file contents, formatting rules, and workflow for creating them.

This document is used during the **project definition stage**.

It is **not** the execution plan itself.  
It is the instruction set for building the execution plan.

---

## High-Level Workflow

A project built with `abracapocus_2` proceeds in two stages.

### Stage 1: Project Definition
In this stage, a human operator works interactively with ChatGPT inside the target repository to define:
- the project purpose
- architecture constraints
- backend/model policy
- development phases
- executable task JSON files

Codex CLI may be used during this stage to create and refine the required documents.

The output of this stage is:
- stable markdown documents
- a master plan
- phase definitions
- executable task JSON files

### Stage 2: Project Execution
Once Stage 1 is complete, `abracapocus_2` is pointed at this repository as the working root and uses the generated documents and task JSON files to:
- plan and refine work
- route tasks to coding backends
- review and verify results
- produce reports and state
- iterate phase by phase

---

## Required Repository Structure

Every project intended for `abracapocus_2` must contain the following structure at minimum:

```text
<repo-root>/
  ABRACAPOCUS_PROJECT_SETUP.md
  AGENTS.md
  README.md

  docs/
    project_brief.md
    architecture_constraints.md
    model_backend_policy.md
    architecture.md
    operations.md

  planning/
    README.md
    master_plan.md
    phase_0/
      phase.md
      task_0.1_<slug>.json
      task_0.2_<slug>.json
    phase_1/
      phase.md
      task_1.1_<slug>.json

  scripts/
  tests/
  reports/
  state/
```

### Notes
- `docs/` contains stable human-readable reference documents.
- `planning/` contains the authoritative execution plan.
- `reports/` and `state/` are runtime/output locations and are not part of the planning source of truth.
- Task JSON files should live inside the appropriate `planning/phase_x/` directory.
- Avoid mixing planning artifacts across `docs/`, `plans/`, `tasks/`, and `phases/`. Use `planning/` as the single source of truth for phases and task JSONs.

---

## Required Documents

The following files are required before `abracapocus_2` should be used to build the project.

---

## 1. `AGENTS.md`

### Purpose
Defines repo-level rules and behavioral constraints for all coding agents and execution backends.

### Required content
- repo purpose
- architecture protection rules
- allowed / forbidden changes
- verification expectations
- git hygiene rules
- execution rules
- priority order for resolving conflicts

### Example outline
```md
# AGENTS.md

## Purpose
This repository is developed using abracapocus_2.

## Rules
- minimal blast radius
- deterministic verification
- no unrelated refactors
- no architecture drift
- no new frameworks without approval

## Verification
- tests must pass
- changes must be reproducible from clean clone

## Task Execution
- honor task JSON selected_backend, model, and verification_profile
- stop and report conflicts instead of improvising

## Git
- do not commit reports/, state/, runtime artifacts
```

### Formatting rules
- Markdown only
- short sections
- imperative language
- no vague philosophy
- focus on operational constraints

---

## 2. `docs/project_brief.md`

### Purpose
Defines what the project is, why it exists, who it is for, and what success looks like.

### Required content
- project name
- purpose
- users
- core goals
- desired end state
- major features
- non-goals
- success criteria

### Required structure
```md
# Project Brief

## Project Name
<name>

## Purpose
<what the project does and why it exists>

## Users
<who uses it>

## Core Goals
- <goal>
- <goal>

## Desired End State
<what “done” looks like>

## Major Features
- <feature>
- <feature>

## Non-Goals
- <not in scope>
- <not in scope>

## Success Criteria
- <criterion>
- <criterion>
```

### Rules
- keep it product-focused
- do not drift into implementation details unless critical
- write for a planning agent, not a marketer

---

## 3. `docs/architecture_constraints.md`

### Purpose
Defines hard implementation boundaries and rules that must constrain planning and execution.

### Required content
- required stack
- forbidden stack/frameworks
- repo structure expectations
- deployment assumptions
- data/storage rules
- verification commands
- blast radius rules
- operational constraints

### Required structure
```md
# Architecture Constraints

## Required Stack
- <language>
- <framework>
- <storage>

## Forbidden Changes
- no new frameworks without approval
- no architecture drift
- no unrelated refactors

## Repo / Workflow Rules
- deterministic verification
- minimal blast radius
- reproducible changes

## Verification
- <command>
- <command>

## Operational Constraints
- <constraint>
- <constraint>
```

### Rules
- these are hard constraints
- do not include preferences here unless they are mandatory
- keep each rule testable or operationally meaningful

---

## 4. `docs/model_backend_policy.md`

### Purpose
Defines which coding backends and model classes should be preferred for different kinds of work.

### Required content
- primary backend
- secondary/fallback backend
- backend/model selection policy by task type
- cost/performance strategy
- non-interactive execution expectations
- any backend restrictions

### Required structure
```md
# Model / Backend Policy

## Primary Backend
<codex_cli | aider_cli | claude_code_cli | gemini_cli>

## Secondary / Fallback Backends
- <backend>
- <backend>

## Task Policy
- planning-heavy tasks → <backend/model style>
- targeted code edits → <backend/model style>
- broad low-cost edits → <backend/model style>
- verification-sensitive tasks → <backend/model style>

## Cost / Performance Strategy
- <policy>

## Execution Rules
- all execution must remain non-interactive
- prefer deterministic backends where practical
```

### Rules
- do not over-specify every model unless necessary
- provide a usable routing policy, not a giant matrix
- task JSONs may still override this later

---

## 5. `docs/architecture.md`

### Purpose
Describes the intended system architecture of the target project.

### Required content
- major components
- responsibilities
- data flow
- interfaces
- deployment shape if relevant

### Required structure
```md
# Architecture Overview

## Major Components
- <component>: <responsibility>
- <component>: <responsibility>

## Data Flow
1. <step>
2. <step>

## Key Boundaries
- <boundary>
- <boundary>

## Extensibility
- <future extension point>
```

### Rules
- this is not a code dump
- should be readable by humans and planning agents
- enough detail to constrain tasks, not enough to lock every line of code

---

## 6. `docs/operations.md`

### Purpose
Defines how the project should be run, tested, and operated.

### Required content
- setup commands
- run commands
- test commands
- important Make targets if any
- environment expectations

### Required structure
```md
# Operations

## Setup
- <command>
- <command>

## Run
- <command>

## Test
- <command>

## Notes
- <operational note>
```

---

## 7. `planning/README.md`

### Purpose
Explains how the planning tree is organized and how `abracapocus_2` should treat it.

### Required content
- planning tree is source of truth
- `master_plan.md` is top-level roadmap
- each `phase_x/phase.md` explains the phase
- each task JSON is an executable unit
- runtime/generated tasks must not be confused with curated task JSONs

### Example structure
```md
# Planning README

This directory contains the authoritative project execution plan.

## Structure
- master_plan.md → top-level roadmap
- phase_x/phase.md → phase description and exit criteria
- phase_x/task_*.json → executable tasks

## Rules
- task JSON files are curated source-of-truth tasks
- runtime-generated tasks must not overwrite curated tasks
- phase execution should follow dependency order
```

---

## 8. `planning/master_plan.md`

### Purpose
Top-level roadmap for the project.

### Required content
- overall objective
- phase list in order
- goals per phase
- deliverables per phase
- acceptance criteria per phase

### Required structure
```md
# Master Plan

## Objective
<overall project objective>

## Phase 0
### Goal
<goal>
### Deliverables
- <deliverable>
### Acceptance Criteria
- <criterion>

## Phase 1
### Goal
<goal>
### Deliverables
- <deliverable>
### Acceptance Criteria
- <criterion>
```

### Rules
- phases should be sequenced logically
- each phase should be independently understandable
- keep it concise enough to stay maintainable

---

## 9. `planning/phase_x/phase.md`

### Purpose
Defines one project phase in detail.

### Required content
- objective
- in scope
- out of scope
- deliverables
- exit criteria
- ordered task list

### Required structure
```md
# Phase X

## Objective
<goal of this phase>

## In Scope
- <item>
- <item>

## Out of Scope
- <item>
- <item>

## Deliverables
- <deliverable>
- <deliverable>

## Exit Criteria
- <criterion>
- <criterion>

## Tasks
- task_x.1_<slug>
- task_x.2_<slug>
```

### Rules
- do not put executable detail here that belongs in task JSON
- this file defines phase intent and boundaries

---

## 10. `planning/phase_x/task_*.json`

### Purpose
Executable unit of work for `abracapocus_2`.

### Required fields

Each task JSON must contain:

```json
{
  "task_id": "0.1",
  "title": "Short human-readable task title",
  "description": "Detailed description of the work to be done.",
  "phase": "phase_0",
  "acceptance_criteria": [
    "Specific verifiable criterion",
    "Specific verifiable criterion"
  ],
  "selected_backend": "codex_cli",
  "verification_profile": "strict",
  "model": "gpt-5.3-codex"
}
```

### Field meanings

#### `task_id`
- unique within the project
- recommended format: `"0.1"`, `"1.2"`, etc.

#### `title`
- short and descriptive
- human-readable

#### `description`
- implementation-oriented description
- should explain what needs to be built and any key constraints

#### `phase`
- must match containing phase directory
- e.g. `"phase_0"`

#### `acceptance_criteria`
- list of concrete, verifiable conditions
- should be testable or inspectable
- avoid vague phrases like “works well”

#### `selected_backend`
Allowed values:
- `codex_cli`
- `aider_cli`
- `claude_code_cli`
- `gemini_cli`

#### `verification_profile`
Typical values:
- `minimal`
- `default`
- `strict`

#### `model`
- optional but recommended when you want to force a specific model
- should be consistent with backend
- examples:
  - `"gpt-5.3-codex"`
  - `"openrouter/deepseek/deepseek-v3.2"`
  - `"openrouter/moonshotai/kimi-k2.5"`

### Formatting rules
- JSON only
- valid parseable JSON
- no comments
- one task per file
- filename should match task id and title slug

Example filename:
```text
task_0.1_scaffold-project-structure.json
```

---

## Planning and Task Design Rules

### Phase design rules
- each phase should deliver a coherent capability slice
- do not make phases too broad
- prefer 3–7 tasks per phase
- use Phase 0 only if there is a meaningful foundational/bootstrap phase

### Task design rules
- tasks must be small enough to execute safely
- tasks must have strong acceptance criteria
- tasks should not combine unrelated changes
- tasks should specify backend and verification intentionally
- task JSONs are source-of-truth execution units, not rough notes

### Acceptance criteria rules
Good acceptance criteria are:
- specific
- testable
- observable

Bad example:
- `"system is better"`

Good example:
- `"ContextStore.query returns top-k results with file path metadata"`
- `"make context-index completes without error"`

---

## Recommended Project Definition Workflow

### Step 1
Create:
- `AGENTS.md`
- `docs/project_brief.md`
- `docs/architecture_constraints.md`
- `docs/model_backend_policy.md`
- `docs/architecture.md`
- `docs/operations.md`

### Step 2
Create:
- `planning/README.md`
- `planning/master_plan.md`

### Step 3
Define phase folders and `phase.md` files.

### Step 4
Generate task JSON files for the first phase or first several phases.

### Step 5
Review all generated docs manually with ChatGPT.

### Step 6
Once the planning tree is clean, use `abracapocus_2` to execute tasks phase by phase.

---

## Role of ChatGPT and Codex During Project Definition

### ChatGPT should be used to:
- help shape project brief
- refine architecture constraints
- decide phase breakdown
- review task scope and acceptance criteria
- improve planning clarity

### Codex should be used to:
- create or revise markdown files
- create task JSON files
- normalize formatting and filenames
- generate phase directories and planning structure
- make targeted edits to planning documents

### `abracapocus_2` should NOT be used to build the project until:
- the required planning docs exist
- the task JSONs exist
- backend/model policy exists
- AGENTS.md exists

---

## Instructions for ChatGPT Sessions in a New Project

When starting a new project in ChatGPT, use this workflow:

1. Read `ABRACAPOCUS_PROJECT_SETUP.md`
2. Interactively define the project with the user
3. Produce or refine:
   - `AGENTS.md`
   - all required `docs/*.md`
   - `planning/master_plan.md`
   - `planning/phase_x/phase.md`
   - `planning/phase_x/task_*.json`
4. Keep planning architecture-aligned and executable
5. Do not start coding the product until the planning tree is complete

---

## Instructions for Codex CLI in a New Project

When using Codex CLI to build planning files in a new project:
- follow this setup document exactly
- create all required markdown files and task JSON files
- preserve valid existing work
- keep changes minimal
- do not invent extra planning layers
- keep the planning structure clean and parseable
- make task JSON files executable by `abracapocus_2`

---

## Final Readiness Checklist

Before using `abracapocus_2` to build the project, confirm the repository has:

- `AGENTS.md`
- `docs/project_brief.md`
- `docs/architecture_constraints.md`
- `docs/model_backend_policy.md`
- `docs/architecture.md`
- `docs/operations.md`
- `planning/README.md`
- `planning/master_plan.md`
- at least one `planning/phase_x/phase.md`
- at least one valid `planning/phase_x/task_*.json`

If all of those exist and are coherent, the project is ready for `abracapocus_2` execution.

---

## Guiding Principle

The planning tree must be:
- explicit
- executable
- maintainable
- reviewable by humans
- understandable by agents

`abracapocus_2` should operate on a **clear project definition**, not a vague idea.
