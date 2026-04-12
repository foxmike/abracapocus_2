# abracapocus_2 Gap Analysis

## What's Real and Working

- Full orchestration pipeline runs end-to-end in mock mode
- `demo_cli` backend executes real subprocess (`scripts/demo_improvement.py`)
- `codex_cli` has `supports_direct_execution = True` and `codex` is installed
- `aider` and `gemini` CLIs are installed
- `claude-code` is NOT installed (`none found`)
- All verification profiles work (py_compile, selfcheck, pytest)
- State, routing, plans, reports — all functional

## Critical Gaps

1. **No real execution for aider/gemini** — both backends have `supports_direct_execution = False` (not set), so they always dry-run regardless of CLI availability. Only `codex_cli` and `demo_cli` can actually write files.

2. **`claude-code` not installed** — `claude_code_cli` backend will always dry-run. Either install it or flip `supports_direct_execution = True` once you do.

3. **aider's `build_command` is broken for real use** — `--files` takes a comma-joined string but aider expects separate positional args. Will fail on real execution.

4. **`DeepAgentFactory` can never load real Deep Agents** — the import candidates (`langchain.agents.deep_agents.base`, etc.) don't exist in langchain 1.2.x or langgraph 1.1.x. Mock mode is the only mode, permanently, until this is resolved. The "real LangChain Deep Agents" path is dead code.

5. **`PlanningAgent` only runs the first phase/task** — `_select_task` returns on the first task it finds. Multi-phase plans never advance past task 1.

6. **`openrouter_models.py` not reviewed** — the router imports `OPENROUTER_MODELS` from it but contents are unknown. If it's empty, aider routing produces no models.

## Priority Queue

- **Make aider/gemini execute for real** → flip `supports_direct_execution = True`, fix aider's `build_command`
- **Hook up a real LLM** → the Deep Agents path is fictional; replace `LocalDeepAgent` with direct LangChain/LangGraph calls using existing installs
- **Multi-task execution** → fix `_select_task` to iterate properly across phases
- **Wire claude-code** → `npm install -g @anthropic-ai/claude-code` or equivalent
