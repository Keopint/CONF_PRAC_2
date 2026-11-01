import pytest
from src.graph import build_dependency_graph

TEST_FILE = "test_repo.txt"


def test_bfs_graph_cycle_and_depth():
    graph = build_dependency_graph(
        root_package="A",
        repo_url=TEST_FILE,
        max_depth=2,
        test_mode=True,
        test_filepath=TEST_FILE
    )

    assert "A" in graph
    assert "B" in graph
    assert "D" in graph

    assert "E" in graph
    assert graph["E"] == []
    assert graph["A"] == ["B", "C"]
    assert graph["B"] == ["D"]