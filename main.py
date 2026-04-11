"""CLI entrypoint for abracapocus_2."""
from __future__ import annotations

import json
import sys

import typer
from rich import print as rich_print

from config import load_config
from models.project import ProjectRequest
from orchestrator.supervisor import SupervisorOrchestrator, run_demo
from runtime.state_store import StateStore

app = typer.Typer(help="LangChain Deep Agents orchestrator")


def _execute_run(goal: str, context: str) -> None:
    config = load_config()
    orchestrator = SupervisorOrchestrator(config)
    request = ProjectRequest(
        project_name=config.project_name,
        goal=goal,
        context=context,
    )
    report = orchestrator.run(request)
    rich_print({"run_id": report.metadata["run_id"], "backend": report.backend_execution.backend})
    print(report.model_dump_json(indent=2))


@app.command()
def run(goal: str = typer.Option(..., help="Goal to execute"), context: str = typer.Option("", help="Additional context")) -> None:
    """Run an orchestration flow."""
    _execute_run(goal, context)


@app.command()
def demo() -> None:
    """Run the built-in demo scenario."""
    report = run_demo()
    typer.echo(report.model_dump_json(indent=2))


@app.command("state")
def state_show() -> None:
    """Print current runtime state."""
    config = load_config()
    state = StateStore(config).read_state()
    typer.echo(state.model_dump_json(indent=2))


if __name__ == "__main__":
    if len(sys.argv) == 1:
        typer.echo("No arguments provided; running default demo goal")
        _execute_run("Demonstrate Deep Agents orchestration", "auto-demo")
    else:
        app()
