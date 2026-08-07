import pytest

from student_management.exceptions.validation import InvalidAgeError
from student_management.validators.age_validator import AgeValidator


@pytest.mark.parametrize(
    "age",
    [
        16,
        18,
        21,
        25,
        50,
        100,
    ],
)
def test_accepts_valid_age(age: int) -> None:
    validator = AgeValidator()
    validator.validate(age)


@pytest.mark.parametrize(
    "age",
    [
        15,
        0,
        -1,
        101,
        150,
        True,
        False,
        18.5,
    ],
)
def test_rejects_invalid_age(age: int) -> None:
    validator = AgeValidator()
    with pytest.raises(InvalidAgeError):
        validator.validate(age)
