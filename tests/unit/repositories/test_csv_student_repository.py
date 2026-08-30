from datetime import datetime
from pathlib import Path

from student_management.domain.models.student import Student
from student_management.repositories.csv_student_repository import (
    CSVStudentRepository,
)


def create_student() -> Student:
    """Create a valid student for repository tests."""
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


def test_save_persists_student(tmp_path: Path) -> None:
    """Test that save writes a student to the CSV file."""
    file_path = tmp_path / "students.csv"
    repository = CSVStudentRepository(file_path)

    student = create_student()

    repository.save(student)

    result = repository.get_by_id("STU001")

    assert result == student


def test_get_by_id_returns_none_when_student_does_not_exist(
    tmp_path: Path,
) -> None:
    """Test that missing students return None."""
    file_path = tmp_path / "students.csv"
    repository = CSVStudentRepository(file_path)

    result = repository.get_by_id("STU999")

    assert result is None


def test_get_all_returns_all_students(tmp_path: Path) -> None:
    """Test that get_all returns every stored student."""
    file_path = tmp_path / "students.csv"
    repository = CSVStudentRepository(file_path)

    first_student = create_student()

    second_student = create_student()
    second_student.student_id = "STU002"
    second_student.first_name = "Rahul"

    repository.save(first_student)
    repository.save(second_student)

    result = repository.get_all()

    assert result == [first_student, second_student]


def test_update_updates_existing_student(tmp_path: Path) -> None:
    """Test that update modifies an existing student."""
    file_path = tmp_path / "students.csv"
    repository = CSVStudentRepository(file_path)

    student = create_student()
    repository.save(student)

    updated_student = create_student()
    updated_student.gpa = 9.5

    result = repository.update(updated_student)

    assert result is True
    assert repository.get_by_id("STU001") == updated_student


def test_update_returns_false_when_student_does_not_exist(
    tmp_path: Path,
) -> None:
    """Test that update returns False for a missing student."""
    file_path = tmp_path / "students.csv"
    repository = CSVStudentRepository(file_path)

    student = create_student()

    result = repository.update(student)

    assert result is False


def test_delete_removes_existing_student(tmp_path: Path) -> None:
    """Test that delete removes an existing student."""
    file_path = tmp_path / "students.csv"
    repository = CSVStudentRepository(file_path)

    student = create_student()
    repository.save(student)

    result = repository.delete("STU001")

    assert result is True
    assert repository.get_by_id("STU001") is None


def test_delete_returns_false_when_student_does_not_exist(
    tmp_path: Path,
) -> None:
    """Test that delete returns False for a missing student."""
    file_path = tmp_path / "students.csv"
    repository = CSVStudentRepository(file_path)

    result = repository.delete("STU999")

    assert result is False


def test_exists_returns_true_for_existing_student(
    tmp_path: Path,
) -> None:
    """Test that exists returns True for an existing student."""
    file_path = tmp_path / "students.csv"
    repository = CSVStudentRepository(file_path)

    student = create_student()
    repository.save(student)

    assert repository.exists("STU001") is True


def test_exists_returns_false_for_missing_student(
    tmp_path: Path,
) -> None:
    """Test that exists returns False for a missing student."""
    file_path = tmp_path / "students.csv"
    repository = CSVStudentRepository(file_path)

    assert repository.exists("STU999") is False
