import argparse
import sys
from src import graph

MIN_DEPTH = 1
MAX_DEPTH_LIMIT = 100


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Dependency graph visualization tool."
    )
    parser.add_argument(
        "--package", type=str, required=True,
        help="Name of the analyzed package."
    )
    parser.add_argument(
        "--repo", type=str, required=True,
        help="Repository URL or path to the test repository file."
    )
    parser.add_argument(
        "--test-mode", action="store_true",
        help="Mode of working with the test repository."
    )
    parser.add_argument(
        "--ascii-tree", action="store_true",
        help="Mode for outputting dependencies in ASCII-tree format."
    )
    parser.add_argument(
        "--install-order", action="store_true",
        help="Show the order of dependency loading (installation)."
    )
    parser.add_argument(
        "--max-depth", type=int, required=True,
        help="Maximum depth of dependency analysis."
    )
    return parser.parse_args()


def validate_arguments(args: argparse.Namespace) -> None:
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
    for index, pkg in enumerate(order):
        print(f"{index + 1}. {pkg}")
    print("--------------------------------------")


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

        if args.install_order:
            order = graph.get_installation_order(dep_graph)
            display_installation_order(order)
        else:
            # Fallback for previous stage demo
            print("\nGraph built successfully. Use --install-order to see it.")
            for pkg, deps in dep_graph.items():
                deps_str = ", ".join(deps) if deps else "None"
                print(f"{pkg} -> {deps_str}")

    except ValueError as error:
        print(f"Error: {error}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()