"""Operational CLI used by the Makefile."""
from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import List, Optional

import typer

from backends.registry import REGISTRY
from config import load_config
from models.plan import Plan
from models.project import ProjectRequest, TaskDocument
from orchestrator.supervisor import SupervisorOrchestrator
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
def task_init(
    task_id: str,
    title: str,
    phase: str,
    description: str = typer.Option(""),
    acceptance: List[str] = typer.Option([], "--acceptance", "-a"),
    backend: Optional[str] = typer.Option(None, "--backend"),
    verification_profile: Optional[str] = typer.Option(None, "--profile"),
) -> None:
    task = TaskDocument(
        task_id=task_id,
        title=title,
        phase=phase,
        description=description,
        acceptance_criteria=list(acceptance),
        selected_backend=backend,
        verification_profile=verification_profile,
    )
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
def task_run(task_id: str, context: str = typer.Option("", "--context")) -> None:
    task, path = _load_task(task_id)
    config = load_config()
    request = ProjectRequest(
        project_name=config.project_name,
        goal=task.description or task.title,
        context=context or f"task:{task.task_id}",
    )
    orchestrator = SupervisorOrchestrator(config)
    report = orchestrator.run(request, task=task)
    typer.echo(report.model_dump_json(indent=2))


@app.command()
def task_verify(profile: Optional[str] = typer.Option(None, "--profile")) -> None:
    config = load_config()
    profile_name = profile or config.verification.active_profile
    try:
        checks = config.verification.active_checks(profile_name)
    except ValueError as exc:  # pragma: no cover
        typer.echo(str(exc))
        raise typer.Exit(code=1)
    typer.echo(f"Running verification profile: {profile_name}")
    failed = False
    for check in checks:
        typer.echo(f"$ {' '.join(check.command)}")
        result = subprocess.run(
            check.command,
            cwd=config.paths.root_dir,
            text=True,
        )
        status = "ok" if result.returncode == 0 else "failed"
        typer.echo(f"-> {check.name}: {status}")
        if result.returncode != 0:
            failed = True
    raise typer.Exit(code=1 if failed else 0)


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
    config = load_config()
    store = StateStore(config)

    def _update(state):
        state.default_backend = descriptor.name
        overrides = dict(state.operator_overrides)
        overrides["backend"] = descriptor.name
        state.operator_overrides = overrides
        return state

    store.update(_update)
    typer.echo(f"Backend override set to {descriptor.name}")


@app.command()
def verification_set(profile: str) -> None:
    config = load_config()
    if not config.verification.has_profile(profile):
        raise typer.BadParameter(f"Unknown verification profile '{profile}'")
    store = StateStore(config)

    def _update(state):
        overrides = dict(state.operator_overrides)
        overrides["verification_profile"] = profile
        state.operator_overrides = overrides
        return state

    store.update(_update)
    typer.echo(f"Verification profile override set to {profile}")


@app.command()
def agent_set(name: str, enable: bool = typer.Option(True, "--enable/--disable")) -> None:
    if name not in {"reviewer", "verifier"}:
        raise typer.BadParameter("Agent name must be 'reviewer' or 'verifier'")
    store = StateStore(load_config())

    def _update(state):
        overrides = dict(state.operator_overrides)
        agents = dict(overrides.get("agents") or {})
        agents[name] = enable
        overrides["agents"] = agents
        state.operator_overrides = overrides
        return state

    store.update(_update)
    status = "enabled" if enable else "disabled"
    typer.echo(f"{name} agent {status}")


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


def _load_task(task_id: str) -> tuple[TaskDocument, Path]:
    path = Path(task_id)
    if path.suffix != ".json":
        path = Path("tasks") / f"{task_id}.json"
    if not path.exists():
        raise typer.BadParameter(f"Task file {path} not found")
    data = json.loads(path.read_text(encoding="utf-8"))
    return TaskDocument(**data), path


if __name__ == "__main__":
    app()
