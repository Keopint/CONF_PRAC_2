import pytest
from src.main import parse_arguments


def test_parse_arguments_success(monkeypatch):
    """Tests successful parsing of arguments."""
    test_args = [
        "main.py",
        "--package", "requests",
        "--repo", "https://pypi.org",
        "--max-depth", "3"
    ]
    monkeypatch.setattr("sys.argv", test_args)
    args = parse_arguments()

    assert args.package == "requests"
    assert args.max_depth == 3