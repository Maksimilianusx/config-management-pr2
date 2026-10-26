"""Package dependency analyzer configuration."""

from pathlib import Path
from urllib.parse import urlparse

import yaml


def require_text(config, key):
    """Validate a required text parameter."""
    value = config.get(key)
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{key} must be a non-empty string")
    return value.strip()


def validate_config(config):
    """Validate all configuration parameters."""
    if not isinstance(config, dict):
        raise ValueError("Configuration must be a YAML mapping")

    required = {
        "package", "repository", "test_mode",
        "version", "max_depth"
    }

    missing = required - config.keys()
    if missing:
        raise ValueError(f"Missing parameters: {sorted(missing)}")

    unknown = config.keys() - required
    if unknown:
        raise ValueError(f"Unknown parameters: {sorted(unknown)}")

    for key in ("package", "repository", "version"):
        require_text(config, key)

    if type(config["test_mode"]) is not bool:
        raise ValueError("test_mode must be true or false")

    depth = config["max_depth"]
    if type(depth) is not int or depth < 0:
        raise ValueError("max_depth must be a non-negative integer")

    repository = config["repository"].strip()

    if config["test_mode"]:
        path = Path(repository)
        if not path.is_absolute():
            path = Path(__file__).resolve().parent.parent / path
        if not path.is_file():
            raise ValueError(f"Repository file not found: {path}")
    else:
        url = urlparse(repository)
        if url.scheme not in ("http", "https") or not url.netloc:
            raise ValueError("repository must be a valid HTTP(S) URL")

    return config


def load_config():
    """Read and validate the YAML configuration."""
    project_dir = Path(__file__).resolve().parent.parent
    config_path = project_dir / "config.yaml"

    with config_path.open("r", encoding="utf-8-sig") as file:
        config = yaml.safe_load(file)

    return validate_config(config)


def main():
    """Display validated configuration parameters."""
    try:
        config = load_config()
        print("Package dependency analyzer")
        print("---------------------------")

        for key, value in config.items():
            print(f"{key}: {value}")

    except (OSError, ValueError, yaml.YAMLError) as error:
        print(f"Configuration error: {error}")
        raise SystemExit(1) from error


if __name__ == "__main__":
    main()
