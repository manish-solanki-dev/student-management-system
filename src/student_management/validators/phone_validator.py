import re

from student_management.exceptions.validation import InvalidPhoneError
from student_management.validators.base import Validator


class PhoneValidator(Validator[str]):
    """Validate Indian mobile phone number format."""

    PATTERN = re.compile(r"^[6-9][0-9]{9}$")

    def validate(self, value: str) -> None:
        """Validate the phone number format."""
        if not self.PATTERN.fullmatch(value):
            raise InvalidPhoneError(
                "Phone number must contain 10 digits and start with 6-9."
            )
