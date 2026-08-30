from student_management.exceptions.base import StudentManagementError


class StudentNotFoundError(StudentManagementError):
    """Raised when a requested student does not exist."""


class DuplicateStudentError(StudentManagementError):
    """Raised when a student ID already exists."""


class InvalidSortFieldError(StudentManagementError):
    """Raised when an unsupported student sort field is requested."""


class InvalidSearchFieldError(StudentManagementError):
    """Raised when an unsupported student search field is requested."""
