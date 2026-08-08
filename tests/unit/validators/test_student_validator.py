from datetime import datetime

import pytest

from student_management.domain.models.student import Student
from student_management.exceptions.validation import InvalidEmailError
from student_management.validators.age_validator import AgeValidator
from student_management.validators.email_validator import EmailValidator
from student_management.validators.gpa_validator import GPAValidator
from student_management.validators.phone_validator import PhoneValidator
from student_management.validators.student_id_validator import StudentIDValidator
from student_management.validators.student_validator import StudentValidator


def create_student_validator() -> StudentValidator:
    return StudentValidator(
        student_id_validator=StudentIDValidator(),
        email_validator=EmailValidator(),
        phone_validator=PhoneValidator(),
        age_validator=AgeValidator(),
        gpa_validator=GPAValidator(),
    )


def create_valid_student() -> Student:
    return Student(
        student_id="STU001",
        first_name="Manish",
        last_name="Solanki",
        email="manish@example.com",
        phone="9876543210",
        age=21,
        course="Python",
        gpa=8.5,
        created_at=datetime.fromisoformat("2023-01-01T10:00:00+00:00"),
    )


def test_accepts_valid_student() -> None:
    validator = create_student_validator()
    student = create_valid_student()
    validator.validate(student)


def test_rejects_invalid_email() -> None:

    validator = create_student_validator()
    student = create_valid_student()
    student.email = "invalid-email"

    with pytest.raises(InvalidEmailError):
        validator.validate(student)
