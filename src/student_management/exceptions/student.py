from student_management.exceptions.base import StudentManagementError


class StudentNotFoundError(StudentManagementError):
    """Raised when a requested student does not exist."""


class DuplicateStudentError(StudentManagementError):
    """Raised when a student ID already exists."""
