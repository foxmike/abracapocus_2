# abracapocus_2 Gap Analysis

## Status: All original gaps resolved as of 2026-04-12

## Resolved
1. ✅ aider/gemini `supports_direct_execution = True` — both execute for real
2. ✅ claude-code noted — flip `supports_direct_execution = True` after `npm install -g @anthropic-ai/claude-code`
3. ✅ aider `build_command` fixed — files passed as separate `--file` args
4. ✅ deepagents factory wired — `pip install deepagents`, correct `create_deep_agent` API
5. ✅ LangGraph supervisor — parallel task execution, phase gating, human checkpoints, SQLite durability
6. ✅ `OPENROUTER_PREFERRED_MODELS` env var — bypasses tag scoring when set

## New item identified during session
7. **codex `build_command` uses wrong CLI args** — current command passes `--id`,
   `--title`, `--phase`, `--context`, `--acceptance` flags but real codex CLI
   does not accept these. Needs update to match actual `codex` CLI interface.
   Run `codex --help` to get current arg spec before fixing.

## Next actions
- Fix item 7: run `codex --help`, generate Codex prompt to fix `backends/codex_cli.py`
- Install claude-code and flip `supports_direct_execution`
- Set `DEEP_AGENT_MOCK_MODE=false` and `OPENAI_API_KEY` for first real agent run
