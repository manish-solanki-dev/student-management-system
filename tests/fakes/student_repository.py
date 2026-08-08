from student_management.domain.models.student import Student
from student_management.repositories.student_repository import StudentRepository


class FakeStudentRepository(StudentRepository):
    """In-memory repository used for unit testing."""

    def __init__(self) -> None:
        self._students: dict[str, Student] = {}

    def save(self, student: Student) -> None:
        """Persist a student in memory."""
        self._students[student.student_id] = student

    def get_by_id(self, student_id: str) -> Student | None:
        """Return a student by ID, or None if it does not exist."""
        return self._students.get(student_id)

    def get_all(self) -> list[Student]:
        """Return all students."""
        return list(self._students.values())

    def update(self, student: Student) -> bool:
        """Update an existing student."""
        if student.student_id not in self._students:
            return False

        self._students[student.student_id] = student
        return True

    def delete(self, student_id: str) -> bool:
        """Delete a student by ID."""
        if student_id not in self._students:
            return False

        del self._students[student_id]
        return True

    def exists(self, student_id: str) -> bool:
        """Return whether a student exists."""
        return student_id in self._students
