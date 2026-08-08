from datetime import datetime

import pytest

from student_management.domain.models.student import Student
from student_management.exceptions.student import (
    DuplicateStudentError,
    InvalidSortFieldError,
    StudentNotFoundError,
)
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


def test_update_student_updates_existing_student() -> None:
    repository = FakeStudentRepository()
    service = create_student_service(repository)

    existing_student = create_valid_student()
    repository.save(existing_student)

    updated_student = create_valid_student()
    updated_student.gpa = 9.5

    result = service.update_student(updated_student)

    assert result is updated_student

    saved_student = repository.get_by_id("STU001")
    assert saved_student is updated_student
    assert saved_student.gpa == 9.5


def test_update_student_rejects_nonexistent_student() -> None:
    repository = FakeStudentRepository()
    service = create_student_service(repository)

    student = create_valid_student()

    with pytest.raises(StudentNotFoundError):
        service.update_student(student)


def test_update_student_rejects_invalid_student() -> None:
    repository = FakeStudentRepository()
    service = create_student_service(repository)

    existing_student = create_valid_student()
    repository.save(existing_student)

    invalid_student = create_valid_student()
    invalid_student.email = "invalid-email"

    with pytest.raises(InvalidEmailError):
        service.update_student(invalid_student)

    saved_student = repository.get_by_id("STU001")
    assert saved_student is existing_student


def test_update_student_raises_error_when_repository_update_fails() -> None:
    repository = FakeStudentRepository()
    service = create_student_service(repository)

    student = create_valid_student()
    repository.save(student)

    repository.should_fail_update = True

    with pytest.raises(StudentNotFoundError):
        service.update_student(student)


def test_delete_student_deletes_existing_student() -> None:
    repository = FakeStudentRepository()
    service = create_student_service(repository)

    student = create_valid_student()
    repository.save(student)

    service.delete_student("STU001")

    assert repository.get_by_id("STU001") is None


def test_delete_student_rejects_nonexistent_student() -> None:
    repository = FakeStudentRepository()
    service = create_student_service(repository)

    with pytest.raises(StudentNotFoundError):
        service.delete_student("STU001")


def test_get_student_returns_existing_student() -> None:
    repository = FakeStudentRepository()
    service = create_student_service(repository)

    student = create_valid_student()
    repository.save(student)

    result = service.get_student("STU001")

    assert result == student


def test_get_student_rejects_nonexistent_student() -> None:
    repository = FakeStudentRepository()
    service = create_student_service(repository)

    with pytest.raises(StudentNotFoundError):
        service.get_student("STU001")


def test_get_all_students_returns_all_students() -> None:
    repository = FakeStudentRepository()
    service = create_student_service(repository)

    first_student = create_valid_student()
    second_student = create_valid_student()
    second_student.student_id = "STU002"

    repository.save(first_student)
    repository.save(second_student)

    result = service.get_all_students()

    assert result == [first_student, second_student]


def test_get_all_students_returns_empty_list_when_no_students_exist() -> None:
    repository = FakeStudentRepository()
    service = create_student_service(repository)

    result = service.get_all_students()

    assert result == []


def test_search_students_by_id() -> None:
    repository = FakeStudentRepository()
    service = create_student_service(repository)

    student = create_valid_student()
    repository.save(student)

    result = service.search_students("STU001", "id")

    assert result == [student]


def test_search_students_by_name() -> None:
    repository = FakeStudentRepository()
    service = create_student_service(repository)

    student = create_valid_student()
    repository.save(student)

    result = service.search_students("Manish", "name")

    assert result == [student]


def test_search_students_by_email() -> None:
    repository = FakeStudentRepository()
    service = create_student_service(repository)

    student = create_valid_student()
    repository.save(student)

    result = service.search_students(
        "manish@example.com",
        "email",
    )

    assert result == [student]


def test_search_students_by_course() -> None:
    repository = FakeStudentRepository()
    service = create_student_service(repository)

    student = create_valid_student()
    repository.save(student)

    result = service.search_students("Python", "course")

    assert result == [student]


def test_search_students_returns_empty_list_when_no_match() -> None:
    repository = FakeStudentRepository()
    service = create_student_service(repository)

    result = service.search_students("Java", "course")

    assert result == []


def test_sort_students_by_gpa() -> None:
    repository = FakeStudentRepository()
    service = create_student_service(repository)

    first_student = create_valid_student()
    first_student.student_id = "STU001"
    first_student.gpa = 8.5

    second_student = create_valid_student()
    second_student.student_id = "STU002"
    second_student.gpa = 9.5

    third_student = create_valid_student()
    third_student.student_id = "STU003"
    third_student.gpa = 7.0

    repository.save(first_student)
    repository.save(second_student)
    repository.save(third_student)

    result = service.sort_students("gpa")

    assert [student.gpa for student in result] == [7.0, 8.5, 9.5]


def test_sort_students_by_gpa_descending() -> None:
    repository = FakeStudentRepository()
    service = create_student_service(repository)

    first_student = create_valid_student()
    first_student.student_id = "STU001"
    first_student.gpa = 8.5

    second_student = create_valid_student()
    second_student.student_id = "STU002"
    second_student.gpa = 9.5

    third_student = create_valid_student()
    third_student.student_id = "STU003"
    third_student.gpa = 7.0

    repository.save(first_student)
    repository.save(second_student)
    repository.save(third_student)

    result = service.sort_students("gpa", descending=True)

    assert [student.gpa for student in result] == [9.5, 8.5, 7.0]


def test_sort_students_by_age() -> None:
    repository = FakeStudentRepository()
    service = create_student_service(repository)

    first_student = create_valid_student()
    first_student.student_id = "STU001"
    first_student.age = 25

    second_student = create_valid_student()
    second_student.student_id = "STU002"
    second_student.age = 18

    third_student = create_valid_student()
    third_student.student_id = "STU003"
    third_student.age = 21

    repository.save(first_student)
    repository.save(second_student)
    repository.save(third_student)

    result = service.sort_students("age")

    assert [student.age for student in result] == [18, 21, 25]


def test_sort_students_by_student_id() -> None:
    repository = FakeStudentRepository()
    service = create_student_service(repository)

    first_student = create_valid_student()
    first_student.student_id = "STU003"

    second_student = create_valid_student()
    second_student.student_id = "STU001"

    third_student = create_valid_student()
    third_student.student_id = "STU002"

    repository.save(first_student)
    repository.save(second_student)
    repository.save(third_student)

    result = service.sort_students("student_id")

    assert [student.student_id for student in result] == [
        "STU001",
        "STU002",
        "STU003",
    ]


def test_sort_students_by_name() -> None:
    repository = FakeStudentRepository()
    service = create_student_service(repository)

    first_student = create_valid_student()
    first_student.student_id = "STU001"
    first_student.first_name = "Rahul"
    first_student.last_name = "Shah"

    second_student = create_valid_student()
    second_student.student_id = "STU002"
    second_student.first_name = "Amit"
    second_student.last_name = "Patel"

    third_student = create_valid_student()
    third_student.student_id = "STU003"
    third_student.first_name = "Manish"
    third_student.last_name = "Solanki"

    repository.save(first_student)
    repository.save(second_student)
    repository.save(third_student)

    result = service.sort_students("name")

    assert [student.first_name for student in result] == [
        "Amit",
        "Manish",
        "Rahul",
    ]


def test_sort_students_returns_empty_list_when_no_students_exist() -> None:
    repository = FakeStudentRepository()
    service = create_student_service(repository)

    result = service.sort_students("gpa")

    assert result == []


def test_sort_students_rejects_invalid_field() -> None:
    repository = FakeStudentRepository()
    service = create_student_service(repository)

    with pytest.raises(InvalidSortFieldError):
        service.sort_students("salary")
