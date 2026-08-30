import logging
from datetime import UTC, datetime

from student_management.domain.models.student import Student
from student_management.exceptions.student import (
    DuplicateStudentError,
    InvalidSortFieldError,
    StudentNotFoundError,
)
from student_management.exceptions.validation import (
    InvalidAgeError,
    InvalidEmailError,
    InvalidGPAError,
    InvalidPhoneError,
    InvalidStudentIDError,
)
from student_management.services.student_service import StudentService

logger = logging.getLogger(__name__)


class StudentCLI:
    """Handle student-related command-line interactions."""

    def __init__(self, service: StudentService) -> None:
        self._service = service

    def add_student(self) -> None:
        """Collect student information and add a new student."""
        student = self._create_student_from_input()
        logger.info("User requested student creation: %s", student.student_id)

        try:
            self._service.add_student(student)
        except (
            DuplicateStudentError,
            InvalidAgeError,
            InvalidEmailError,
            InvalidGPAError,
            InvalidPhoneError,
            InvalidStudentIDError,
        ) as error:
            print(f"Error: {error}")
            return

        print(f"Student '{student.student_id}' added successfully.")

    def _create_student_from_input(self) -> Student:
        """Create a Student object from command-line input."""
        student_id = input("Enter Student ID: ").strip()
        first_name = input("Enter First Name: ").strip()
        last_name = input("Enter Last Name: ").strip()
        email = input("Enter Email: ").strip()
        phone = input("Enter Phone: ").strip()
        age = self._get_int("Enter Age: ")
        course = input("Enter Course: ").strip()
        gpa = self._get_float("Enter GPA: ")

        return Student(
            student_id=student_id,
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            age=age,
            course=course,
            gpa=gpa,
            created_at=datetime.now(UTC),
        )

    @staticmethod
    def _get_int(prompt: str) -> int:
        """Read an integer from the user."""
        while True:
            value = input(prompt).strip()

            try:
                return int(value)
            except ValueError:
                print("Error: Please enter a valid integer.")

    @staticmethod
    def _get_float(prompt: str) -> float:
        """Read a floating-point number from the user."""
        while True:
            value = input(prompt).strip()

            try:
                return float(value)
            except ValueError:
                print("Error: Please enter a valid number.")

    def view_student(self) -> None:
        """Display a student by student ID."""
        student_id = input("Enter Student ID: ").strip()

        try:
            student = self._service.get_student(student_id)
        except StudentNotFoundError as error:
            print(f"Error: {error}")
            return

        self._display_student_details(student)

    def view_all_students(self) -> None:
        """Display all students."""
        students = self._service.get_all_students()

        if not students:
            print("No students found.")
            return

        print()
        print("=" * 80)
        print("                           All Students")
        print("=" * 80)

        print(f"{'ID':<10}" f"{'Name':<25}" f"{'Course':<25}" f"{'GPA':<10}")
        print("-" * 80)

        for student in students:
            name = f"{student.first_name} {student.last_name}"

            print(
                f"{student.student_id:<10}"
                f"{name:<25}"
                f"{student.course:<25}"
                f"{student.gpa:<10.2f}"
            )

        print("=" * 80)

    def search_students(self) -> None:
        """Search students by ID, name, email, or course."""
        print()
        print("=" * 40)
        print("        Search Students")
        print("=" * 40)
        print("1. Search by Student ID")
        print("2. Search by Name")
        print("3. Search by Email")
        print("4. Search by Course")
        print("5. Back")
        print("=" * 40)

        choice = input("Enter your choice: ").strip()

        search_fields = {
            "1": "id",
            "2": "name",
            "3": "email",
            "4": "course",
        }

        if choice == "5":
            return

        field = search_fields.get(choice)

        if field is None:
            logger.warning(
                "User selected invalid search option: %s",
                choice,
            )
            print("Error: Invalid search option.")
            return

        query = input("Enter search value: ").strip()

        logger.info(
            "User requested student search: field=%s",
            field,
        )

        if not query:
            logger.warning("User entered an empty search value.")
            print("Error: Search value cannot be empty.")
            return

        students = self._service.search_students(
            query=query,
            field=field,
        )

        if not students:
            print(f"No students found matching '{query}'.")
            return

        self._sort_search_results(students)

    @staticmethod
    def _display_student_table(students: list[Student]) -> None:
        """Display students in a compact table."""
        print()
        print("=" * 80)
        print("                         Search Results")
        print("=" * 80)

        print(f"{'ID':<10}" f"{'Name':<25}" f"{'Course':<25}" f"{'GPA':<10}")
        print("-" * 80)

        for student in students:
            name = f"{student.first_name} {student.last_name}"

            print(
                f"{student.student_id:<10}"
                f"{name:<25}"
                f"{student.course:<25}"
                f"{student.gpa:<10.2f}"
            )

        print("=" * 80)

    def _sort_search_results(self, students: list[Student]) -> None:
        """Optionally sort and display search results."""
        print()
        print("=" * 40)
        print("        Sort Search Results")
        print("=" * 40)
        print("1. Name")
        print("2. GPA")
        print("3. Age")
        print("4. Student ID")
        print("5. No Sorting")
        print("=" * 40)

        choice = input("Enter your choice: ").strip()

        sort_fields = {
            "1": "name",
            "2": "gpa",
            "3": "age",
            "4": "student_id",
        }

        if choice == "5":
            self._display_student_table(students)
            return

        field = sort_fields.get(choice)

        if field is None:
            logger.warning(
                "User selected invalid sort option: %s",
                choice,
            )
            print("Error: Invalid sort option.")
            return

        descending = input("Sort descending? (y/n): ").strip().lower() == "y"

        try:
            sorted_students = self._service.sort_student_list(
                students,
                field,
                descending,
            )
        except InvalidSortFieldError as error:
            print(f"Error: {error}")
            return

        self._display_student_table(sorted_students)

    def update_student(self) -> None:
        """Update an existing student's information."""
        student_id = input("Enter Student ID to update: ").strip()

        logger.info(
            "User requested student update: %s",
            student_id,
        )

        try:
            existing_student = self._service.get_student(student_id)
        except StudentNotFoundError as error:
            print(f"Error: {error}")
            return

        print()
        print("=" * 40)
        print("        Update Student")
        print("=" * 40)
        print("Press Enter to keep the current value.")
        print()

        first_name = self._get_updated_value(
            "First Name",
            existing_student.first_name,
        )
        last_name = self._get_updated_value(
            "Last Name",
            existing_student.last_name,
        )
        email = self._get_updated_value(
            "Email",
            existing_student.email,
        )
        phone = self._get_updated_value(
            "Phone",
            existing_student.phone,
        )

        age = self._get_updated_int(
            "Age",
            existing_student.age,
        )

        course = self._get_updated_value(
            "Course",
            existing_student.course,
        )

        gpa = self._get_updated_float(
            "GPA",
            existing_student.gpa,
        )

        updated_student = Student(
            student_id=existing_student.student_id,
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            age=age,
            course=course,
            gpa=gpa,
            created_at=existing_student.created_at,
        )

        try:
            self._service.update_student(updated_student)
        except (
            InvalidAgeError,
            InvalidEmailError,
            InvalidGPAError,
            InvalidPhoneError,
            InvalidStudentIDError,
            StudentNotFoundError,
        ) as error:
            print(f"Error: {error}")
            return

        print(f"Student '{updated_student.student_id}' " "updated successfully.")

    @staticmethod
    def _get_updated_value(
        field_name: str,
        current_value: str,
    ) -> str:
        """Return a new text value or keep the current value."""
        value = input(f"{field_name} [{current_value}]: ").strip()

        return value if value else current_value

    @staticmethod
    def _get_updated_int(
        field_name: str,
        current_value: int,
    ) -> int:
        """Return a new integer value or keep the current value."""
        while True:
            value = input(f"{field_name} [{current_value}]: ").strip()

            if not value:
                return current_value

            try:
                return int(value)
            except ValueError:
                print(f"Error: {field_name} must be a valid integer.")

    @staticmethod
    def _get_updated_float(
        field_name: str,
        current_value: float,
    ) -> float:
        """Return a new floating-point value or keep the current value."""
        while True:
            value = input(f"{field_name} [{current_value}]: ").strip()

            if not value:
                return current_value

            try:
                return float(value)
            except ValueError:
                print(f"Error: {field_name} must be a valid number.")

    def delete_student(self) -> None:
        """Delete a student after confirming the operation."""
        student_id = input("Enter Student ID to delete: ").strip()

        logger.info(
            "User requested student deletion: %s",
            student_id,
        )

        try:
            student = self._service.get_student(student_id)
        except StudentNotFoundError as error:
            print(f"Error: {error}")
            return

        self._display_student_details(student)

        confirmation = (
            input("Are you sure you want to delete this student? (y/n): ")
            .strip()
            .lower()
        )

        if confirmation != "y":
            logger.info(
                "User cancelled student deletion: %s",
                student_id,
            )
            print("Deletion cancelled.")
            return

        try:
            self._service.delete_student(student_id)
        except StudentNotFoundError as error:
            print(f"Error: {error}")
            return

        print(f"Student '{student_id}' deleted successfully.")

    @staticmethod
    def _display_student_details(student: Student) -> None:
        """Display complete details of a student."""
        print()
        print("=" * 40)
        print("        Student Details")
        print("=" * 40)
        print(f"Student ID : {student.student_id}")
        print(f"Name       : {student.first_name} {student.last_name}")
        print(f"Email      : {student.email}")
        print(f"Phone      : {student.phone}")
        print(f"Age        : {student.age}")
        print(f"Course     : {student.course}")
        print(f"GPA        : {student.gpa}")
        print(f"Created At : {student.created_at}")
        print("=" * 40)
