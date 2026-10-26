"""Read package metadata from an Ubuntu APT repository."""

import gzip
from urllib.request import urlopen


def download_index(url):
    """Download and decompress a Packages.gz index."""
    try:
        with urlopen(url, timeout=30) as response:
            compressed = response.read()
    except (OSError, TimeoutError) as error:
        raise ValueError(
            f"Cannot download repository: {error}"
        ) from error

    try:
        return gzip.decompress(compressed).decode("utf-8")
    except (OSError, EOFError, UnicodeError) as error:
        raise ValueError(
            f"Invalid repository index: {error}"
        ) from error


def parse_record(text):
    """Parse one Debian package metadata record."""
    fields = {}
    last_key = None

    for line in text.splitlines():
        if line.startswith((" ", "\t")) and last_key:
            fields[last_key] += " " + line.strip()
        elif ":" in line:
            key, value = line.split(":", 1)
            fields[key] = value.strip()
            last_key = key

    return fields


def find_package(index_text, name, version):
    """Find a package matching the exact name and version."""
    for record_text in index_text.split("\n\n"):
        record = parse_record(record_text)

        if (
            record.get("Package") == name
            and record.get("Version") == version
        ):
            return record

    raise ValueError(
        f"Package {name} version {version} not found"
    )


def get_direct_dependencies(record):
    """Extract direct dependency expressions."""
    dependencies = []

    for field in ("Pre-Depends", "Depends"):
        value = record.get(field, "")

        for dependency in value.split(","):
            dependency = dependency.strip()
            if dependency:
                dependencies.append(dependency)

    return dependencies
