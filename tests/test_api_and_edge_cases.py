"""
Unit Tests for Flask API Endpoints and Edge Cases (Stage 12)
"""
import pytest
import json
from app import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_api_dashboard_endpoint(client):
    """Test GET /api/dashboard returns 200 OK and valid JSON structure."""
    res = client.get('/api/dashboard')
    assert res.status_code == 200
    data = res.get_json()
    assert "summary" in data
    assert "quality" in data
    assert "graph" in data
    assert "timetable" in data
    assert "key_results" in data


def test_api_constraints_endpoint(client):
    """Test GET /api/constraints returns 200 OK."""
    res = client.get('/api/constraints')
    assert res.status_code == 200
    data = res.get_json()
    assert "hard_violations" in data
    assert "soft_violations" in data


def test_api_optimization_endpoint(client):
    """Test GET /api/optimization returns 200 OK."""
    res = client.get('/api/optimization')
    assert res.status_code == 200
    data = res.get_json()
    assert "optimized_timetable" in data
    assert "final_score" in data


def test_api_comparison_endpoint(client):
    """Test GET /api/comparison returns 200 OK."""
    res = client.get('/api/comparison')
    assert res.status_code == 200
    data = res.get_json()
    assert "greedy" in data
    assert "backtracking" in data
    assert "optimized" in data


def test_api_explain_valid_and_invalid(client):
    """Test GET /api/explain/<subject> with valid and invalid subjects."""
    res_valid = client.get('/api/explain/Operating%20Systems')
    assert res_valid.status_code == 200
    assert "assigned_slot" in res_valid.get_json()

    res_invalid = client.get('/api/explain/NonExistentSubject')
    assert res_invalid.status_code == 404
    assert "error" in res_invalid.get_json()


def test_api_simulate_post_valid_and_invalid(client):
    """Test POST /api/simulate with valid, invalid subject, and malformed inputs."""
    # Valid simulation
    res_valid = client.post(
        '/api/simulate',
        data=json.dumps({"subject": "Operating Systems", "target_slot": "Monday P3"}),
        content_type='application/json'
    )
    assert res_valid.status_code == 200
    assert "score_change" in res_valid.get_json()

    # Invalid subject -> 404
    res_invalid_sub = client.post(
        '/api/simulate',
        data=json.dumps({"subject": "FakeSubject", "target_slot": "Monday P1"}),
        content_type='application/json'
    )
    assert res_invalid_sub.status_code == 404
    assert "error" in res_invalid_sub.get_json()

    # Invalid slot format -> 400
    res_invalid_slot = client.post(
        '/api/simulate',
        data=json.dumps({"subject": "Operating Systems", "target_slot": "InvalidSlot"}),
        content_type='application/json'
    )
    assert res_invalid_slot.status_code == 400
    assert "error" in res_invalid_slot.get_json()


def test_empty_dataset_edge_case():
    """Edge Case A: Empty dataset does not crash conflict graph builder."""
    from algorithms.conflict_graph import build_conflict_graph
    empty_data = {"subjects": [], "teachers": [], "rooms": []}
    G = build_conflict_graph(empty_data)
    assert G.number_of_nodes() == 0
    assert G.number_of_edges() == 0


def test_single_class_edge_case():
    """Edge Case B: Single class dataset."""
    from algorithms.conflict_graph import build_conflict_graph
    from algorithms.graph_coloring import greedy_graph_coloring
    single_data = {
        "division": "TY-C",
        "days": ["Monday"],
        "periods": ["P1"],
        "subjects": [{"id": "S1", "name": "Solo Subject", "type": "Theory"}],
        "teachers": [{"name": "Prof. Solo", "subjects": ["Solo Subject"]}],
        "rooms": [{"name": "Room 101", "type": "Theory", "capacity": 60}]
    }
    G = build_conflict_graph(single_data)
    res = greedy_graph_coloring(G, days=["Monday"], periods=["P1"])
    assert res["total_classes"] == 1
    assert len(res["timetable_entries"]) == 1
