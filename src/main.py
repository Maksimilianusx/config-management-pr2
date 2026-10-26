"""Package dependency analyzer for Ubuntu APT."""

from pathlib import Path
from urllib.parse import urlparse

import yaml

if __package__:
    from .apt_repository import (
        download_index,
        find_package,
        get_direct_dependencies,
    )
else:
    from apt_repository import (
        download_index,
        find_package,
        get_direct_dependencies,
    )


PROJECT_DIR = Path(__file__).resolve().parent.parent


def require_text(config, key):
    """Validate a required text parameter."""
    value = config.get(key)
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{key} must be a non-empty string")
    return value.strip()


def validate_config(config):
    """Validate all YAML configuration parameters."""
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
            path = PROJECT_DIR / path
        if not path.is_file():
            raise ValueError(f"Repository file not found: {path}")
    else:
        url = urlparse(repository)
        if url.scheme not in ("http", "https") or not url.netloc:
            raise ValueError("repository must be a valid HTTP(S) URL")

    return config


def load_config():
    """Read and validate YAML configuration."""
    config_path = PROJECT_DIR / "config.yaml"

    with config_path.open("r", encoding="utf-8-sig") as file:
        config = yaml.safe_load(file)

    return validate_config(config)


def read_test_dependencies(repository, package):
    """Read direct dependencies from a test repository."""
    path = Path(repository)
    if not path.is_absolute():
        path = PROJECT_DIR / path

    for line in path.read_text(
        encoding="utf-8-sig"
    ).splitlines():
        name, separator, dependencies = line.partition(":")
        if separator and name.strip() == package:
            return dependencies.split()

    raise ValueError(f"Test package {package} not found")


def get_dependencies(config):
    """Get direct dependencies from the selected repository."""
    if config["test_mode"]:
        return read_test_dependencies(
            config["repository"],
            config["package"],
        )

    index_text = download_index(config["repository"])

    record = find_package(
        index_text,
        config["package"],
        config["version"],
    )

    return get_direct_dependencies(record)


def main():
    """Display configuration and direct dependencies."""
    try:
        config = load_config()

        print("Package dependency analyzer")
        print("---------------------------")

        for key, value in config.items():
            print(f"{key}: {value}")

        dependencies = get_dependencies(config)

        print("\nDirect dependencies:")

        if not dependencies:
            print("(none)")
        else:
            for dependency in dependencies:
                print(f"- {dependency}")

    except (OSError, ValueError, yaml.YAMLError) as error:
        print(f"Error: {error}")
        raise SystemExit(1) from error


if __name__ == "__main__":
    main()
