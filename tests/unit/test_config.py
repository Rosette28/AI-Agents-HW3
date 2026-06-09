import json

import pytest

from src.shared.config import ConfigError
from src.shared.config import load_config


def test_load_valid_config(tmp_path, monkeypatch):
    config_dir = tmp_path / "config"
    config_dir.mkdir()

    config_file = config_dir / "test.json"

    config_file.write_text(
        json.dumps(
            {
                "version": "1.00",
                "value": 123
            }
        )
    )

    monkeypatch.chdir(tmp_path)

    result = load_config("test.json")

    assert result["value"] == 123


def test_missing_file():
    with pytest.raises(ConfigError):
        load_config("does_not_exist.json")


def test_invalid_version(tmp_path, monkeypatch):
    config_dir = tmp_path / "config"
    config_dir.mkdir()

    config_file = config_dir / "bad.json"

    config_file.write_text(
        json.dumps(
            {
                "version": "2.00"
            }
        )
    )

    monkeypatch.chdir(tmp_path)

    with pytest.raises(ConfigError):
        load_config("bad.json")