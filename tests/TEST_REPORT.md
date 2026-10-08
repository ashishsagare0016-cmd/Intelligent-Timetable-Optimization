# Stage 12 Test Suite & Validation Report

**Project Title:** Intelligent Timetable Optimization Using Graph Colouring, Backtracking and Constraint Analysis  
**Execution Date:** 2026-10-07  
**Test Runner:** `pytest 9.1.1`  
**Python Version:** `Python 3.11.9`

---

## 1. Test Suite Summary

| Metric | Value |
| :--- | :--- |
| **Total Test Files** | 7 files |
| **Total Test Cases** | **37 tests** |
| **Passed Tests** | **37 passed** |
| **Failed Tests** | **0 failed** |
| **Pass Rate** | **100%** |
| **Execution Time** | **2.05 seconds** |

---

## 2. Test Files Breakdown

| Test File | Description | Tests | Status |
| :--- | :--- | :---: | :---: |
| [`tests/test_coloring.py`](file:///c:/Users/ashis/OneDrive/Desktop/Intelligent-Timetable-Optimization/tests/test_coloring.py) | Graph Colouring with Degree-Based Ordering | 4 | **PASSED** |
| [`tests/test_backtracking.py`](file:///c:/Users/ashis/OneDrive/Desktop/Intelligent-Timetable-Optimization/tests/test_backtracking.py) | Recursive Backtracking Timetable Solver | 4 | **PASSED** |
| [`tests/test_constraints.py`](file:///c:/Users/ashis/OneDrive/Desktop/Intelligent-Timetable-Optimization/tests/test_constraints.py) | 7 Hard & 3 Soft Constraint Analysis Engine | 9 | **PASSED** |
| [`tests/test_optimizer.py`](file:///c:/Users/ashis/OneDrive/Desktop/Intelligent-Timetable-Optimization/tests/test_optimizer.py) | Hill-Climbing Local Search Optimizer | 4 | **PASSED** |
| [`tests/test_simulation.py`](file:///c:/Users/ashis/OneDrive/Desktop/Intelligent-Timetable-Optimization/tests/test_simulation.py) | What-If Simulation Engine & Immutability | 5 | **PASSED** |
| [`tests/test_comparison.py`](file:///c:/Users/ashis/OneDrive/Desktop/Intelligent-Timetable-Optimization/tests/test_comparison.py) | Algorithm Comparison Engine Metrics | 3 | **PASSED** |
| [`tests/test_api_and_edge_cases.py`](file:///c:/Users/ashis/OneDrive/Desktop/Intelligent-Timetable-Optimization/tests/test_api_and_edge_cases.py) | Flask API Endpoints & Data Edge Cases | 8 | **PASSED** |

---

## 3. Important Edge Cases Verified

1. **Timetable Copy Immutability (`test_original_timetable_not_modified`)**:
   - Verified that `simulate_move()` executes on a deep copy and leaves the baseline timetable 100% identical to its pre-simulation state.
2. **Impossible Schedule Detection (`test_deliberately_impossible_dataset`)**:
   - Verified that when 3 mutually conflicting classes are scheduled with only 2 available slots, the backtracking solver returns `success=False` gracefully without hanging or throwing exceptions.
3. **Empty & Single-Class Datasets (`test_empty_dataset_edge_case`, `test_single_class_edge_case`)**:
   - Verified zero crash on 0 subjects and clean slot assignment for 1 subject.
4. **Availability Mappings (`check_teacher_availability`, `check_room_availability`)**:
   - Verified support for both `unavailable_slots` lists (`["Monday P1"]`) and explicit `availability` dictionaries without false violation flags.
5. **API Error Handling (`test_api_explain_valid_and_invalid`, `test_api_simulate_post_valid_and_invalid`)**:
   - Verified HTTP `404 Not Found` for invalid subjects and HTTP `400 Bad Request` for invalid slot formats without exposing raw Python tracebacks to users.

---

## 4. Final Test Command

To execute the complete test suite:

```bash
.\venv\Scripts\python.exe -m pytest -v
```
