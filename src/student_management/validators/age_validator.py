from student_management.exceptions.validation import InvalidAgeError
from student_management.validators.base import Validator


class AgeValidator(Validator[int]):
    """Validate student age."""

    MIN_AGE = 16
    MAX_AGE = 100

    def validate(self, value: int) -> None:
        """Validate that age is an integer within the allowed range."""
        if isinstance(value, bool) or not isinstance(value, int):
            raise InvalidAgeError("Age must be a whole number.")

        if not self.MIN_AGE <= value <= self.MAX_AGE:
            raise InvalidAgeError("Age must be between 16 and 100.")
