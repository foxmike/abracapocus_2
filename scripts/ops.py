"""Operational CLI used by the Makefile."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Optional

import typer

from backends.registry import REGISTRY
from config import load_config
from models.plan import Plan
from models.project import TaskDocument
from runtime.state_store import StateStore

app = typer.Typer(help="Operational helpers")


@app.command()
def plan_init(name: str = typer.Option("master"), summary: str = typer.Option("Master plan")) -> None:
    config = load_config()
    plan = Plan(project_name=config.project_name, summary=summary, phases=[])
    path = Path("plans") / f"{name}.json"
    path.write_text(plan.model_dump_json(indent=2), encoding="utf-8")
    typer.echo(f"Plan written to {path}")


@app.command()
def plan_show(name: str = typer.Option("master")) -> None:
    path = Path("plans") / f"{name}.json"
    typer.echo(path.read_text(encoding="utf-8"))


@app.command()
def phase_init(name: str, objective: str = typer.Option("")) -> None:
    path = Path("phases") / f"{name}.json"
    payload = {"name": name, "objective": objective, "tasks": []}
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    typer.echo(f"Phase file created at {path}")


@app.command()
def phase_show(name: str) -> None:
    path = Path("phases") / f"{name}.json"
    typer.echo(path.read_text(encoding="utf-8"))


@app.command()
def task_init(task_id: str, title: str, phase: str, description: str = typer.Option("")) -> None:
    task = TaskDocument(task_id=task_id, title=title, phase=phase, description=description)
    path = Path("tasks") / f"{task_id}.json"
    path.write_text(task.model_dump_json(indent=2), encoding="utf-8")
    typer.echo(f"Task stored at {path}")


@app.command()
def task_list() -> None:
    for path in sorted(Path("tasks").glob("*.json")):
        typer.echo(path.name)


@app.command()
def task_show(task_id: str) -> None:
    path = Path("tasks") / f"{task_id}.json"
    typer.echo(path.read_text(encoding="utf-8"))


@app.command()
def state_show() -> None:
    state = StateStore(load_config()).read_state()
    typer.echo(state.model_dump_json(indent=2))


@app.command()
def state_reset() -> None:
    store = StateStore(load_config())
    store.reset()
    typer.echo("Runtime state reset")


@app.command()
def backend_list() -> None:
    for descriptor in REGISTRY.list_backends():
        typer.echo(f"{descriptor.name}: {descriptor.description}")


@app.command()
def backend_set(name: str) -> None:
    descriptor = REGISTRY.describe(name)
    store = StateStore(load_config())
    store.update(lambda state: state.model_copy(update={"default_backend": descriptor.name}))
    typer.echo(f"Default backend set to {descriptor.name}")


@app.command()
def config_show() -> None:
    config = load_config()
    typer.echo(json.dumps(
        {
            "project_name": config.project_name,
            "environment": config.environment,
            "default_backend": config.default_backend,
            "routing_mode": config.routing.routing_mode,
        },
        indent=2,
    ))


@app.command()
def prompt_show(name: str) -> None:
    path = Path("prompts") / f"{name}.md"
    typer.echo(path.read_text(encoding="utf-8"))


@app.command()
def skill_list() -> None:
    for path in sorted(Path("skills").glob("*/SKILL.md")):
        typer.echo(str(path))


@app.command()
def report_show(run_id: Optional[str] = None) -> None:
    reports = sorted(Path("reports").glob("run-*.json"))
    if not reports:
        typer.echo("No reports available")
        return
    target = None
    if run_id:
        path = Path("reports") / f"run-{run_id}.json"
        if path.exists():
            target = path
    if target is None:
        target = reports[-1]
    typer.echo(target.read_text(encoding="utf-8"))


@app.command()
def tree() -> None:
    for path in Path('.').rglob('*'):
        if any(part.startswith('.git') for part in path.parts):
            continue
        typer.echo(str(path))


if __name__ == "__main__":
    app()
