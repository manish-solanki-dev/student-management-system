from student_management.exceptions.base import StudentManagementError


class ValidationError(StudentManagementError):
    """Base exception for validation failures."""


class InvalidEmailError(ValidationError):
    """Raised when an email address is invalid."""


class InvalidPhoneError(ValidationError):
    """Raised when a phone number is invalid."""


class InvalidGPAError(ValidationError):
    """Raised when a GPA is invalid."""


class InvalidAgeError(ValidationError):
    """Raised when an age is invalid."""


class InvalidStudentIDError(ValidationError):
    """Raised when a student ID is invalid."""
