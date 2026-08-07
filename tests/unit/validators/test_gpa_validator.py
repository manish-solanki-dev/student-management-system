import pytest

from student_management.exceptions.validation import InvalidGPAError
from student_management.validators.gpa_validator import GPAValidator


@pytest.mark.parametrize(
    "gpa",
    [
        0,
        0.0,
        5,
        7.5,
        8.25,
        10,
        10.0,
    ],
)
def test_accepts_valid_gpa(gpa: float) -> None:
    validator = GPAValidator()
    validator.validate(gpa)


@pytest.mark.parametrize(
    "gpa",
    [
        -1,
        -0.1,
        10.1,
        11,
        True,
        False,
    ],
)
def test_rejects_invalid_gpa(gpa: float) -> None:
    validator = GPAValidator()
    with pytest.raises(InvalidGPAError):
        validator.validate(gpa)
