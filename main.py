import logging
from pathlib import Path

from student_management.cli.application import Application
from student_management.cli.menu import Menu
from student_management.cli.student_cli import StudentCLI
from student_management.logging.logger import configure_logging
from student_management.repositories.csv_student_repository import (
    CSVStudentRepository,
)
from student_management.services.student_service import StudentService
from student_management.validators.age_validator import AgeValidator
from student_management.validators.email_validator import EmailValidator
from student_management.validators.gpa_validator import GPAValidator
from student_management.validators.phone_validator import PhoneValidator
from student_management.validators.student_id_validator import StudentIDValidator
from student_management.validators.student_validator import StudentValidator

logger = logging.getLogger(__name__)


def main() -> None:
    """Start the Student Management System."""
    configure_logging()

    logger.info("Application started.")

    repository = CSVStudentRepository(
        Path("data/students.csv"),
    )

    validator = StudentValidator(
        student_id_validator=StudentIDValidator(),
        email_validator=EmailValidator(),
        phone_validator=PhoneValidator(),
        age_validator=AgeValidator(),
        gpa_validator=GPAValidator(),
    )

    service = StudentService(
        repository=repository,
        validator=validator,
    )

    student_cli = StudentCLI(service)

    application = Application(
        menu=Menu(),
        student_cli=student_cli,
    )

    application.run()


if __name__ == "__main__":
    main()
