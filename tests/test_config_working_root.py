import json
from pathlib import Path

from config import load_config
from scripts.ops import config_show


def test_working_root_comes_from_env(monkeypatch, tmp_path):
    monkeypatch.setenv("ABRACAPOCUS_WORKING_ROOT", str(tmp_path))

    config = load_config()

    assert config.paths.working_root == tmp_path


def test_working_root_defaults_to_cwd(monkeypatch):
    monkeypatch.delenv("ABRACAPOCUS_WORKING_ROOT", raising=False)

    config = load_config()

    assert config.paths.working_root == Path.cwd()


def test_config_show_includes_working_root(monkeypatch, tmp_path, capsys):
    monkeypatch.setenv("ABRACAPOCUS_WORKING_ROOT", str(tmp_path))

    config_show()
    payload = json.loads(capsys.readouterr().out)

    assert payload["working_root"] == str(tmp_path)


def test_retry_defaults_applied_when_env_unset(monkeypatch):
    monkeypatch.delenv("RETRY_TIER_1", raising=False)
    monkeypatch.delenv("RETRY_TIER_2", raising=False)
    monkeypatch.delenv("RETRY_TIER_3", raising=False)
    monkeypatch.delenv("RETRY_DELAY_SECONDS", raising=False)

    config = load_config()

    assert config.retry.max_retries_tier_1 == 2
    assert config.retry.max_retries_tier_2 == 1
    assert config.retry.max_retries_tier_3 == 1
    assert config.retry.retry_delay_seconds == 2


def test_retry_tier_one_zero_disables_tier_one_retries(monkeypatch):
    monkeypatch.setenv("RETRY_TIER_1", "0")

    config = load_config()

    assert config.retry.max_retries_tier_1 == 0


def test_config_show_includes_retry_settings(monkeypatch, capsys):
    monkeypatch.setenv("RETRY_TIER_1", "0")
    monkeypatch.setenv("RETRY_TIER_2", "4")
    monkeypatch.setenv("RETRY_TIER_3", "2")
    monkeypatch.setenv("RETRY_DELAY_SECONDS", "7")

    config_show()
    payload = json.loads(capsys.readouterr().out)

    assert payload["retry"]["max_retries_tier_1"] == 0
    assert payload["retry"]["max_retries_tier_2"] == 4
    assert payload["retry"]["max_retries_tier_3"] == 2
    assert payload["retry"]["retry_delay_seconds"] == 7
