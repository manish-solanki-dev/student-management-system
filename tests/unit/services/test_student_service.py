from datetime import datetime

import pytest

from student_management.domain.models.student import Student
from student_management.exceptions.student import DuplicateStudentError
from student_management.exceptions.validation import InvalidEmailError
from student_management.services.student_service import StudentService
from student_management.validators.age_validator import AgeValidator
from student_management.validators.email_validator import EmailValidator
from student_management.validators.gpa_validator import GPAValidator
from student_management.validators.phone_validator import PhoneValidator
from student_management.validators.student_id_validator import StudentIDValidator
from student_management.validators.student_validator import StudentValidator
from tests.fakes.student_repository import FakeStudentRepository


def create_student_validator() -> StudentValidator:
    return StudentValidator(
        student_id_validator=StudentIDValidator(),
        email_validator=EmailValidator(),
        phone_validator=PhoneValidator(),
        age_validator=AgeValidator(),
        gpa_validator=GPAValidator(),
    )


def create_student_service(
    repository: FakeStudentRepository,
) -> StudentService:
    validator = create_student_validator()

    return StudentService(
        repository=repository,
        validator=validator,
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


def test_add_student_saves_valid_student() -> None:
    repository = FakeStudentRepository()
    service = create_student_service(repository)
    student = create_valid_student()

    result = service.add_student(student)

    assert result is student
    assert repository.get_by_id("STU001") is student


def test_add_student_rejects_duplicate_student_id() -> None:
    repository = FakeStudentRepository()
    service = create_student_service(repository)

    existing_student = create_valid_student()
    repository.save(existing_student)

    duplicate_student = create_valid_student()

    with pytest.raises(DuplicateStudentError):
        service.add_student(duplicate_student)


def test_add_student_does_not_replace_existing_student() -> None:
    repository = FakeStudentRepository()
    service = create_student_service(repository)

    existing_student = create_valid_student()
    repository.save(existing_student)

    duplicate_student = create_valid_student()

    with pytest.raises(DuplicateStudentError):
        service.add_student(duplicate_student)

    assert repository.get_by_id("STU001") is existing_student


def test_add_student_does_not_save_invalid_student() -> None:
    repository = FakeStudentRepository()
    service = create_student_service(repository)

    student = create_valid_student()
    student.email = "invalid-email"

    with pytest.raises(InvalidEmailError):
        service.add_student(student)

    assert repository.get_by_id("STU001") is None
