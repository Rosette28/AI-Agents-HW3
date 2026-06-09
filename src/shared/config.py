"""Configuration management module."""
import json
import os
from pathlib import Path

VERSION = "1.00"

class ConfigError(Exception):
    """Custom exception for configuration errors."""


def load_config(file_name: str) -> dict:
    """Load and validate a JSON configuration file."""
    path = Path("config") / file_name
    if not path.exists():
        msg = f"Configuration file not found: {path}"
        raise ConfigError(msg)

    with path.open(encoding="utf-8") as file:
        data = json.load(file)

    if data.get("version") != VERSION:
        msg = f"Invalid version. Expected {VERSION}"
        raise ConfigError(msg)

    return data

def get_env_variable(name: str, default: str | None = None) -> str | None:
    """Safely retrieve an environment variable."""
    return os.environ.get(name, default)
