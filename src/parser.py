def parse_test_repository(filepath: str) -> dict[str, list[str]]:
    """
    Parses a local text file representing a dependency graph.
    Format: 'PACKAGE: DEP1 DEP2'
    """
    graph = {}
    try:
        with open(filepath, "r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue

                if ":" not in line:
                    continue

                package, deps_str = line.split(":", 1)
                package = package.strip()
                dependencies = deps_str.split()

                if package:
                    graph[package] = dependencies
    except FileNotFoundError as error:
        raise ValueError(
            f"Test repository file not found: {filepath}"
        ) from error

    return graph