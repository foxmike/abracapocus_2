from runtime.model_profile_store import ModelProfileStore


def test_get_best_model_returns_valid_name_for_coding_low_cost() -> None:
    store = ModelProfileStore()

    best = store.get_best_model("coding", "low", 8000)

    assert isinstance(best, str)
    assert best
    assert store.get_profile(best) is not None


def test_get_profile_returns_all_expected_fields_for_known_model() -> None:
    store = ModelProfileStore()

    profile = store.get_profile("openrouter/qwen/qwen3-coder-next")

    assert profile is not None
    expected_fields = {
        "name",
        "provider",
        "strengths",
        "weaknesses",
        "context_window",
        "speed",
        "cost_tier",
        "non_interactive",
        "best_for",
    }
    assert expected_fields.issubset(profile.keys())


def test_unknown_model_returns_none() -> None:
    store = ModelProfileStore()

    assert store.get_profile("not-a-real-model") is None


def test_get_non_interactive_models_returns_names() -> None:
    store = ModelProfileStore()

    models = store.get_non_interactive_models()

    assert models
    assert "codex" in models
