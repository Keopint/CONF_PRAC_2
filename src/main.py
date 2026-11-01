import argparse
import sys
from src import fetcher

MIN_DEPTH = 1
MAX_DEPTH_LIMIT = 100


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Dependency graph visualization tool."
    )
    parser.add_argument(
        "--package",
        type=str,
        required=True,
        help="Name of the analyzed package."
    )
    parser.add_argument(
        "--repo",
        type=str,
        required=True,
        help="Repository URL or path to the test repository file."
    )
    parser.add_argument(
        "--test-mode",
        action="store_true",
        help="Mode of working with the test repository."
    )
    parser.add_argument(
        "--ascii-tree",
        action="store_true",
        help="Mode for outputting dependencies in ASCII-tree format."
    )
    parser.add_argument(
        "--max-depth",
        type=int,
        required=True,
        help="Maximum depth of dependency analysis."
    )
    return parser.parse_args()


def validate_arguments(args: argparse.Namespace) -> None:
    if not args.package.strip():
        raise ValueError("Package name cannot be empty.")

    if not args.repo.strip():
        raise ValueError("Repository URL or path cannot be empty.")

    if args.max_depth < MIN_DEPTH:
        raise ValueError(
            f"Max depth must be at least {MIN_DEPTH}."
        )
    if args.max_depth > MAX_DEPTH_LIMIT:
        raise ValueError(
            f"Max depth cannot exceed {MAX_DEPTH_LIMIT}."
        )


def print_configuration(args: argparse.Namespace) -> None:
    print("--- Current Configuration ---")
    print(f"package: {args.package}")
    print(f"repository: {args.repo}")
    print(f"test_mode: {args.test_mode}")
    print(f"ascii_tree: {args.ascii_tree}")
    print(f"max_depth: {args.max_depth}")
    print("-----------------------------")


def process_dependencies(args: argparse.Namespace) -> None:
    if args.test_mode:
        print("Test mode will be implemented in Stage 3.")
        return

    try:
        print(f"Fetching data for package: {args.package}...")
        deps = fetcher.get_direct_dependencies(args.repo, args.package)

        print(f"\nDirect dependencies for '{args.package}':")
        if not deps:
            print("  No direct dependencies found.")
        else:
            for dep in deps:
                print(f"  - {dep}")

    except ValueError as error:
        print(f"Data collection error: {error}", file=sys.stderr)
        sys.exit(1)


def main() -> None:
    try:
        args = parse_arguments()
        validate_arguments(args)
        print_configuration(args)
        process_dependencies(args)
    except ValueError as error:
        print(f"Configuration error: {error}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()