import pytest

from student_management.exceptions.validation import InvalidEmailError
from student_management.validators.email_validator import EmailValidator


@pytest.mark.parametrize(
    "email",
    [
        "manish@gmail.com",
        "rahul@example.com",
        "john.doe@college.ac.in",
        "student123@university.edu",
        "user+test@example.com",
    ],
)
def test_accepts_valid_email(email: str) -> None:
    validator = EmailValidator()
    validator.validate(email)


@pytest.mark.parametrize(
    "email",
    [
        "",
        "manish",
        "manish@",
        "@gmail.com",
        "manish@gmail",
        "manish @gmail.com",
        "manish@example",
        "[manish..patel@example.com](mailto:manish..patel@example.com)",
    ],
)
def test_rejects_invalid_email(email: str) -> None:
    validator = EmailValidator()
    with pytest.raises(InvalidEmailError):
        validator.validate(email)
