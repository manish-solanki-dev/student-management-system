from abc import ABC, abstractmethod

from student_management.domain.models.student import Student


class StudentRepository(ABC):
    """Define persistence operations for Student entities."""

    @abstractmethod
    def save(self, student: Student) -> None:
        """Persist a new student."""
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, student_id: str) -> Student | None:
        """Return a student by ID, or None if it does not exist."""
        raise NotImplementedError

    @abstractmethod
    def get_all(self) -> list[Student]:
        """Return all students."""
        raise NotImplementedError

    @abstractmethod
    def update(self, student: Student) -> None:
        """Update an existing student."""
        raise NotImplementedError

    @abstractmethod
    def delete(self, student_id: str) -> bool:
        """Delete a student and return whether deletion occurred."""
        raise NotImplementedError

    @abstractmethod
    def exists(self, student_id: str) -> bool:
        """Return whether a student with the given ID exists."""
        raise NotImplementedError
