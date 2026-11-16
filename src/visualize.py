"""Render dependency graphs using Mermaid."""

import base64
import json
import webbrowser
from html import escape


def to_mermaid(graph):
    """Convert a dependency graph to Mermaid syntax."""
    names = list(dict.fromkeys(
        [*graph, *(dep for deps in graph.values() for dep in deps)]
    ))
    identifiers = {name: f"n{index}" for index, name in enumerate(names)}
    lines = ["flowchart TD"]

    for name in names:
        label = escape(name, quote=True)
        lines.append(f'    {identifiers[name]}["{label}"]')

    for name, dependencies in graph.items():
        for dependency in dependencies:
            lines.append(
                f"    {identifiers[name]} --> {identifiers[dependency]}"
            )

    return "\n".join(lines)


def show_mermaid(graph):
    """Open the dependency diagram in a web browser."""
    diagram = to_mermaid(graph)
    print("\nMermaid diagram:")
    print(diagram)

    payload = json.dumps({"code": diagram}).encode("utf-8")
    encoded = base64.urlsafe_b64encode(payload).decode("ascii")
    url = f"https://mermaid.ink/svg/base64:{encoded}"
    webbrowser.open(url)
