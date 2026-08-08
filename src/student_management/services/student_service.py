from student_management.domain.models.student import Student
from student_management.exceptions.student import (
    DuplicateStudentError,
    InvalidSortFieldError,
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

    def get_all_students(
        self,
        sort_by: str | None = None,
        descending: bool = False,
    ) -> list[Student]:
        """Return all students, optionally sorted."""
        students = self._repository.get_all()

        sort_keys = {
            "name": lambda student: student.first_name,
            "gpa": lambda student: student.gpa,
            "age": lambda student: student.age,
            "student_id": lambda student: student.student_id,
        }

        if sort_by is None:
            return students

        if sort_by not in sort_keys:
            raise InvalidSortFieldError(f"Unsupported sort field: {sort_by}")

        students.sort(
            key=sort_keys[sort_by],
            reverse=descending,
        )

        return students

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

        return []

    def sort_students(
        self,
        field: str,
        descending: bool = False,
    ) -> list[Student]:
        """Return students sorted by the requested field."""
        students = self._repository.get_all()

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
