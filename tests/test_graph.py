import pytest
from src.graph import build_dependency_graph, get_installation_order

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


def test_installation_order():
    graph_data = {
        "A": ["B", "C"],
        "B": ["D"],
        "C": ["D"],
        "D": []
    }

    order = get_installation_order(graph_data)

    assert order[0] == "D"
    assert order[-1] == "A"
    assert order.index("D") < order.index("B")
    assert order.index("D") < order.index("C")