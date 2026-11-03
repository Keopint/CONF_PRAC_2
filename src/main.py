import argparse
import sys
from src import graph

MIN_DEPTH = 1
MAX_DEPTH_LIMIT = 100
ERROR_EXIT_CODE = 1
START_INDEX = 1
COMMANDS = ["--package", "--repo", "--test-mode",
                "--ascii-tree", "--install-order", "--max-depth"]

def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Dependency graph visualization tool."
    )
    parser.add_argument(
        COMMANDS[0], type=str, required=True,
        help="Name of the analyzed package."
    )
    parser.add_argument(
        COMMANDS[1], type=str, required=True,
        help="Repository URL or path to the test repository file."
    )
    parser.add_argument(
        COMMANDS[2], action="store_true",
        help="Mode of working with the test repository."
    )
    parser.add_argument(
        COMMANDS[3], action="store_true",
        help="Mode for outputting dependencies in ASCII-tree format."
    )
    parser.add_argument(
        COMMANDS[4], action="store_true",
        help="Show the order of dependency loading (installation)."
    )
    parser.add_argument(
        COMMANDS[5], type=int, required=True,
        help="Maximum depth of dependency analysis."
    )
    return parser.parse_args()


def validate_arguments(args: argparse.Namespace) -> None:
    """Validates the parsed arguments."""
    if not args.package.strip():
        raise ValueError("Package name cannot be empty.")

    if not args.repo.strip():
        raise ValueError("Repository URL or path cannot be empty.")

    if not MIN_DEPTH <= args.max_depth <= MAX_DEPTH_LIMIT:
        raise ValueError(
            f"Max depth must be between {MIN_DEPTH} and {MAX_DEPTH_LIMIT}."
        )


def print_configuration(args: argparse.Namespace) -> None:
    print("--- Current Configuration ---")
    print(f"package: {args.package}")
    print(f"repository: {args.repo}")
    print(f"test_mode: {args.test_mode}")
    print(f"ascii_tree: {args.ascii_tree}")
    print(f"install_order: {args.install_order}")
    print(f"max_depth: {args.max_depth}")
    print("-----------------------------")


def display_installation_order(order: list[str]) -> None:
    print("\n--- Installation Order (Bottom-Up) ---")
    for index, pkg in enumerate(order, start=START_INDEX):
        print(f"{index}. {pkg}")
    print("--------------------------------------")


def display_graph(dep_graph: dict[str, list[str]]) -> None:
    print("\n--- Dependency Graph ---")
    for pkg, deps in dep_graph.items():
        deps_str = ", ".join(deps) if deps else "None"
        print(f"{pkg} -> {deps_str}")


def process_output(args: argparse.Namespace,
                   dep_graph:
                   dict[str, list[str]]) -> None:
    if args.install_order:
        order = graph.get_installation_order(dep_graph)
        display_installation_order(order)
    else:
        display_graph(dep_graph)


def main() -> None:
    try:
        args = parse_arguments()
        validate_arguments(args)
        print_configuration(args)

        print("\nBuilding graph...")
        dep_graph = graph.build_dependency_graph(
            root_package=args.package,
            repo_url=args.repo,
            max_depth=args.max_depth,
            test_mode=args.test_mode,
            test_filepath=args.repo if args.test_mode else ""
        )

        process_output(args, dep_graph)

    except ValueError as error:
        print(f"Error: {error}", file=sys.stderr)
        sys.exit(ERROR_EXIT_CODE)


if __name__ == "__main__":
    main()