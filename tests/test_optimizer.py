"""
Unit Tests for Local Search Timetable Optimizer (Stage 7)
"""
import pytest
import os
import json
from algorithms.conflict_graph import build_conflict_graph
from algorithms.backtracking import solve_timetable_backtracking
from algorithms.optimizer import optimize_timetable, calculate_quality_score
from algorithms.constraints import analyze_timetable


@pytest.fixture
def sample_dataset():
    data_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'sample_data.json')
    with open(data_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def test_optimizer_accepts_valid_starting_timetable(sample_dataset):
    """Test optimizer accepts backtracking initial timetable and executes."""
    G = build_conflict_graph(sample_dataset)
    bt_res = solve_timetable_backtracking(G, days=sample_dataset.get('days'), periods=sample_dataset.get('periods'))
    opt_res = optimize_timetable(bt_res['timetable_entries'], sample_dataset)

    assert "optimized_timetable" in opt_res
    assert len(opt_res["optimized_timetable"]) == len(bt_res["timetable_entries"])


def test_optimizer_does_not_introduce_hard_violations(sample_dataset):
    """Test local search optimizer never introduces new hard violations."""
    G = build_conflict_graph(sample_dataset)
    bt_res = solve_timetable_backtracking(G, days=sample_dataset.get('days'), periods=sample_dataset.get('periods'))
    initial_analysis = analyze_timetable(bt_res['timetable_entries'], sample_dataset)
    
    opt_res = optimize_timetable(bt_res['timetable_entries'], sample_dataset)
    final_analysis = analyze_timetable(opt_res['optimized_timetable'], sample_dataset)

    assert final_analysis["hard_violation_count"] <= initial_analysis["hard_violation_count"]


def test_optimizer_score_range_and_metrics(sample_dataset):
    """Test score is 0..100 and iteration/candidate metrics are non-negative."""
    G = build_conflict_graph(sample_dataset)
    bt_res = solve_timetable_backtracking(G, days=sample_dataset.get('days'), periods=sample_dataset.get('periods'))
    opt_res = optimize_timetable(bt_res['timetable_entries'], sample_dataset)

    metrics = opt_res["metrics"]
    final_score = opt_res["final_score"]["score"]
    initial_score = opt_res["initial_score"]["score"]
    assert 0 <= final_score <= 100
    assert metrics["iterations"] >= 0
    assert metrics["candidate_moves"] >= 0
    assert metrics["accepted_moves"] >= 0
    assert opt_res["score_improvement"] == final_score - initial_score



def test_optimizer_no_improvement_case():
    """Test optimizer handles case where starting timetable is already optimal."""
    dataset = {
        "division": "TY-C",
        "days": ["Monday"],
        "periods": ["P1"],
        "subjects": [{"id": "S1", "name": "Subject 1", "type": "Theory"}],
        "teachers": [{"name": "T1", "subjects": ["Subject 1"]}],
        "rooms": [{"name": "R1", "type": "Theory", "capacity": 60}]
    }
    initial_timetable = [
        {"subject": "Subject 1", "teacher": "T1", "division": "TY-C", "room": "R1", "day": "Monday", "period": "P1"}
    ]
    opt_res = optimize_timetable(initial_timetable, dataset)
    assert opt_res["score_improvement"] >= 0
    assert len(opt_res["optimized_timetable"]) == 1
