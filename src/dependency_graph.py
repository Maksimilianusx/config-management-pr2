"""Build dependency graphs using breadth-first search."""

from collections import deque


def build_graph(start_package, get_dependencies, max_depth):
    """Build a dependency graph using iterative BFS."""
    if not isinstance(start_package, str) or not start_package:
        raise ValueError("Invalid starting package")

    if type(max_depth) is not int or max_depth < 0:
        raise ValueError("Invalid maximum depth")

    graph = {start_package: []}
    visited = {start_package}
    queue = deque([(start_package, 0)])

    while queue:
        package, depth = queue.popleft()

        if depth >= max_depth:
            continue

        dependencies = list(dict.fromkeys(
            get_dependencies(package)
        ))

        graph[package] = dependencies

        for dependency in dependencies:
            graph.setdefault(dependency, [])

            if dependency not in visited:
                visited.add(dependency)
                queue.append((dependency, depth + 1))

    return graph
