"""
Unit Tests for Greedy Graph Colouring (Stage 4)
"""
import pytest
import networkx as nx
from algorithms.conflict_graph import build_conflict_graph
from algorithms.graph_coloring import greedy_graph_coloring


@pytest.fixture
def sample_raw_data():
    return {
        "division": "TY-C",
        "days": ["Monday", "Tuesday"],
        "periods": ["P1", "P2", "P3"],
        "subjects": [
            {"id": "S1", "name": "Subject 1", "type": "Theory", "requires_lab": False},
            {"id": "S2", "name": "Subject 2", "type": "Theory", "requires_lab": False},
            {"id": "S3", "name": "Subject 3", "type": "Theory", "requires_lab": False}
        ],
        "teachers": [
            {"name": "Teacher A", "subjects": ["Subject 1"]},
            {"name": "Teacher B", "subjects": ["Subject 2"]},
            {"name": "Teacher C", "subjects": ["Subject 3"]}
        ]
    }


def test_no_edges_graph(sample_raw_data):
    """Test graph with no resource conflicts (independent subjects, different divisions)."""
    # Make divisions different so no division conflict exists
    sample_raw_data["subjects"][0]["division"] = "Div-A"
    sample_raw_data["subjects"][1]["division"] = "Div-B"
    sample_raw_data["subjects"][2]["division"] = "Div-C"

    # Manually build isolated graph
    G = nx.Graph()
    G.add_node("S1", subject="Subject 1", teacher="Teacher A", division="Div-A", room="Room 101")
    G.add_node("S2", subject="Subject 2", teacher="Teacher B", division="Div-B", room="Room 102")

    result = greedy_graph_coloring(G, days=["Monday"], periods=["P1", "P2"])
    assert result["colors_used"] >= 1
    assert result["total_classes"] == 2
    assert len(result["timetable_entries"]) == 2


def test_single_conflict_edge():
    """Test graph with one conflict edge (Same Teacher)."""
    G = nx.Graph()
    G.add_node("S1", subject="Subject 1", teacher="Teacher A", division="TY-C", room="Room 101")
    G.add_node("S2", subject="Subject 2", teacher="Teacher A", division="TY-C", room="Room 102")
    G.add_edge("S1", "S2", reasons=["Same Teacher"])

    result = greedy_graph_coloring(G, days=["Monday"], periods=["P1", "P2"])
    assignments = result["color_assignments"]

    assert assignments["S1"] != assignments["S2"], "Conflicting nodes must be assigned different slots"


def test_connected_nodes_different_colors(sample_raw_data):
    """Test that all connected nodes in conflict graph receive distinct time slots."""
    G = build_conflict_graph(sample_raw_data)
    result = greedy_graph_coloring(G, days=sample_raw_data["days"], periods=sample_raw_data["periods"])
    assignments = result["color_assignments"]

    for u, v in G.edges():
        assert assignments[u] != assignments[v], f"Conflict edge between {u} and {v} violated color assignment"


def test_every_class_receives_valid_slot(sample_raw_data):
    """Test that every class node receives a valid formatted slot (Day Period)."""
    G = build_conflict_graph(sample_raw_data)
    result = greedy_graph_coloring(G, days=sample_raw_data["days"], periods=sample_raw_data["periods"])

    assert result["total_classes"] == len(sample_raw_data["subjects"])
    for entry in result["timetable_entries"]:
        assert "day" in entry and entry["day"] in sample_raw_data["days"]
        assert "period" in entry and entry["period"] in sample_raw_data["periods"]
