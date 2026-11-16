"""Demonstrate three dependency graphs."""

from src.install_order import installation_order
from src.visualize import to_mermaid

examples = {
    "A": {"A": ["B", "C"], "B": ["D"], "C": ["D"], "D": []},
    "E": {"E": ["F"], "F": ["G"], "G": []},
    "H": {"H": ["I", "J"], "I": [], "J": []},
}

for package, graph in examples.items():
    print()
    print(f"=== Package {package} ===")
    print("Installation order:")
    print(" -> ".join(installation_order(graph, package)))
    print("Mermaid diagram:")
    print(to_mermaid(graph))
