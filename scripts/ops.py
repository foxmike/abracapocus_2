"""Operational CLI used by the Makefile."""
from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path
from typing import List, Optional

import typer

from backends.registry import REGISTRY
from config import load_config
from models.plan import Plan
from models.project import ProjectRequest, TaskDocument
from orchestrator.supervisor import SupervisorOrchestrator
from runtime.git_manager import GitManager
from runtime.state_store import StateStore
from runtime.context_store import ContextStore

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
def task_resume(
    task_id: str = typer.Option(..., "--task-id"),
    context: str = typer.Option("", "--context"),
) -> None:
    config = load_config()
    blocked_path = _latest_blocked_report(config.paths.reports_dir, task_id)
    blocked_payload = json.loads(blocked_path.read_text(encoding="utf-8"))
    resumed_task = _task_from_blocked_payload(blocked_payload, blocked_path)
    request = ProjectRequest(
        project_name=config.project_name,
        goal=resumed_task.description or resumed_task.title,
        context=context or f"resume:{resumed_task.task_id}:{blocked_path.name}",
    )
    orchestrator = SupervisorOrchestrator(config)
    report = orchestrator.run(request, task=resumed_task)
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
def context_index() -> None:
    config = load_config()
    store = ContextStore()
    store.index_repo(config.paths.working_root)
    typer.echo(f"Context index built at {config.paths.working_root / 'state' / 'chroma'}")


@app.command()
def context_reset() -> None:
    config = load_config()
    chroma_dir = config.paths.working_root / "state" / "chroma"
    if chroma_dir.exists():
        shutil.rmtree(chroma_dir)
    store = ContextStore()
    store.index_repo(config.paths.working_root)
    typer.echo(f"Context index reset at {chroma_dir}")


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
            "working_root": str(config.paths.working_root),
            "retry": {
                "max_retries_tier_1": config.retry.max_retries_tier_1,
                "max_retries_tier_2": config.retry.max_retries_tier_2,
                "max_retries_tier_3": config.retry.max_retries_tier_3,
                "retry_delay_seconds": config.retry.retry_delay_seconds,
            },
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
def branch_show() -> None:
    config = load_config()
    git = GitManager(config.paths.root_dir)
    current = git.current_branch()
    if not current:
        typer.echo("No git repository detected")
        return
    report_payload = _latest_run_report_payload(config.paths.reports_dir)
    run_branch = _extract_branch_name(report_payload) or current
    status = "dirty" if git.get_changed_files() else "clean"
    typer.echo(json.dumps({"branch": run_branch, "current": current, "status": status}, indent=2))


@app.command()
def merge(task_id: str = typer.Option(..., "--task-id")) -> None:
    config = load_config()
    git = GitManager(config.paths.root_dir)
    if not git.current_branch():
        typer.echo("No git repository detected")
        return
    payload = _latest_run_report_payload(config.paths.reports_dir, task_id=task_id)
    if payload is None:
        typer.echo(f"No run report found for task_id '{task_id}'")
        return
    run_branch = _extract_branch_name(payload)
    if not run_branch:
        typer.echo(f"Run report for task_id '{task_id}' does not contain branch_name")
        return
    if not _run_git(config.paths.root_dir, ["checkout", git.base_branch]):
        raise typer.Exit(code=1)
    if not _run_git(config.paths.root_dir, ["merge", "--no-ff", run_branch]):
        raise typer.Exit(code=1)
    if _run_git(config.paths.root_dir, ["remote", "get-url", "origin"], quiet=True):
        _run_git(config.paths.root_dir, ["push", "origin", git.base_branch], quiet=True)
    typer.echo(f"Merged {run_branch} into {git.base_branch}")


@app.command()
def abandon(task_id: str = typer.Option(..., "--task-id")) -> None:
    config = load_config()
    git = GitManager(config.paths.root_dir)
    if not git.current_branch():
        typer.echo("No git repository detected")
        return
    payload = _latest_run_report_payload(config.paths.reports_dir, task_id=task_id)
    if payload is None:
        typer.echo(f"No run report found for task_id '{task_id}'")
        return
    run_branch = _extract_branch_name(payload)
    if not run_branch:
        typer.echo(f"Run report for task_id '{task_id}' does not contain branch_name")
        return
    if not _run_git(config.paths.root_dir, ["checkout", git.base_branch]):
        raise typer.Exit(code=1)
    if not _run_git(config.paths.root_dir, ["branch", "-D", run_branch]):
        raise typer.Exit(code=1)
    typer.echo(f"Abandoned {run_branch} and returned to {git.base_branch}")


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


def _latest_blocked_report(reports_dir: Path, task_id: str) -> Path:
    candidates = sorted(reports_dir.glob(f"blocked-{task_id}-*.json"), key=lambda path: path.stat().st_mtime)
    if not candidates:
        raise typer.BadParameter(f"No blocked report found for task_id '{task_id}' in {reports_dir}")
    return candidates[-1]


def _latest_run_report_payload(reports_dir: Path, task_id: str | None = None) -> dict | None:
    reports = sorted(reports_dir.glob("run-*.json"), key=lambda path: path.stat().st_mtime, reverse=True)
    for report_path in reports:
        payload = json.loads(report_path.read_text(encoding="utf-8"))
        metadata = payload.get("metadata") or {}
        if task_id is None or metadata.get("task_id") == task_id:
            return payload
    return None


def _extract_branch_name(report_payload: dict | None) -> str:
    if not report_payload:
        return ""
    metadata = report_payload.get("metadata") or {}
    branch_name = metadata.get("branch_name")
    return str(branch_name) if branch_name else ""


def _run_git(repo_root: Path, args: List[str], quiet: bool = False) -> bool:
    command = ["git", *args]
    result = subprocess.run(command, cwd=repo_root, capture_output=True, text=True)
    if result.returncode == 0:
        return True
    if not quiet:
        error = result.stderr.strip() or result.stdout.strip() or "git command failed"
        typer.echo(error)
    return False


def _task_from_blocked_payload(payload: dict, blocked_path: Path) -> TaskDocument:
    task_payload = payload.get("task")
    if not isinstance(task_payload, dict):
        raise typer.BadParameter(f"Blocked report {blocked_path} is missing task payload")
    task = TaskDocument.model_validate(task_payload)
    attempt_summaries = _render_attempt_summaries(payload.get("attempts") or [])
    resume_context = "\n".join(
        [
            f"Resume source: {blocked_path.name}",
            "Prior attempts context:",
            attempt_summaries,
        ]
    )
    description = f"{task.description}\n\n{resume_context}".strip()
    return task.model_copy(update={"description": description, "status": "pending"})


def _render_attempt_summaries(attempts: list) -> str:
    if not attempts:
        return "No prior attempts recorded"
    lines: List[str] = []
    for index, attempt in enumerate(attempts, start=1):
        if not isinstance(attempt, dict):
            continue
        changed_files = []
        for changed in attempt.get("changed_files") or []:
            if not isinstance(changed, dict):
                continue
            path = changed.get("path") or changed.get("file")
            if isinstance(path, str) and path:
                changed_files.append(path)
        lines.extend(
            [
                f"Attempt {index}: backend={attempt.get('backend')} model={attempt.get('model') or 'default'} exit_code={attempt.get('exit_code')}",
                f"stdout:\n{attempt.get('stdout') or ''}",
                f"stderr:\n{attempt.get('stderr') or ''}",
                f"diff_summary:\n{attempt.get('diff_summary') or ''}",
                f"changed_files: {', '.join(changed_files) if changed_files else 'none'}",
            ]
        )
    return "\n\n".join(lines)


if __name__ == "__main__":
    app()
