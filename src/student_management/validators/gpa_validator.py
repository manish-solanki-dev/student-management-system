from student_management.exceptions.validation import InvalidGPAError
from student_management.validators.base import Validator


class GPAValidator(Validator[float]):
    """Validate GPA values on a 10-point scale."""

    MIN_GPA = 0.0
    MAX_GPA = 10.0

    def validate(self, value: float) -> None:
        """Validate that GPA is within the allowed range."""
        if isinstance(value, bool):
            raise InvalidGPAError("GPA must be a numeric value between 0.0 and 10.0.")

        if not self.MIN_GPA <= value <= self.MAX_GPA:
            raise InvalidGPAError("GPA must be between 0.0 and 10.0.")
