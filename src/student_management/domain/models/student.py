from dataclasses import dataclass
from datetime import datetime


@dataclass(slots=True)
class Student:
    """Represent a student in the student management domain."""

    student_id: str
    first_name: str
    last_name: str
    email: str
    phone: str
    age: int
    course: str
    gpa: float
    created_at: datetime
