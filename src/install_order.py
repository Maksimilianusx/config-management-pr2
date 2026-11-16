"""Determine dependency installation order."""


def installation_order(graph, package):
    """List dependencies before the packages requiring them."""
    states = {}
    result = []
    stack = [(package, False)]

    while stack:
        name, completed = stack.pop()

        if completed:
            states[name] = 2
            result.append(name)
            continue

        state = states.get(name, 0)
        if state == 2:
            continue
        if state == 1:
            raise ValueError(f"Cyclic dependency involving {name}")

        states[name] = 1
        stack.append((name, True))

        for dependency in reversed(graph.get(name, [])):
            if states.get(dependency) == 1:
                raise ValueError(
                    f"Cyclic dependency involving {dependency}"
                )
            if states.get(dependency) != 2:
                stack.append((dependency, False))

    return result
