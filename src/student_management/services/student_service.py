from student_management.domain.models.student import Student
from student_management.exceptions.student import (
    DuplicateStudentError,
    StudentNotFoundError,
)
from student_management.repositories.student_repository import StudentRepository
from student_management.validators.student_validator import StudentValidator


class StudentService:
    """Provide application-level operations for students."""

    def __init__(
        self,
        repository: StudentRepository,
        validator: StudentValidator,
    ) -> None:
        self._repository = repository
        self._validator = validator

    def add_student(self, student: Student) -> Student:
        """Validate and persist a new student."""
        self._validator.validate(student)

        if self._repository.exists(student.student_id):
            raise DuplicateStudentError(
                f"Student ID already exists: {student.student_id}"
            )

        self._repository.save(student)
        return student

    def update_student(self, student: Student) -> Student:
        """Validate and update an existing student."""
        self._validator.validate(student)

        updated = self._repository.update(student)

        if not updated:
            raise StudentNotFoundError(f"Student not found: {student.student_id}")

        return student

    def delete_student(self, student_id: str) -> None:
        """Delete an existing student."""
        deleted = self._repository.delete(student_id)

        if not deleted:
            raise StudentNotFoundError(f"Student not found: {student_id}")

    def get_student(self, student_id: str) -> Student:
        """Return a student by ID or raise StudentNotFoundError."""
        student = self._repository.get_by_id(student_id)

        if student is None:
            raise StudentNotFoundError(f"Student with ID '{student_id}' was not found.")

        return student

    def get_all_students(self) -> list[Student]:
        """Return all students."""
        return self._repository.get_all()
