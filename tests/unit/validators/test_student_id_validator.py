import pytest

from student_management.exceptions.validation import InvalidStudentIDError
from student_management.validators.student_id_validator import StudentIDValidator


@pytest.mark.parametrize(
    "student_id",
    [
        "STU001",
        "STU123",
        "STU999",
    ],
)
def test_accepts_valid_student_id(student_id: str) -> None:
    validator = StudentIDValidator()
    validator.validate(student_id)


@pytest.mark.parametrize(
    "student_id",
    [
        "",
        "stu001",
        "STU1",
        "STU01",
        "STUDENT001",
        "123",
        "ABC001",
    ],
)
def test_rejects_invalid_student_id(student_id: str) -> None:
    validator = StudentIDValidator()
    with pytest.raises(InvalidStudentIDError):
        validator.validate(student_id)
