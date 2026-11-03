from collections import deque
from src import fetcher
from src import parser

START_DEPTH = 0
DEPTH_INCREMENT = 1


def _fetch_dependencies(
        package: str,
        repo_url: str,
        test_mode: bool,
        test_data: dict[str, list[str]]
) -> list[str]:
    if test_mode:
        return test_data.get(package, [])

    try:
        return fetcher.get_direct_dependencies(repo_url, package)
    except ValueError:
        return []


def build_dependency_graph(
        root_package: str,
        repo_url: str,
        max_depth: int,
        test_mode: bool,
        test_filepath: str
) -> dict[str, list[str]]:
    graph = {}
    visited = set()

    queue = deque([(root_package, START_DEPTH)])

    test_data = {}
    if test_mode:
        test_data = parser.parse_test_repository(test_filepath)

    while queue:
        current_pkg, current_depth = queue.popleft()

        if current_pkg in visited:
            continue

        visited.add(current_pkg)
        graph[current_pkg] = []

        if current_depth >= max_depth:
            continue

        deps = _fetch_dependencies(
            current_pkg, repo_url, test_mode, test_data
        )
        graph[current_pkg] = deps

        for dep in deps:
            if dep not in visited:
                new_depth = current_depth + DEPTH_INCREMENT
                queue.append((dep, new_depth))

    return graph


def get_installation_order(graph: dict[str, list[str]]) -> list[str]:
    visited = set()
    order = []

    for start_node in graph:
        if start_node in visited:
            continue

        stack = [(start_node, False)]

        while stack:
            node, is_processed = stack.pop()

            if is_processed:
                order.append(node)
                continue

            if node in visited:
                continue

            visited.add(node)
            stack.append((node, True))

            for dep in graph.get(node, []):
                if dep not in visited:
                    stack.append((dep, False))

    return order