"""
Unit Tests for What-If Timetable Simulation (Stage 11)
"""
import pytest
import os
import json
import copy
from algorithms.conflict_graph import build_conflict_graph
from algorithms.backtracking import solve_timetable_backtracking
from algorithms.simulation import simulate_move


@pytest.fixture
def sample_dataset():
    data_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'sample_data.json')
    with open(data_path, 'r', encoding='utf-8') as f:
        return json.load(f)


@pytest.fixture
def baseline_timetable(sample_dataset):
    G = build_conflict_graph(sample_dataset)
    res = solve_timetable_backtracking(G, days=sample_dataset.get('days'), periods=sample_dataset.get('periods'))
    return res['timetable_entries']


def test_simulation_valid_subject_and_slot(baseline_timetable, sample_dataset):
    """Test valid subject and target slot simulation."""
    res, status_code = simulate_move("Operating Systems", "Monday P3", baseline_timetable, sample_dataset)
    assert status_code == 200
    assert res["subject"] == "Operating Systems"
    assert res["target_slot"] == "Monday P3"
    assert "before" in res and "after" in res
    assert "score_change" in res
    assert "recommendation" in res


def test_simulation_invalid_subject(baseline_timetable, sample_dataset):
    """Test invalid subject returns 404 error."""
    res, status_code = simulate_move("NonExistentSubject", "Monday P1", baseline_timetable, sample_dataset)
    assert status_code == 404
    assert "error" in res


def test_simulation_invalid_target_slot(baseline_timetable, sample_dataset):
    """Test invalid target slot format returns 400 error."""
    res, status_code = simulate_move("Operating Systems", "InvalidSlotFormat", baseline_timetable, sample_dataset)
    assert status_code == 400
    assert "error" in res


def test_simulation_hard_conflict_detection(baseline_timetable, sample_dataset):
    """Test simulation of a move that introduces a hard conflict (e.g. same teacher)."""
    # Find slot of another subject taught by same teacher or same division
    entry_dbms = next(e for e in baseline_timetable if e["subject"] == "Database Management Systems")
    target_slot = f"{entry_dbms['day']} {entry_dbms['period']}"

    # Move Operating Systems (TY-C) to same slot as DBMS (TY-C) -> Division Conflict!
    res, status_code = simulate_move("Operating Systems", target_slot, baseline_timetable, sample_dataset)
    assert status_code == 200
    assert res["after"]["hard_violations"] > res["before"]["hard_violations"] or res["recommendation_type"] == "not_recommended"


def test_original_timetable_not_modified(baseline_timetable, sample_dataset):
    """Critical Test: Verify original timetable is NOT modified by simulation."""
    original_copy = copy.deepcopy(baseline_timetable)
    
    # Perform simulation move
    res, status_code = simulate_move("Operating Systems", "Thursday P6", baseline_timetable, sample_dataset)
    assert status_code == 200

    # Verify baseline_timetable is strictly identical to original_copy
    assert baseline_timetable == original_copy, "Original timetable must remain unchanged after simulation"
