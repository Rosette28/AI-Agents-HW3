import json
import os
from pathlib import Path


__version__ = "1.00"


class ConfigError(Exception):
    pass


def load_config(file_name: str) -> dict:
    path = Path("config") / file_name

    if not path.exists():
        raise ConfigError(f"Configuration file not found: {path}")

    with open(path, "r", encoding="utf-8") as file:
        data = json.load(file)

    if data.get("version") != VERSION:
        raise ConfigError(
            f"Invalid version. Expected {VERSION}"
        )

    return data


def get_env_variable(name: str, default=None):
    return os.environ.get(name, default)