PYTHON ?= python
PIP ?= pip
GOAL ?= Deliver autonomous scaffold
CONTEXT ?= operator-demo
PLAN_NAME ?= master
PHASE ?= phase-1
TASK ?=
PROMPT ?= supervisor
NAME ?= codex_cli
SKILL ?=

.PHONY: help install setup run demo test lint format clean tree docs state-show state-reset \
	plan-init plan-show phase-init phase-show task-init task-list task-show task-run task-verify \
	report-show backend-list backend-set agent-list config-show prompt-show skill-list plan-init

help: ## Show available targets
	@grep -E '^[a-zA-Z_-]+:.*?##' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS=":.*?##"} {printf "%-20s %s\n", $$1, $$2}'

install: ## Install Python dependencies
	$(PIP) install -r requirements.txt

setup: install state-reset plan-init ## Install deps and bootstrap plan/state

run: ## Run orchestration with GOAL and CONTEXT
	$(PYTHON) main.py run --goal "$(GOAL)" --context "$(CONTEXT)"

demo: ## Run built-in demo flow
	$(PYTHON) main.py

test: ## Run pytest suite
	$(PYTHON) -m pytest

lint: ## Run static analysis (ruff)
	$(PYTHON) -m ruff check agents backends models orchestrator runtime scripts

format: ## Format code with ruff format
	$(PYTHON) -m ruff format agents backends models orchestrator runtime scripts main.py config.py

clean: ## Remove caches and temporary files
	find . -name '__pycache__' -prune -exec rm -rf {} +
	rm -rf .pytest_cache reports/run-*.json

 tree: ## Print repo tree
	$(PYTHON) -m scripts.ops tree

 docs: ## List docs directory contents
	@ls docs

state-show: ## Show runtime state
	$(PYTHON) -m scripts.ops state-show

state-reset: ## Reset runtime state
	$(PYTHON) -m scripts.ops state-reset

plan-init: ## Initialize a plan document
	$(PYTHON) -m scripts.ops plan-init --name $(PLAN_NAME)

plan-show: ## Show plan document
	$(PYTHON) -m scripts.ops plan-show --name $(PLAN_NAME)

phase-init: ## Initialize a phase document
	$(PYTHON) -m scripts.ops phase-init --name $(PHASE)

phase-show: ## Show a phase document
	$(PYTHON) -m scripts.ops phase-show --name $(PHASE)

task-init: ## Initialize a task document
	@if [ -z "$(TASK)" ]; then echo "Set TASK=<id>"; exit 1; fi
	$(PYTHON) -m scripts.ops task-init --task-id $(TASK) --title "$(GOAL)" --phase $(PHASE)

task-list: ## List task documents
	$(PYTHON) -m scripts.ops task-list

task-show: ## Show a task document
	@if [ -z "$(TASK)" ]; then echo "Set TASK=<id>"; exit 1; fi
	$(PYTHON) -m scripts.ops task-show --task-id $(TASK)

task-run: ## Run supervisor using TASK json file
	@if [ -z "$(TASK)" ]; then echo "Set TASK=tasks/<file>.json"; exit 1; fi
	@$(PYTHON) - <<'PY'
import json
from pathlib import Path
from config import load_config
from models.project import ProjectRequest, TaskDocument
from orchestrator.supervisor import SupervisorOrchestrator
path = Path("$(TASK)")
if not path.exists():
    raise SystemExit(f"Task file {path} missing")
task = TaskDocument(**json.loads(path.read_text()))
config = load_config()
request = ProjectRequest(project_name=config.project_name, goal=task.description or task.title, context=f"phase:{task.phase}")
SupervisorOrchestrator(config).run(request)
PY

task-verify: ## Run deterministic verification only
	$(PYTHON) -m pytest tests/test_verifier_contracts.py

report-show: ## Show latest or specific report
	$(PYTHON) -m scripts.ops report-show

backend-list: ## List registered backends
	$(PYTHON) -m scripts.ops backend-list

backend-set: ## Set default backend in state store
	$(PYTHON) -m scripts.ops backend-set --name $(NAME)

agent-list: ## List configured agents
	@printf "%s\n" supervisor planning_agent research_agent management_agent reviewer_agent verifier_agent

config-show: ## Display runtime config
	$(PYTHON) -m scripts.ops config-show

prompt-show: ## Display an agent/backend prompt
	$(PYTHON) -m scripts.ops prompt-show --name $(PROMPT)

skill-list: ## List available skills
	$(PYTHON) -m scripts.ops skill-list
