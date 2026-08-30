from student_management.cli.menu import Menu
from student_management.cli.student_cli import StudentCLI


class Application:
    """Application entry point for the Student Management System."""

    def __init__(
        self,
        menu: Menu,
        student_cli: StudentCLI,
    ) -> None:
        self._menu = menu
        self._student_cli = student_cli

    def run(self) -> None:
        """Start the application and process menu selections."""
        actions = {
            "1": self._student_cli.add_student,
            "2": self._student_cli.view_student,
            "3": self._student_cli.view_all_students,
            "4": self._student_cli.update_student,
            "5": self._student_cli.delete_student,
            "6": self._student_cli.search_students,
        }

        while True:
            self._menu.display()
            choice = self._menu.get_choice()

            if choice == "7":
                print("Goodbye!")
                break

            action = actions.get(choice)

            if action is None:
                print("Error: Invalid menu option.")
                continue

            action()
