import re

from student_management.exceptions.validation import InvalidEmailError
from student_management.validators.base import Validator


class EmailValidator(Validator[str]):
    """Validate email address format."""

    PATTERN = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")

    def validate(self, value: str) -> None:
        """Validate the email address format."""
        if not self.PATTERN.fullmatch(value):
            raise InvalidEmailError(
                "Email must have a valid format, such as name@example.com."
            )
