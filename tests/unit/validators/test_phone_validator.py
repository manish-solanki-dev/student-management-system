import pytest

from student_management.exceptions.validation import InvalidPhoneError
from student_management.validators.phone_validator import PhoneValidator


@pytest.mark.parametrize(
    "phone",
    [
        "9876543210",
        "8123456789",
        "7012345678",
        "6123456789",
    ],
)
def test_accepts_valid_phone(phone: str) -> None:
    validator = PhoneValidator()
    validator.validate(phone)


@pytest.mark.parametrize(
    "phone",
    [
        "",
        "5123456789",
        "1234567890",
        "987654321",
        "98765432101",
        "98765abc10",
        "+919876543210",
        "987-654-3210",
        "987 654 3210",
    ],
)
def test_rejects_invalid_phone(phone: str) -> None:
    validator = PhoneValidator()
    with pytest.raises(InvalidPhoneError):
        validator.validate(phone)
