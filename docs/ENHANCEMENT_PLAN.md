# abracapocus_2 Enhancement Plan

## Overview
Six phases of enhancement transforming abracapocus_2 from a working
orchestration scaffold into a production-capable autonomous development
system. Each phase is independently deployable and builds on the previous.

---

## Phase 1: Research Agent — RAG Context Engine

### Objective
Replace the naive 25-file alphabetical scan with a vector-search-backed
context engine that indexes repo files on first run, updates incrementally
after each backend execution, and retrieves semantically relevant context
for each task.

### Entry criteria
- abracapocus_2 passes all 21 tests
- Research agent currently functional in mock mode

### Exit criteria
- ContextStore indexes repo on first run and persists to state/
- Research agent queries by semantic similarity, not file walk
- Changed files from BackendResult trigger incremental re-index
- .abracapocus_context hint file is read and force-included
- All 21 existing tests still pass
- New tests cover index, update, and query paths

### Tasks

#### Task 1.1 — Install and wire embedding dependencies
- Add chromadb and sentence-transformers to requirements.txt
- Verify import in a new runtime/context_store.py stub
- Acceptance criteria:
  - `pip install -r requirements.txt` completes without error
  - `python -c "import chromadb; import sentence_transformers"` succeeds
  - runtime/context_store.py exists with a stub ContextStore class
- Verification: `python -m py_compile runtime/context_store.py`

#### Task 1.2 — Build ContextStore index and query
- Implement ContextStore class in runtime/context_store.py
- Methods: index_repo(root), update_files(changed_files), query(text, k=15)
- Use ChromaDB with local persistent storage at state/chroma/
- Chunk files by function/class boundary for .py, by paragraph for .md
- Filter out .venv, __pycache__, .git, node_modules, *.pyc on index
- Acceptance criteria:
  - index_repo() indexes all eligible files under repo root
  - query() returns k most relevant chunks with file paths
  - update_files() re-indexes only the provided paths
  - state/chroma/ directory created and persisted after index
- Verification: `python -m pytest tests/test_context_store.py -x`

#### Task 1.3 — Add .abracapocus_context hint file support
- ContextStore reads .abracapocus_context from repo root if present
- Format: one file path or glob per line, # comments ignored
- Files matching hints are always included in query results regardless
  of similarity score
- Acceptance criteria:
  - .abracapocus_context parsed correctly with comments stripped
  - Hint files appear in every query result
  - Missing hint file is silently ignored
- Verification: `python -m pytest tests/test_context_store.py -x`

#### Task 1.4 — Wire ContextStore into ResearchAgent
- Replace _scan_repo() file walk in agents/research_agent.py with
  ContextStore.query() using task goal as query text
- Initialize ContextStore in ResearchAgent.__init__
- Call update_files() after each run using changed_files from report
- Acceptance criteria:
  - ResearchAgent.gather() returns semantically relevant files
  - .venv and __pycache__ never appear in context packages
  - ContextPackage.files contains actual relevant paths
- Verification: `python -m pytest tests/ -x`

#### Task 1.5 — Add context_store make targets
- Add to Makefile: context-index, context-reset
- context-index runs python -m scripts.ops context-index
- context-reset deletes state/chroma/ and reinitializes
- Add context_index and context_reset commands to scripts/ops.py
- Acceptance criteria:
  - make context-index completes without error on real repo
  - make context-reset clears and rebuilds the index
- Verification: `make context-index && make test`

---

## Phase 2: Planning Agent Intelligence

### Objective
Replace the rigid three-phase plan template with complexity-aware
planning that decomposes tasks from acceptance criteria, classifies
scope, and assigns backends per task based on task characteristics.

### Entry criteria
- Phase 1 complete
- Planning agent functional with LocalDeepAgent

### Exit criteria
- Plan phase count varies by task complexity (1, 3, or 5+ phases)
- Each acceptance criterion maps to at least one concrete task
- Backend assigned per task at planning time not routing time
- Historical plan data informs future plans
- All tests pass

### Tasks

#### Task 2.1 — Build task complexity classifier
- Add agents/complexity_classifier.py
- Inputs: task title, description, acceptance_criteria, context file list
- Outputs: ComplexityScore dataclass with fields:
  scope (micro/standard/complex), risk (low/medium/high),
  estimated_files (int), recommended_phases (int),
  recommended_backend (str)
- Score based on: acceptance criteria count, description length,
  number of relevant context files, keywords (auth, database, api,
  migration = higher risk)
- Acceptance criteria:
  - micro: 1 criterion, <100 char description → 1 phase
  - standard: 2-4 criteria → 3 phases
  - complex: 5+ criteria or high-risk keywords → 5 phases
  - recommended_backend matches task type
- Verification: `python -m pytest tests/test_complexity_classifier.py -x`

#### Task 2.2 — Rewrite PlanningAgent.create_plan() with complexity awareness
- Import and call ComplexityClassifier before generating phases
- Generate phase count from complexity score
- For each acceptance criterion, generate one TaskDocument
- Assign selected_backend from complexity score per task
- Acceptance criteria:
  - Single-criterion task produces single-phase plan
  - Five-criterion task produces five or more tasks across phases
  - Each task has selected_backend set
  - Plans persist correctly to plans/ directory
- Verification: `python -m pytest tests/ -x`

#### Task 2.3 — Acceptance-criteria-driven task decomposition
- Add PlanningAgent._decompose_from_criteria() method
- Each criterion becomes a TaskDocument with:
  task_id derived from criterion text slug
  description = criterion text
  acceptance_criteria = [criterion]
  phase assigned by criterion index and complexity score
- Acceptance criteria:
  - Three criteria → three tasks across appropriate phases
  - task_id slugs are unique and deterministic
  - No duplicate tasks generated
- Verification: `python -m pytest tests/ -x`

#### Task 2.4 — Two-pass plan review
- Add agents/plan_critic.py with PlanCriticAgent
- After PlanningAgent generates draft, PlanCriticAgent reviews for:
  missing verification tasks, missing research tasks,
  tasks with no acceptance criteria, phase ordering issues
- Returns list of PlanCritique items, planning agent revises if any
- Acceptance criteria:
  - Plan with no verification task gets one added
  - Plan with empty acceptance criteria gets flagged
  - Revised plan persisted correctly
- Verification: `python -m pytest tests/ -x`

#### Task 2.5 — Historical plan learning
- ManagementAgent stores successful plan templates in state/plan_history.json
- PlanningAgent reads plan_history.json and passes similar prior plans
  to create_plan() as examples
- Similarity matched by: project_name, goal keyword overlap
- Acceptance criteria:
  - Successful run writes plan template to plan_history.json
  - Second run on same project loads prior plan as example
  - plan_history.json capped at 20 entries, oldest removed
- Verification: `python -m pytest tests/ -x`

---

## Phase 3: Model Profiles and Non-Interactive Prompting

### Objective
Give the planning agent explicit knowledge of available models and their
strengths so it can assign the right model to each task. Ensure all
backend prompts communicate non-interactive operation mode clearly.

### Entry criteria
- Phase 2 complete
- OpenRouter models list in backends/openrouter_models.py

### Exit criteria
- model_profiles.yaml exists and is read by planning and routing agents
- Every backend prompt includes non-interactive operation header
- Planning agent assigns model per task based on profile match
- All tests pass

### Tasks

#### Task 3.1 — Create model_profiles.yaml
- Create config/model_profiles.yaml
- One entry per model in OPENROUTER_MODELS plus codex, aider, gemini,
  claude-code
- Fields per model:
  name, provider, strengths (list), weaknesses (list),
  context_window (int), speed (fast/medium/slow),
  cost_tier (low/medium/high), non_interactive (bool),
  best_for (list of task types)
- Acceptance criteria:
  - All models in OPENROUTER_MODELS have a profile entry
  - codex, aider, gemini, claude-code have entries
  - YAML parses without error
  - `python -c "import yaml; yaml.safe_load(open('config/model_profiles.yaml'))"` succeeds
- Verification: `python -m py_compile backends/openrouter_models.py`

#### Task 3.2 — ModelProfileStore loader
- Add runtime/model_profile_store.py
- Loads config/model_profiles.yaml at startup
- Method: get_best_model(task_type, cost_tier, context_size) → model name
- Method: get_profile(model_name) → dict
- Method: get_non_interactive_models() → list
- Acceptance criteria:
  - get_best_model("coding", "low", 8000) returns a valid model name
  - get_profile returns all fields for known model
  - Unknown model returns None without error
- Verification: `python -m pytest tests/test_model_profile_store.py -x`

#### Task 3.3 — Wire ModelProfileStore into routing
- BackendRouter imports ModelProfileStore
- select() consults profile store when routing_mode is auto
- Overrides tag-based selection with profile-based selection
- Acceptance criteria:
  - auto routing returns model matched to task complexity
  - manual and rules routing unaffected
  - OPENROUTER_PREFERRED_MODELS still takes highest priority
- Verification: `python -m pytest tests/test_router.py -x`

#### Task 3.4 — Non-interactive prompt headers
- Add shared prompt header to prompts/shared/non_interactive_header.md
- Content: clear statement that the agent operates non-interactively,
  must not prompt for input, must not ask clarifying questions,
  must make reasonable assumptions and proceed, must output
  machine-parseable results
- CodingBackend base class prepends this header to all prompts on load
- Acceptance criteria:
  - All backend prompts include non-interactive header when loaded
  - Header file exists at prompts/shared/non_interactive_header.md
  - `grep -r "non-interactively" prompts/` finds header in all backends
- Verification: `python -m pytest tests/ -x`

#### Task 3.5 — Model assignment in TaskDocument
- Add model field to TaskDocument (Optional[str], default None)
- PlanningAgent sets model per task from ModelProfileStore
- BackendRouter respects task.model if set, overrides profile selection
- Acceptance criteria:
  - TaskDocument serializes/deserializes model field correctly
  - task.model set by planner appears in routing decision
  - task.model=None falls through to normal routing
- Verification: `python -m pytest tests/ -x`

---

## Phase 4: Verification Feedback Loop

### Objective
Transform verification from a pass/fail gate into a correction loop.
Failed verification classifies the failure type, constructs an enriched
retry prompt, and re-runs the backend up to a configurable tier limit
before escalating to human or marking blocked.

### Entry criteria
- Phase 3 complete
- Verification profiles working (minimal, default, strict)

### Exit criteria
- Verification failures trigger classified retry with enriched prompt
- Retry tiers: same model → stronger model → human checkpoint
- Loop limit configurable per tier
- Blocked tasks persist full context for human review
- All tests pass

### Tasks

#### Task 4.1 — Failure classifier
- Add runtime/failure_classifier.py
- Input: VerificationReport, list of BackendExecution
- Output: FailureClassification dataclass with fields:
  failure_type (syntax/import/test/missing_file/logic/unknown),
  affected_files (list), failure_detail (str), retry_likely (bool),
  suggested_focus (str)
- Classification rules:
  - SyntaxError in stderr → syntax
  - ImportError/ModuleNotFoundError → import
  - pytest FAILED → test, extract test name and assertion
  - FileNotFoundError → missing_file
  - exit_code != 0 with no recognized pattern → unknown
  - Repeated same failure across retries → logic
- Acceptance criteria:
  - SyntaxError stderr classified as syntax with retry_likely=True
  - pytest failure extracts failing test name into failure_detail
  - Unknown failures have retry_likely=False after 2nd occurrence
- Verification: `python -m pytest tests/test_failure_classifier.py -x`

#### Task 4.2 — Retry prompt builder
- Add runtime/retry_prompt_builder.py
- Input: original TaskDocument, FailureClassification,
  list of prior BackendExecution attempts, attempt number
- Output: enriched TaskDocument with description augmented with:
  failure type and detail, exact stderr/stdout from failed attempt,
  list of files changed in prior attempt,
  explicit instruction not to repeat same approach
- On attempt 2+: include diff summary of what prior attempt changed
- Acceptance criteria:
  - Retry task description contains failure_detail from classifier
  - Retry task description contains changed files from prior attempt
  - Attempt 3 description includes diff summary
  - Original acceptance_criteria preserved unchanged
- Verification: `python -m pytest tests/test_retry_prompt_builder.py -x`

#### Task 4.3 — Tiered retry loop in supervisor
- Add retry loop to verification_node in orchestrator/supervisor.py
- Tier config in AppConfig:
  max_retries_tier_1 (default 2, same model)
  max_retries_tier_2 (default 1, stronger model from profile store)
  max_retries_tier_3 (default 1, human checkpoint)
- Loop: on verification failure, classify → build retry task →
  re-execute backend → re-verify → check tier limits → escalate
- On tier 3 exhaustion: mark task blocked, persist all attempt context
  to reports/blocked-{task_id}-{run_id}.json, stop gracefully
- Acceptance criteria:
  - Syntax error triggers retry with enriched prompt
  - After tier_1 exhaustion, stronger model used for tier_2
  - After all tiers exhausted, blocked report written
  - Passing verification exits loop immediately
  - Loop never exceeds max_retries_tier_1 + tier_2 + tier_3 total
- Verification: `python -m pytest tests/test_retry_loop.py -x`

#### Task 4.4 — Retry configuration in .env and config
- Add to config.py RetrySettings dataclass:
  max_retries_tier_1, max_retries_tier_2, max_retries_tier_3,
  retry_delay_seconds (default 2)
- Load from env: RETRY_TIER_1, RETRY_TIER_2, RETRY_TIER_3,
  RETRY_DELAY_SECONDS
- Add to make targets: make config-show displays retry settings
- Acceptance criteria:
  - Default values applied when env vars not set
  - RETRY_TIER_1=0 disables tier 1 retries
  - config-show includes retry settings in output
- Verification: `python -m pytest tests/ -x`

#### Task 4.5 — Blocked task resume
- Add scripts/ops.py command: task-resume --task-id <id>
- Reads blocked report from reports/blocked-{task_id}-*.json
- Re-queues task with full prior context as a new run
- Add make target: make task-resume TASK=<id>
- Acceptance criteria:
  - task-resume loads blocked report and creates new TaskDocument
  - New task description includes all prior attempt summaries
  - make task-resume TASK=<id> runs without error
- Verification: `python -m pytest tests/ -x`

---

## Phase 5: Branch-Per-Run and PR Workflow

### Objective
Ensure all backend execution happens on isolated git branches.
Nothing touches main directly. Completed runs leave a branch ready
for human review and merge. Make targets support the full review
and merge workflow.

### Entry criteria
- Phase 4 complete
- Git available in working directory

### Exit criteria
- Every run creates and switches to abracapocus/{task_id}-{date} branch
- All file changes committed to run branch automatically
- main never touched by automated runs
- make pr, make merge, make abandon targets functional
- All tests pass

### Tasks

#### Task 5.1 — GitManager utility
- Add runtime/git_manager.py with GitManager class
- Methods:
  create_branch(branch_name) → bool
  current_branch() → str
  commit_changes(message) → bool
  branch_exists(branch_name) → bool
  get_changed_files() → list
  safe_to_run() → bool (checks not on main/master)
- All methods use subprocess, no external git libraries
- Acceptance criteria:
  - create_branch creates and checks out branch
  - commit_changes stages all changes and commits with message
  - safe_to_run returns False when on main or master
  - All methods handle git-not-initialized gracefully
- Verification: `python -m pytest tests/test_git_manager.py -x`

#### Task 5.2 — Branch creation in supervisor run()
- SupervisorOrchestrator.run() calls GitManager at start
- If safe_to_run() is False and ABRACAPOCUS_ALLOW_MAIN not set,
  raise RuntimeError with clear message
- Branch name format: abracapocus/{task_id}-{YYYYMMDD}-{run_id[:8]}
- Branch created before planning_node executes
- Branch name stored in run metadata
- Acceptance criteria:
  - Every run creates a new branch before any file changes
  - Run on main without ABRACAPOCUS_ALLOW_MAIN raises error
  - Branch name appears in OrchestrationReport metadata
  - ABRACAPOCUS_ALLOW_MAIN=true bypasses protection
- Verification: `python -m pytest tests/ -x`

#### Task 5.3 — Auto-commit after successful phase
- phase_advance node calls GitManager.commit_changes() after
  each phase completes successfully
- Commit message format:
  abracapocus: phase {phase_name} complete [{run_id[:8]}]
- Only commits if changed_files non-empty
- Acceptance criteria:
  - Successful phase produces a git commit on run branch
  - Empty phase (no file changes) skips commit silently
  - Commit message includes phase name and run id
- Verification: `python -m pytest tests/ -x`

#### Task 5.4 — PR and merge make targets
- Add to scripts/ops.py: branch-show, merge, abandon
- branch-show: print current run branch name and status
- merge: git merge --no-ff run branch into base branch, push if remote
- abandon: git checkout base branch, delete run branch
- Add make targets: make branch-show, make merge TASK=<id>,
  make abandon TASK=<id>
- Acceptance criteria:
  - make branch-show prints branch name for last run
  - make merge merges run branch with no-ff commit
  - make abandon deletes run branch and returns to base
  - All targets handle no-git-repo gracefully
- Verification: `python -m pytest tests/ -x`

#### Task 5.5 — Branch protection config and docs
- Add ABRACAPOCUS_ALLOW_MAIN, ABRACAPOCUS_BASE_BRANCH to .env.example
- Add branch workflow section to docs/QUICKSTART.md
- Default base branch: main, overridable via ABRACAPOCUS_BASE_BRANCH
- Acceptance criteria:
  - .env.example documents both variables with comments
  - QUICKSTART.md explains branch workflow end to end
  - ABRACAPOCUS_BASE_BRANCH=develop routes merges to develop
- Verification: `python -m pytest tests/ -x`

---

## Phase 6: Backend Hardening and Pace Control

### Objective
Make all backends reliable for unattended operation. Add retry with
exponential backoff, rate limit awareness, fallback model chains,
and pace control. Tune each backend's command construction for
non-interactive production use.

### Entry criteria
- Phase 5 complete
- All backends have supports_direct_execution set correctly

### Exit criteria
- All backends retry on transient failures with backoff
- Rate limit responses trigger pace control not hard failure
- Fallback model chain executes automatically on model failure
- Per-backend pace settings configurable via env
- All tests pass

### Tasks

#### Task 6.1 — Retry and backoff in CodingBackend base
- Add to backends/base.py:
  max_retries (default 3), retry_delay_base (default 2.0)
- execute() wraps subprocess call in retry loop
- Exponential backoff with jitter: delay = base * (2^attempt) + random(0,1)
- Retry on: exit_code 1 with rate-limit keywords in stderr,
  subprocess.TimeoutExpired, ConnectionError
- Do not retry on: exit_code 2 (bad args), FileNotFoundError
- Acceptance criteria:
  - Rate limit stderr triggers retry with backoff delay
  - TimeoutExpired retries up to max_retries
  - Bad args (exit_code 2) fails immediately without retry
  - Total retry count logged per execution
- Verification: `python -m pytest tests/test_backend_retry.py -x`

#### Task 6.2 — Fallback model chain
- RoutingDecision already has models list
- If primary model execution fails after retries, execute() moves
  to next model in decision.models list automatically
- BackendResult includes model_attempts list showing all tried models
- Acceptance criteria:
  - Two-model list tries second model on first model failure
  - model_attempts in BackendResult lists all tried models in order
  - All models exhausted returns failure with full attempt log
- Verification: `python -m pytest tests/ -x`

#### Task 6.3 — Pace control per backend
- Add PaceSettings to config.py:
  min_seconds_between_calls (default 0), max_calls_per_minute (default 0)
- Load per-backend from env:
  AIDER_MIN_DELAY, GEMINI_MIN_DELAY, CODEX_MIN_DELAY
- CodingBackend base tracks last_call_time, sleeps if needed
- max_calls_per_minute=0 means unlimited
- Acceptance criteria:
  - AIDER_MIN_DELAY=5 causes 5 second minimum between aider calls
  - Pace delay logged at INFO level
  - max_calls_per_minute enforced with blocking sleep
- Verification: `python -m pytest tests/test_pace_control.py -x`

#### Task 6.4 — Gemini CLI command hardening
- Run gemini --help and update backends/gemini_cli.py build_command
  to match real CLI interface same as codex fix in session
- Add non-interactive flags appropriate to gemini CLI
- Acceptance criteria:
  - build_command produces valid gemini CLI invocation
  - --help output flags matched in command construction
  - py_compile passes
- Verification: `python -m py_compile backends/gemini_cli.py && python -m pytest tests/ -x`

#### Task 6.5 — Claude Code CLI hardening
- Install claude-code: npm install -g @anthropic-ai/claude-code
- Run claude --help and update backends/claude_code_cli.py build_command
- Set supports_direct_execution = True
- Add ANTHROPIC_API_KEY to .env.example
- Acceptance criteria:
  - claude --help succeeds in shell
  - build_command produces valid claude CLI invocation
  - supports_direct_execution = True
  - ANTHROPIC_API_KEY documented in .env.example
- Verification: `python -m py_compile backends/claude_code_cli.py && python -m pytest tests/ -x`

#### Task 6.6 — End-to-end hardening test suite
- Add tests/test_e2e_hardening.py
- Tests covering: retry behavior, fallback chain, pace control,
  branch creation, blocked task persistence
- All tests use monkeypatch, no real CLI calls
- Acceptance criteria:
  - All hardening tests pass in CI without external dependencies
  - Coverage report shows >80% on runtime/ and backends/
- Verification: `python -m pytest tests/test_e2e_hardening.py -v`

---

## Execution Notes

- Run phases in order — each phase exit criteria is the next phase entry criteria
- Use `make test` as the baseline pass/fail after every task
- Use `DEEP_AGENT_MOCK_MODE=true` throughout unless specifically testing real agent behavior
- Commit after every task: `git add -A && git commit -m "feat: {task_id} {title}"`
- Use `make task-run TASK=<task_id>` to execute each task through the system itself
  once Phase 2 is stable enough to self-direct
EOF
