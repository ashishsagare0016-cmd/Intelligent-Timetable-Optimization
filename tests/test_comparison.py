"""
Unit Tests for Algorithm Comparison Engine (Stage 8)
"""
import pytest
import os
import json
from algorithms.comparison import run_algorithm_comparison


@pytest.fixture
def sample_dataset():
    data_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'sample_data.json')
    with open(data_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def test_comparison_contains_all_algorithms(sample_dataset):
    """Test comparison output includes Greedy, Backtracking, and Optimized algorithms."""
    res = run_algorithm_comparison(sample_dataset)

    assert "greedy" in res
    assert "backtracking" in res
    assert "optimized" in res
    assert "algorithms" in res and len(res["algorithms"]) == 3
    assert "best_algorithm" in res


def test_algorithm_metrics_presence_and_non_negativity(sample_dataset):
    """Test all algorithms return execution_time, quality_score, and non-negative violations."""
    res = run_algorithm_comparison(sample_dataset)

    for algo_key in ["greedy", "backtracking", "optimized"]:
        data = res[algo_key]
        assert "execution_time" in data and data["execution_time"] >= 0
        assert "quality_score" in data and 0 <= data["quality_score"] <= 100
        assert "hard_violations" in data and data["hard_violations"] >= 0
        assert "soft_violations" in data and data["soft_violations"] >= 0
        assert "total_violations" in data and data["total_violations"] >= 0


def test_best_algorithm_selection(sample_dataset):
    """Test best algorithm is dynamically identified based on quality score and violations."""
    res = run_algorithm_comparison(sample_dataset)
    best_name = res["best_algorithm"]
    algo_names = [a["name"] for a in res["algorithms"]]

    assert best_name in algo_names
    assert len(res["observations"]) >= 3
