"""
Timetable Data Model
Defines classes for Subjects, Teachers, Rooms, Timetable Entries, and Dataset.
"""
from dataclasses import dataclass
from typing import List, Dict, Optional


@dataclass
class Subject:
    """Represents an academic subject/course."""
    id: str
    name: str
    class_type: str  # "Theory" or "Practical"
    requires_lab: bool
    weekly_sessions: int = 3

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            id=data.get('id', ''),
            name=data.get('name', ''),
            class_type=data.get('type', 'Theory'),
            requires_lab=data.get('requires_lab', False),
            weekly_sessions=data.get('weekly_sessions', 3)
        )


@dataclass
class Teacher:
    """Represents a faculty member teaching one or more subjects."""
    id: str
    name: str
    subjects: List[str]
    availability: Dict[str, List[str]]  # Day -> List of periods available

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            id=data.get('id', ''),
            name=data.get('name', ''),
            subjects=data.get('subjects', []),
            availability=data.get('availability', {})
        )

    def is_available(self, day: str, period: str) -> bool:
        """Check if teacher is available on a given day and period."""
        return period in self.availability.get(day, [])


@dataclass
class Room:
    """Represents a classroom or laboratory."""
    id: str
    name: str
    capacity: int
    is_lab: bool
    availability: Dict[str, List[str]]  # Day -> List of periods available

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            id=data.get('id', ''),
            name=data.get('name', ''),
            capacity=data.get('capacity', 60),
            is_lab=data.get('is_lab', False),
            availability=data.get('availability', {})
        )

    def is_available(self, day: str, period: str) -> bool:
        """Check if room is available on a given day and period."""
        return period in self.availability.get(day, [])


@dataclass
class TimetableEntry:
    """Represents a scheduled class slot in a timetable."""
    subject: str
    teacher: str
    division: str
    room: str
    class_type: str  # "Theory" or "Practical"
    day: Optional[str] = None
    period: Optional[str] = None

    def to_dict(self) -> dict:
        return {
            "subject": self.subject,
            "teacher": self.teacher,
            "division": self.division,
            "room": self.room,
            "class_type": self.class_type,
            "day": self.day,
            "period": self.period
        }


class TimetableData:
    """Container class representing the entire input dataset."""
    def __init__(self, department: str, division: str, days: List[str], periods: List[str],
                 subjects: List[Subject], teachers: List[Teacher], rooms: List[Room]):
        self.department = department
        self.division = division
        self.days = days
        self.periods = periods
        self.subjects = subjects
        self.teachers = teachers
        self.rooms = rooms

    @classmethod
    def from_dict(cls, data: dict):
        subjects = [Subject.from_dict(s) for s in data.get('subjects', [])]
        teachers = [Teacher.from_dict(t) for t in data.get('teachers', [])]
        rooms = [Room.from_dict(r) for r in data.get('rooms', [])]
        return cls(
            department=data.get('department', 'Computer Engineering'),
            division=data.get('division', 'TY-C'),
            days=data.get('days', []),
            periods=data.get('periods', []),
            subjects=subjects,
            teachers=teachers,
            rooms=rooms
        )
