"""Curated OpenRouter model registry for the Aider backend."""
from __future__ import annotations

OPENROUTER_MODELS = [
    {"name": "openrouter/qwen/qwen3-coder-next", "tags": ["coding_strong", "reasoning_strong"], "context": 128000},
    {"name": "openrouter/qwen/qwen3-235b-a22b-2507", "tags": ["coding_strong"], "context": 128000},
    {"name": "openrouter/deepseek/deepseek-v3.2", "tags": ["coding_strong", "reasoning_strong"], "context": 128000},
    {"name": "openrouter/z-ai/glm-4.7-flash", "tags": ["cheap_fast", "coding"], "context": 64000},
    {"name": "openrouter/phind/codellama-34b-v2", "tags": ["coding"], "context": 4096},
    {"name": "openrouter/meta-llama/codellama-34b-instruct", "tags": ["coding"], "context": 8192},
    {"name": "openrouter/mistralai/mistral-openorca-7b", "tags": ["general", "cheap_fast"], "context": 8192},
    {"name": "openrouter/teknium/openhermes-2-mistral-7b", "tags": ["general"], "context": 8192},
    {"name": "openrouter/nousresearch/hermes-70b", "tags": ["reasoning_strong"], "context": 4096},
    {"name": "openrouter/nousresearch/hermes-13b", "tags": ["reasoning"], "context": 4096},
    {"name": "openrouter/xwin/xwin-70b", "tags": ["reasoning_strong"], "context": 8192},
    {"name": "openrouter/migtissera/synthia-70b", "tags": ["reasoning_strong"], "context": 8192},
    {"name": "openrouter/huggingfaceh4/zephyr-7b", "tags": ["cheap_fast"], "context": 4096},
    {"name": "openrouter/meta-llama/llama-2-13b-chat", "tags": ["cheap_fast"], "context": 4096},
    {"name": "openrouter/meta-llama/llama-2-70b-chat", "tags": ["general"], "context": 4096},
    {"name": "openrouter/jondurbin/airoboros-70b", "tags": ["experimental", "reasoning"], "context": 4096},
    {"name": "openrouter/pygmalionai/mythalion-13b", "tags": ["experimental"], "context": 8192},
]
