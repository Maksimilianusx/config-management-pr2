"""Resolve package dependencies from an APT index."""

import re

if __package__:
    from .apt_repository import (
        find_package,
        get_direct_dependencies,
        parse_record,
    )
else:
    from apt_repository import (
        find_package,
        get_direct_dependencies,
        parse_record,
    )


def index_packages(index_text):
    """Create a lookup table of available packages."""
    packages = {}

    for block in index_text.split("\n\n"):
        record = parse_record(block)
        name = record.get("Package")

        if name:
            packages.setdefault(name, record)

    return packages


def extract_name(expression):
    """Extract the package name from a dependency expression."""
    match = re.match(
        r"^\s*([a-zA-Z0-9][a-zA-Z0-9.+-]*)",
        expression,
    )
    return match.group(1) if match else None


def resolve_dependency(expression, packages):
    """Choose an available dependency alternative."""
    alternatives = expression.split("|")

    for alternative in alternatives:
        name = extract_name(alternative)

        if name in packages:
            return name

    return extract_name(alternatives[0])


def create_dependency_lookup(index_text, package, version):
    """Create a lookup function for BFS traversal."""
    packages = index_packages(index_text)
    root_record = find_package(index_text, package, version)

    def lookup(name):
        """Return direct dependencies of one package."""
        record = (
            root_record if name == package
            else packages.get(name)
        )

        if record is None:
            return []

        expressions = get_direct_dependencies(record)
        result = []

        for expression in expressions:
            dependency = resolve_dependency(
                expression, packages
            )

            if dependency:
                result.append(dependency)

        return result

    return lookup
