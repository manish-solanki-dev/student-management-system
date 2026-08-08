from student_management.domain.models.student import Student
from student_management.validators.age_validator import AgeValidator
from student_management.validators.email_validator import EmailValidator
from student_management.validators.gpa_validator import GPAValidator
from student_management.validators.phone_validator import PhoneValidator
from student_management.validators.student_id_validator import StudentIDValidator


class StudentValidator:
    """Validate the fields of a Student entity."""

    def __init__(
        self,
        student_id_validator: StudentIDValidator,
        email_validator: EmailValidator,
        phone_validator: PhoneValidator,
        age_validator: AgeValidator,
        gpa_validator: GPAValidator,
    ) -> None:
        self._student_id_validator = student_id_validator
        self._email_validator = email_validator
        self._phone_validator = phone_validator
        self._age_validator = age_validator
        self._gpa_validator = gpa_validator

    def validate(self, student: Student) -> None:
        """Validate all applicable fields of a student."""
        self._student_id_validator.validate(student.student_id)
        self._email_validator.validate(student.email)
        self._phone_validator.validate(student.phone)
        self._age_validator.validate(student.age)
        self._gpa_validator.validate(student.gpa)
