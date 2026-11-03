MAX_SPLIT_COUNT = 1


def parse_test_repository(filepath: str) -> dict[str, list[str]]:
    graph = {}
    try:
        with open(filepath, "r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue

                if ":" not in line:
                    continue

                package, deps_str = line.split(":", MAX_SPLIT_COUNT)
                package = package.strip()
                dependencies = deps_str.split()

                if package:
                    graph[package] = dependencies
    except FileNotFoundError as error:
        raise ValueError(
            f"Test repository file not found: {filepath}"
        ) from error

    return graph