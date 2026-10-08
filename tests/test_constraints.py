"""
Unit Tests for Constraint Analysis Engine (Stage 6)
"""
import pytest
from algorithms.constraints import analyze_timetable


@pytest.fixture
def raw_data_specs():
    return {
        "division": "TY-C",
        "student_count": 60,
        "days": ["Monday", "Tuesday", "Wednesday"],
        "periods": ["P1", "P2", "P3", "P4", "P5", "P6"],
        "subjects": [
            {"id": "OS", "name": "Operating Systems", "type": "Theory", "requires_lab": False},
            {"id": "ML", "name": "Machine Learning", "type": "Practical", "requires_lab": True}
        ],
        "teachers": [
            {"name": "Prof. Joshi", "subjects": ["Operating Systems"], "unavailable_slots": ["Monday P1"]}
        ],
        "rooms": [
            {"name": "Room 101", "type": "Theory", "capacity": 70, "unavailable_slots": ["Monday P2"]},
            {"name": "Room Small", "type": "Theory", "capacity": 30},
            {"name": "Lab 1", "type": "Laboratory", "capacity": 60}
        ]
    }


def test_teacher_conflict_detected(raw_data_specs):
    """Test Hard Constraint 1: Teacher Conflict."""
    entries = [
        {"subject": "Operating Systems", "teacher": "Prof. Joshi", "division": "TY-C", "room": "Room 101", "day": "Monday", "period": "P3"},
        {"subject": "Database Systems", "teacher": "Prof. Joshi", "division": "TY-D", "room": "Room 102", "day": "Monday", "period": "P3"}
    ]
    analysis = analyze_timetable(entries, raw_data_specs)
    assert analysis["hard_violation_count"] >= 1
    assert any(v["constraint_name"] == "Teacher Conflict" for v in analysis["hard_violations"])
    assert analysis["is_feasible"] is False


def test_division_conflict_detected(raw_data_specs):
    """Test Hard Constraint 2: Division Conflict."""
    entries = [
        {"subject": "Operating Systems", "teacher": "Prof. Joshi", "division": "TY-C", "room": "Room 101", "day": "Monday", "period": "P3"},
        {"subject": "Computer Networks", "teacher": "Prof. Kulkarni", "division": "TY-C", "room": "Room 102", "day": "Monday", "period": "P3"}
    ]
    analysis = analyze_timetable(entries, raw_data_specs)
    assert analysis["hard_violation_count"] >= 1
    assert any(v["constraint_name"] == "Division Conflict" for v in analysis["hard_violations"])
    assert analysis["is_feasible"] is False


def test_room_conflict_detected(raw_data_specs):
    """Test Hard Constraint 3: Room Conflict."""
    entries = [
        {"subject": "Operating Systems", "teacher": "Prof. Joshi", "division": "TY-C", "room": "Room 101", "day": "Monday", "period": "P3"},
        {"subject": "Mathematics", "teacher": "Prof. More", "division": "TY-D", "room": "Room 101", "day": "Monday", "period": "P3"}
    ]
    analysis = analyze_timetable(entries, raw_data_specs)
    assert any(v["constraint_name"] == "Room Conflict" for v in analysis["hard_violations"])
    assert analysis["is_feasible"] is False


def test_teacher_unavailability_detected(raw_data_specs):
    """Test Hard Constraint 4: Teacher Unavailability (Prof. Joshi unavailable on Monday P1)."""
    entries = [
        {"subject": "Operating Systems", "teacher": "Prof. Joshi", "division": "TY-C", "room": "Room 101", "day": "Monday", "period": "P1"}
    ]
    analysis = analyze_timetable(entries, raw_data_specs)
    assert any(v["constraint_name"] == "Teacher Availability" for v in analysis["hard_violations"])


def test_room_unavailability_detected(raw_data_specs):
    """Test Hard Constraint 5: Room Unavailability (Room 101 unavailable on Monday P2)."""
    entries = [
        {"subject": "Operating Systems", "teacher": "Prof. Joshi", "division": "TY-C", "room": "Room 101", "day": "Monday", "period": "P2"}
    ]
    analysis = analyze_timetable(entries, raw_data_specs)
    assert any(v["constraint_name"] == "Room Availability" for v in analysis["hard_violations"])


def test_insufficient_room_capacity(raw_data_specs):
    """Test Hard Constraint 6: Insufficient Room Capacity (Room Small cap=30 vs student_count=60)."""
    entries = [
        {"subject": "Operating Systems", "teacher": "Prof. Joshi", "division": "TY-C", "room": "Room Small", "day": "Monday", "period": "P3"}
    ]
    analysis = analyze_timetable(entries, raw_data_specs)
    assert any(v["constraint_name"] == "Room Capacity" for v in analysis["hard_violations"])


def test_lab_requirement_mismatch(raw_data_specs):
    """Test Hard Constraint 7: Practical class assigned to non-lab room."""
    entries = [
        {"subject": "Machine Learning", "teacher": "Prof. Deshmukh", "division": "TY-C", "room": "Room 101", "day": "Monday", "period": "P3"}
    ]
    analysis = analyze_timetable(entries, raw_data_specs)
    assert any(v["constraint_name"] == "Lab Requirement" for v in analysis["hard_violations"])


def test_consecutive_lectures_soft_constraint(raw_data_specs):
    """Test Soft Constraint: Too Many Consecutive Lectures (P1, P2, P3 scheduled continuously)."""
    entries = [
        {"subject": "S1", "teacher": "T1", "division": "TY-C", "room": "R1", "day": "Monday", "period": "P1"},
        {"subject": "S2", "teacher": "T2", "division": "TY-C", "room": "R2", "day": "Monday", "period": "P2"},
        {"subject": "S3", "teacher": "T3", "division": "TY-C", "room": "R3", "day": "Monday", "period": "P3"}
    ]
    analysis = analyze_timetable(entries, raw_data_specs)
    assert any(v["constraint_name"] == "Too Many Consecutive Lectures" for v in analysis["soft_violations"])


def test_is_feasible_logic(raw_data_specs):
    """Verify is_feasible is True ONLY when zero hard violations exist."""
    valid_entries = [
        {"subject": "Operating Systems", "teacher": "Prof. Joshi", "division": "TY-C", "room": "Room 101", "day": "Monday", "period": "P3"}
    ]
    analysis = analyze_timetable(valid_entries, raw_data_specs)
    assert analysis["hard_violation_count"] == 0
    assert analysis["is_feasible"] is True
