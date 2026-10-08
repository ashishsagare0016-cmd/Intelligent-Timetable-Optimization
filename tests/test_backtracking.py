"""
Unit Tests for Backtracking Timetable Solver (Stage 5)
"""
import pytest
import networkx as nx
from algorithms.conflict_graph import build_conflict_graph
from algorithms.backtracking import solve_timetable_backtracking, BacktrackingTimetableSolver


@pytest.fixture
def sample_dataset():
    return {
        "division": "TY-C",
        "days": ["Monday", "Tuesday"],
        "periods": ["P1", "P2"],
        "subjects": [
            {"id": "OS", "name": "Operating Systems", "type": "Theory"},
            {"id": "DBMS", "name": "Database Systems", "type": "Theory"}
        ],
        "teachers": [
            {"name": "Prof. Joshi", "subjects": ["Operating Systems"]},
            {"name": "Prof. Patil", "subjects": ["Database Systems"]}
        ]
    }


def test_simple_feasible_timetable(sample_dataset):
    """Test backtracking solver on a simple feasible dataset."""
    G = build_conflict_graph(sample_dataset)
    result = solve_timetable_backtracking(G, days=sample_dataset["days"], periods=sample_dataset["periods"])

    assert result["success"] is True
    assert result["classes_assigned"] == 2
    assert len(result["timetable_entries"]) == 2


def test_conflicting_classes_no_shared_slot():
    """Test that conflicting classes are assigned distinct time slots."""
    G = nx.Graph()
    G.add_node("C1", subject="Class 1", teacher="Prof. A", division="TY-C", room="Room 101")
    G.add_node("C2", subject="Class 2", teacher="Prof. A", division="TY-C", room="Room 102")
    G.add_edge("C1", "C2", reasons=["Same Teacher"])

    result = solve_timetable_backtracking(G, days=["Monday"], periods=["P1", "P2"])
    assignments = result["assignments"]

    assert assignments["C1"] != assignments["C2"], "Conflicting classes must not share the same slot"


def test_backtracking_metrics_structure(sample_dataset):
    """Test that solver metrics are non-negative and properly structured."""
    G = build_conflict_graph(sample_dataset)
    result = solve_timetable_backtracking(G, days=sample_dataset["days"], periods=sample_dataset["periods"])

    assert "execution_time" in result and result["execution_time"] >= 0
    assert "backtrack_count" in result and result["backtrack_count"] >= 0
    assert "recursive_calls" in result and result["recursive_calls"] > 0
    assert "assignments_attempted" in result and result["assignments_attempted"] >= 0


def test_deliberately_impossible_dataset():
    """
    Test an impossible dataset: 3 classes with 1 teacher, but only 2 available slots in total.
    Should report failure gracefully without crashing or entering infinite loops.
    """
    G = nx.Graph()
    G.add_node("C1", subject="Class 1", teacher="Prof. Busy", division="TY-C", room="Room 1")
    G.add_node("C2", subject="Class 2", teacher="Prof. Busy", division="TY-C", room="Room 2")
    G.add_node("C3", subject="Class 3", teacher="Prof. Busy", division="TY-C", room="Room 3")

    # Complete graph conflict among C1, C2, C3
    G.add_edge("C1", "C2", reasons=["Same Teacher"])
    G.add_edge("C2", "C3", reasons=["Same Teacher"])
    G.add_edge("C1", "C3", reasons=["Same Teacher"])

    # Only 2 time slots available!
    result = solve_timetable_backtracking(G, days=["Monday"], periods=["P1", "P2"])

    assert result["success"] is False, "Solver must report failure when no feasible assignment exists"
    assert result["classes_assigned"] < 3
    assert result["backtrack_count"] >= 0
