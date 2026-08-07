import re

from student_management.exceptions.validation import InvalidStudentIDError
from student_management.validators.base import Validator


class StudentIDValidator(Validator[str]):
    """Validate student ID format."""

    PATTERN = re.compile(r"^STU[0-9]{3}$")

    def validate(self, value: str) -> None:
        """Validate student ID format."""
        if not self.PATTERN.fullmatch(value):
            raise InvalidStudentIDError("Student ID must follow the format STU001.")
