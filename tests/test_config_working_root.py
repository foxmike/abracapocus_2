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

