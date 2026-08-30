import logging

from student_management.domain.models.student import Student
from student_management.exceptions.student import (
    DuplicateStudentError,
    InvalidSearchFieldError,
    InvalidSortFieldError,
    StudentNotFoundError,
)
from student_management.repositories.student_repository import StudentRepository
from student_management.validators.student_validator import StudentValidator

logger = logging.getLogger(__name__)


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
            logger.warning(
                "Attempted to add duplicate student: %s",
                student.student_id,
            )

            raise DuplicateStudentError(
                f"Student ID already exists: {student.student_id}"
            )

        self._repository.save(student)

        logger.info(
            "Student added successfully: %s",
            student.student_id,
        )

        return student

    def update_student(self, student: Student) -> Student:
        """Validate and update an existing student."""
        self._validator.validate(student)

        updated = self._repository.update(student)

        if not updated:
            logger.warning(
                "Attempted to update non-existent student: %s",
                student.student_id,
            )

            raise StudentNotFoundError(f"Student not found: {student.student_id}")

        logger.info(
            "Student updated successfully: %s",
            student.student_id,
        )

        return student

    def delete_student(self, student_id: str) -> None:
        """Delete an existing student."""
        deleted = self._repository.delete(student_id)

        if not deleted:
            logger.warning(
                "Attempted to delete non-existent student: %s",
                student_id,
            )

            raise StudentNotFoundError(f"Student not found: {student_id}")

        logger.info(
            "Student deleted successfully: %s",
            student_id,
        )

    def get_student(self, student_id: str) -> Student:
        """Return a student by ID or raise StudentNotFoundError."""
        student = self._repository.get_by_id(student_id)

        if student is None:
            logger.warning(
                "Student lookup failed: %s",
                student_id,
            )

            raise StudentNotFoundError(f"Student with ID '{student_id}' was not found.")

        return student

    def get_all_students(
        self,
        sort_by: str | None = None,
        descending: bool = False,
    ) -> list[Student]:
        """Return all students, optionally sorted."""
        students = self._repository.get_all()

        if sort_by is None:
            return students

        return self._sort_student_list(
            students,
            sort_by,
            descending,
        )

    def search_students(self, query: str, field: str) -> list[Student]:
        """Search students by the specified field."""
        students = self._repository.get_all()

        if field == "id":
            return [student for student in students if student.student_id == query]

        if field == "name":
            query = query.lower()
            return [
                student
                for student in students
                if query in f"{student.first_name} {student.last_name}".lower()
            ]

        if field == "email":
            query = query.lower()
            return [student for student in students if query in student.email.lower()]

        if field == "course":
            query = query.lower()
            return [student for student in students if query in student.course.lower()]

        raise InvalidSearchFieldError(f"Unsupported search field: {field}")

    def sort_students(
        self,
        field: str,
        descending: bool = False,
    ) -> list[Student]:
        """Return all students sorted by the requested field."""
        students = self._repository.get_all()

        return self._sort_student_list(
            students,
            field,
            descending,
        )

    def sort_student_list(
        self,
        students: list[Student],
        field: str,
        descending: bool = False,
    ) -> list[Student]:
        """Sort an existing list of students."""
        return self._sort_student_list(
            students,
            field,
            descending,
        )

    @staticmethod
    def _sort_student_list(
        students: list[Student],
        field: str,
        descending: bool = False,
    ) -> list[Student]:
        """Sort a student list by the requested field."""
        sort_keys = {
            "student_id": lambda student: student.student_id,
            "name": lambda student: (
                student.first_name.lower(),
                student.last_name.lower(),
            ),
            "gpa": lambda student: student.gpa,
            "age": lambda student: student.age,
        }

        key = sort_keys.get(field)

        if key is None:
            raise InvalidSortFieldError(f"Unsupported sort field: {field}")

        return sorted(
            students,
            key=key,
            reverse=descending,
        )
