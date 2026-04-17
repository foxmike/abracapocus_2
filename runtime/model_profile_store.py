"""Runtime loader and selector for model profiles."""
from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml


class ModelProfileStore:
    """Load model profiles from YAML and expose lookup helpers."""

    _COST_RANK = {"low": 0, "medium": 1, "high": 2}

    def __init__(self, path: str | Path = "config/model_profiles.yaml") -> None:
        self.path = Path(path)
        self._profiles = self._load_profiles()
        self._by_name = {
            str(profile.get("name")): profile
            for profile in self._profiles
            if profile.get("name")
        }

    def get_profile(self, model_name: str) -> dict[str, Any] | None:
        """Return profile for a model name, or None when unknown."""
        profile = self._by_name.get(model_name)
        if profile is None:
            return None
        return dict(profile)

    def get_non_interactive_models(self) -> list[str]:
        """Return model names marked as non-interactive."""
        models: list[str] = []
        for profile in self._profiles:
            if bool(profile.get("non_interactive")) and isinstance(profile.get("name"), str):
                models.append(profile["name"])
        return models

    def get_best_model(self, task_type: str, cost_tier: str, context_size: int) -> str | None:
        """Return the best matching model name for task, budget, and context needs."""
        if not self._profiles:
            return None

        requested_cost_rank = self._COST_RANK.get(cost_tier, self._COST_RANK["high"])
        context_candidates = [
            profile
            for profile in self._profiles
            if int(profile.get("context_window", 0)) >= int(context_size)
        ]
        if not context_candidates:
            context_candidates = list(self._profiles)

        affordable_candidates = [
            profile
            for profile in context_candidates
            if self._COST_RANK.get(str(profile.get("cost_tier", "high")), self._COST_RANK["high"])
            <= requested_cost_rank
        ]
        candidates = affordable_candidates or context_candidates

        best = max(candidates, key=lambda profile: self._score_profile(profile, task_type))
        return str(best.get("name")) if best.get("name") else None

    def _load_profiles(self) -> list[dict[str, Any]]:
        if not self.path.exists():
            return []

        data = yaml.safe_load(self.path.read_text(encoding="utf-8")) or {}
        profiles = data.get("model_profiles") if isinstance(data, dict) else None
        if not isinstance(profiles, list):
            return []
        return [profile for profile in profiles if isinstance(profile, dict)]

    def _score_profile(self, profile: dict[str, Any], task_type: str) -> tuple[int, int, int]:
        strengths = profile.get("strengths") if isinstance(profile.get("strengths"), list) else []
        best_for = profile.get("best_for") if isinstance(profile.get("best_for"), list) else []

        normalized_task = task_type.lower().strip()
        task_match = int(any(normalized_task in str(item).lower() for item in strengths + best_for))

        speed = str(profile.get("speed", "slow"))
        speed_bonus = {"fast": 2, "medium": 1, "slow": 0}.get(speed, 0)

        context = int(profile.get("context_window", 0))
        return task_match, speed_bonus, context
