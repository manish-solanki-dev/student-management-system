
# Student Management System

A production-oriented **CLI-based Student Management System built with Python**, designed to demonstrate practical software engineering rather than a simple CRUD script.

The project separates the domain model, validation, business logic, persistence, CLI interaction, exceptions, logging, and testing into dedicated layers. Student data is currently persisted in CSV format behind a repository abstraction, making the storage implementation replaceable without coupling the service layer to CSV-specific code.

## Overview

The application provides a terminal-based interface for managing student records.

### Core capabilities

- Add a student
- View a student by ID
- View all students
- Update an existing student
- Delete a student with confirmation
- Search students by:
  - Student ID
  - Name
  - Email
  - Course
- Sort student collections by:
  - Name
  - GPA
  - Age
  - Student ID
- Validate student data
- Detect duplicate student IDs
- Persist student records to CSV
- Record important application and business events through Python logging
- Run automated unit tests for repositories, services, and validators

## Engineering Highlights

This project is intentionally structured around software engineering principles.

### Layered architecture

```text
                    ┌──────────────────────┐
                    │       CLI Layer      │
                    │ Menu / Application   │
                    │     / StudentCLI     │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │    Service Layer     │
                    │    StudentService    │
                    │  Business operations │
                    └──────────┬───────────┘
                               │
                 ┌─────────────┴─────────────┐
                 ▼                           ▼
       ┌──────────────────┐        ┌──────────────────┐
       │ Validation Layer │        │ Repository Layer │
       │ Field Validators │        │ StudentRepository│
       └────────┬─────────┘        │ CSV implementation│
                │                  └────────┬─────────┘
                ▼                           │
       ┌──────────────────┐                 ▼
       │  Domain Layer    │        ┌──────────────────┐
       │     Student      │        │   students.csv   │
       └──────────────────┘        └──────────────────┘
```

The dependency direction keeps CLI concerns away from business logic and keeps the service layer dependent on the repository abstraction rather than directly on CSV implementation details.

## Architecture & Design

### Domain Layer

The `Student` entity represents the core student data:

- Student ID
- First name
- Last name
- Email
- Phone
- Age
- Course
- GPA
- Creation timestamp

The entity is implemented as a Python `dataclass` with `slots=True`.

### Repository Layer

The repository layer defines persistence operations through an abstract `StudentRepository` interface:

- `save()`
- `get_by_id()`
- `get_all()`
- `update()`
- `delete()`
- `exists()`

`CSVStudentRepository` provides the current CSV-backed implementation.

This is an example of the **Repository Pattern** and supports the **Dependency Inversion Principle**: the service layer depends on the repository contract instead of being tied directly to CSV file operations.

Because persistence is isolated, future implementations such as SQLite or PostgreSQL can be introduced with substantially less impact on the service layer.

### Validation Layer

Validation is separated from business operations.

Dedicated validators currently handle:

- Student ID format
- Email format
- Indian mobile phone format
- Age range
- GPA range

`StudentValidator` composes these validators and validates a `Student` entity before persistence.

### Service Layer

`StudentService` contains application-level student operations such as:

- Adding students
- Updating students
- Deleting students
- Retrieving students
- Searching students
- Sorting students

The service does not contain CLI input/output code.

This separation makes the business logic independently testable and reusable by another interface in the future.

### CLI Layer

The CLI layer is responsible for user interaction:

- Menu display
- Input collection
- Input conversion
- Confirmation prompts
- User-facing error messages
- Displaying student information
- Search and sort interaction

The CLI delegates actual business operations to `StudentService`.

### Exception Handling

The project defines domain-specific exceptions instead of relying only on generic exceptions.

Examples include:

- `StudentNotFoundError`
- `DuplicateStudentError`
- `InvalidSearchFieldError`
- `InvalidSortFieldError`
- `InvalidEmailError`
- `InvalidPhoneError`
- `InvalidGPAError`
- `InvalidAgeError`
- `InvalidStudentIDError`

Validation exceptions inherit from a common `ValidationError`, while application exceptions inherit from `StudentManagementError`.

### Logging

Application-wide logging is configured centrally in:

```text
src/student_management/logging/logger.py
```

The logging configuration writes to:

```text
logs/application.log
```

and also provides console logging.

Important events are logged from the appropriate application/service components, including:

- Application startup
- Application exit
- Invalid menu selections
- Student creation requests
- Student additions
- Duplicate student attempts
- Student updates
- Failed student lookups
- Student deletions
- Cancelled deletions
- Search/sort interaction events

Generated logs are intentionally excluded from version control through `.gitignore`.

## Project Structure

```text
student-management-system/
│
├── data/
│   └── students.csv
│
├── src/
│   └── student_management/
│       ├── cli/
│       │   ├── application.py
│       │   ├── menu.py
│       │   └── student_cli.py
│       │
│       ├── domain/
│       │   └── models/
│       │       └── student.py
│       │
│       ├── exceptions/
│       │   ├── base.py
│       │   ├── student.py
│       │   └── validation.py
│       │
│       ├── logging/
│       │   └── logger.py
│       │
│       ├── repositories/
│       │   ├── student_repository.py
│       │   └── csv_student_repository.py
│       │
│       ├── services/
│       │   └── student_service.py
│       │
│       └── validators/
│           ├── base.py
│           ├── student_validator.py
│           ├── student_id_validator.py
│           ├── email_validator.py
│           ├── phone_validator.py
│           ├── age_validator.py
│           └── gpa_validator.py
│
├── tests/
│   ├── fakes/
│   │   └── student_repository.py
│   │
│   └── unit/
│       ├── repositories/
│       ├── services/
│       └── validators/
│
├── main.py
├── pyproject.toml
├── .gitignore
└── README.md
```

## Technology Stack

| Technology                         | Purpose                            |
| ---------------------------------- | ---------------------------------- |
| Python 3.11+                       | Application development            |
| Standard Library`csv`            | CSV persistence                    |
| `dataclasses`                    | Domain entity modeling             |
| `abc` / `Generic` / type hints | Abstractions and contracts         |
| `logging`                        | Application logging                |
| `pytest`                         | Automated testing                  |
| `black`                          | Code formatting                    |
| `ruff`                           | Linting                            |
| `mypy`                           | Static type checking               |
| setuptools                         | Python package/build configuration |

The application currently has **no third-party runtime dependencies**. Development tools are defined as optional dependencies in `pyproject.toml`.

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/manish-solanki-dev/student-management-system.git
cd student-management-system
```

### 2. Create a virtual environment

Windows PowerShell:

```powershell
python -m venv .venv
```

Activate it:

```powershell
.venv\Scripts\Activate.ps1
```

### 3. Install the project with development tools

```powershell
python -m pip install -e ".[dev]"
```

## Running the Application

From the project root:

```powershell
python main.py
```

The application starts an interactive menu:

```text
========================================
     Student Management System
========================================
1. Add Student
2. View Student
3. View All Students
4. Update Student
5. Delete Student
6. Search Students
7. Exit
========================================
Enter your choice:
```

Student records are stored in:

```text
data/students.csv
```

The application creates the CSV file and its header when the configured file does not already exist.

## Example Workflow

### Add a student

```text
Enter your choice: 1
Enter Student ID: STU003
Enter First Name: Manish
Enter Last Name: Solanki
Enter Email: manish@example.com
Enter Phone: 9876543210
Enter Age: 21
Enter Course: Python
Enter GPA: 8.4

Student 'STU003' added successfully.
```

Invalid input is handled without crashing the application. For example:

```text
Enter Age: abc
Error: Please enter a valid integer.
```

Domain validation errors are reported with meaningful messages, such as:

```text
Error: Student ID must follow the format STU001.
```

## Validation Rules

The current validators enforce the following rules:

| Field      | Current rule                                           |
| ---------- | ------------------------------------------------------ |
| Student ID | `STU` followed by exactly 3 digits                   |
| Email      | Valid email-like format; consecutive dots are rejected |
| Phone      | Exactly 10 digits and starts with 6–9                 |
| Age        | Integer from 16 through 100                            |
| GPA        | Numeric value from 0.0 through 10.0                    |

## Testing

The project contains **54 test functions** covering validators, the CSV repository, and the student service. Several validator tests use `pytest.mark.parametrize`, so the number of collected test cases is higher than the number of test functions.

Run the complete test suite with:

```powershell
pytest
```

Run tests in quiet mode:

```powershell
pytest -q
```

The test suite uses a fake repository for service-level tests so that business logic can be tested without depending on the real CSV file.

## Code Quality

The project is configured with:

### Black

```powershell
black --check .
```

Format the code when needed:

```powershell
black .
```

### Ruff

```powershell
ruff check .
```

### Mypy

```powershell
mypy .
```

Mypy is configured in strict mode:

```toml
[tool.mypy]
strict = true
```

## Design Principles Demonstrated

### Single Responsibility Principle

Components have focused responsibilities:

- CLI classes handle interaction.
- Services handle application/business operations.
- Validators handle validation.
- Repositories handle persistence.
- Domain models represent domain data.
- Logging configuration handles application-wide logging setup.

### Dependency Inversion Principle

`StudentService` receives a `StudentRepository` abstraction through dependency injection rather than constructing the CSV repository internally.

```python
service = StudentService(
    repository=repository,
    validator=validator,
)
```

This improves testability and keeps the service independent of the concrete storage technology.

### Separation of Concerns

User interaction, business logic, validation, persistence, exception definitions, and logging are separated into dedicated modules.

### Repository Pattern

Persistence operations are exposed through an abstraction, allowing the storage implementation to evolve independently from the service layer.

### Dependency Injection

Dependencies such as the repository and validator are passed into services and dependencies are assembled in the application entry point.

## Current Scope

The current implementation focuses on the student management workflow, CSV persistence, validation, logging, exception handling, automated testing, and code-quality tooling.

The following items from the original project roadmap are **not currently implemented** and are therefore not presented as completed features:

- Admin authentication
- Password hashing
- Role-based access
- Statistical reporting
- SQLite/PostgreSQL/MongoDB persistence implementations
- Rich/Typer-based CLI
- Excel/OpenPyXL storage

## Future Improvements

Potential future iterations could add:

- Authentication and role-based authorization
- Password hashing with a dedicated authentication component
- Statistical student reports
- SQLite persistence
- PostgreSQL persistence
- Excel import/export
- Rich-based terminal presentation
- More comprehensive CLI integration tests
- CI/CD with GitHub Actions
- Coverage reporting
- Configuration management for environment-specific settings
- More robust persistence error handling and transactional behavior

These are future enhancements, not current application features.

## Project Goals

This project was built as a practical exercise in moving from procedural CRUD development toward maintainable Python application architecture.

The main learning goals are:

- Designing applications around responsibilities rather than files
- Applying object-oriented design in a real application
- Separating business logic from presentation
- Designing replaceable persistence layers
- Writing testable services
- Creating meaningful domain-specific exceptions
- Introducing application-wide logging
- Using static analysis and automated formatting/linting
- Maintaining a professional Python project structure

## License

No license has currently been specified for this project.
