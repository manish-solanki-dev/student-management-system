import csv
from datetime import datetime
from pathlib import Path
from typing import ClassVar

from student_management.domain.models.student import Student
from student_management.repositories.student_repository import StudentRepository


class CSVStudentRepository(StudentRepository):
    """Persist Student entities using a CSV file."""

    FIELDNAMES: ClassVar[tuple[str, ...]] = (
        "student_id",
        "first_name",
        "last_name",
        "email",
        "phone",
        "age",
        "course",
        "gpa",
        "created_at",
    )

    def __init__(self, file_path: Path) -> None:
        self._file_path = file_path
        self._ensure_file_exists()

    def save(self, student: Student) -> None:
        """Append a new student to the CSV file."""
        with self._file_path.open(
            mode="a",
            newline="",
            encoding="utf-8",
        ) as file:
            writer = csv.DictWriter(file, fieldnames=self.FIELDNAMES)

            if self._file_path.stat().st_size == 0:
                writer.writeheader()

            writer.writerow(self._student_to_row(student))

    def get_by_id(self, student_id: str) -> Student | None:
        """Return a student by ID, or None if it does not exist."""
        for student in self.get_all():
            if student.student_id == student_id:
                return student

        return None

    def get_all(self) -> list[Student]:
        """Return all students stored in the CSV file."""
        with self._file_path.open(
            mode="r",
            newline="",
            encoding="utf-8",
        ) as file:
            reader = csv.DictReader(file)
            return [self._row_to_student(row) for row in reader]

    def update(self, student: Student) -> None:
        """Update an existing student."""
        students = self.get_all()

        for index, existing_student in enumerate(students):
            if existing_student.student_id == student.student_id:
                students[index] = student
                break

        self._write_all(students)

    def delete(self, student_id: str) -> bool:
        """Delete a student and return whether deletion occurred."""
        students = self.get_all()

        remaining_students = [
            student for student in students if student.student_id != student_id
        ]

        if len(remaining_students) == len(students):
            return False

        self._write_all(remaining_students)
        return True

    def exists(self, student_id: str) -> bool:
        """Return whether a student with the given ID exists."""
        return self.get_by_id(student_id) is not None

    def _ensure_file_exists(self) -> None:
        """Create the CSV file with headers if it does not exist."""
        self._file_path.parent.mkdir(parents=True, exist_ok=True)

        if not self._file_path.exists():
            with self._file_path.open(
                mode="w",
                newline="",
                encoding="utf-8",
            ) as file:
                writer = csv.DictWriter(
                    file,
                    fieldnames=self.FIELDNAMES,
                )
                writer.writeheader()

    def _write_all(self, students: list[Student]) -> None:
        """Rewrite the CSV file with the supplied students."""
        with self._file_path.open(
            mode="w",
            newline="",
            encoding="utf-8",
        ) as file:
            writer = csv.DictWriter(file, fieldnames=self.FIELDNAMES)
            writer.writeheader()

            for student in students:
                writer.writerow(self._student_to_row(student))

    @staticmethod
    def _student_to_row(student: Student) -> dict[str, str]:
        """Convert a Student object into a CSV-compatible row."""
        return {
            "student_id": student.student_id,
            "first_name": student.first_name,
            "last_name": student.last_name,
            "email": student.email,
            "phone": student.phone,
            "age": str(student.age),
            "course": student.course,
            "gpa": str(student.gpa),
            "created_at": student.created_at.isoformat(),
        }

    @staticmethod
    def _row_to_student(row: dict[str, str]) -> Student:
        """Convert a CSV row into a Student object."""
        return Student(
            student_id=row["student_id"],
            first_name=row["first_name"],
            last_name=row["last_name"],
            email=row["email"],
            phone=row["phone"],
            age=int(row["age"]),
            course=row["course"],
            gpa=float(row["gpa"]),
            created_at=datetime.fromisoformat(row["created_at"]),
        )
