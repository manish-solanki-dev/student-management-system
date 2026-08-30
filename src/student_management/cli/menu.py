class Menu:
    """Display and handle the main application menu."""

    def display(self) -> None:
        """Display available menu options."""
        print()
        print("=" * 40)
        print("     Student Management System")
        print("=" * 40)
        print("1. Add Student")
        print("2. View Student")
        print("3. View All Students")
        print("4. Update Student")
        print("5. Delete Student")
        print("6. Search Students")
        print("7. Exit")
        print("=" * 40)

    def get_choice(self) -> str:
        """Return the user's selected menu option."""
        return input("Enter your choice: ").strip()
