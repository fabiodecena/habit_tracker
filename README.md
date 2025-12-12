# Habit Tracker CLI

A professional Python command-line application to track and analyze your habits, built with clean **MVC architecture** and **business logic separation**.

![Python](https://img.shields.io/badge/Python-3.7%2B-blue)
![Architecture](https://img.shields.io/badge/Architecture-MVC-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## 📑 Table of Contents

- [Features](#-features)
- [Architecture](#️-architecture)
  - [Directory Structure](#directory-structure)
  - [Architecture Layers Explained](#-architecture-layers-explained)
  - [Data Flow](#-data-flow)
- [Getting Started](#-getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Usage](#-usage)
  - [Interactive Mode](#interactive-mode-recommended)
  - [Direct CLI Commands](#direct-cli-commands)
- [Menu Options](#-menu-options)
- [Running Tests](#-running-tests)
- [Database Schema](#️-database-schema)
- [Configuration](#️-configuration)
- [Key Features in Detail](#-key-features-in-detail)
  - [Soft Delete (Archive)](#1-soft-delete-archive)
  - [UUID-based Identification](#2-uuid-based-identification)
  - [Streak Calculation Algorithm](#3-streak-calculation-algorithm)
  - [Input Validation](#4-input-validation)
  - [Completion Notes](#5-completion-notes)
  - [Completion Table & History](#6-completion-table--history)
  - [Functional Programming](#7-functional-programming)
- [Example Workflow](#-example-workflow)
- [Benefits of This Architecture](#-benefits-of-this-architecture)
- [Understanding the Code Flow](#-understanding-the-code-flow)
- [Dependencies](#-dependencies)
- [Learning from This Project](#-learning-from-this-project)
- [Contributing](#-contributing)
- [License](#-license)
- [Support](#-support)

---

## ✨ Features

- ✅ **Create, edit, and delete habits** with validation
- ✅ **Track daily and weekly habits** with optional notes
- ✅ **Add and edit completion notes** for each check-off
- ✅ **Calculate longest streaks** with smart date normalization
- ✅ **Filter habits by periodicity** (daily/weekly)
- ✅ **Soft delete support** - archive habits instead of deleting
- ✅ **Completion table** - comprehensive overview with statistics
- ✅ **Detailed completion history** - view all check-offs with timestamps and notes
- ✅ **Beautiful CLI interface** powered by Rich
- ✅ **Pre-seeded sample data** for quick start
- ✅ **UUID-based unique identifiers** for all entities
- ✅ **Comprehensive test suite**
- ✅ **Functional programming** approach for data sorting

---

## 🏗️ Architecture

This application follows **professional software engineering practices** with a clean separation of concerns:

### Directory Structure

```
📁 habit_tracker/
│
├── 📂 models/                    # Pure data models (DTOs)
│   ├── __init__.py
│   ├── habit.py                  # Habit entity (dataclass)
│   └── tracker.py                # TrackerEvent entity (dataclass)
│
├── 📂 repositories/              # Data Access Layer (DAL)
│   ├── __init__.py
│   ├── habit_repository.py       # CRUD operations for habits
│   └── tracker_repository.py     # CRUD operations for tracker events
│
├── 📂 services/                  # Business Logic Layer (BLL)
│   ├── __init__.py
│   ├── habit_service.py          # Habit business logic & validation
│   ├── tracker_service.py        # Tracking business logic
│   └── analytics_service.py      # Analytics & streak calculations
│
├── 📂 views/                     # Presentation Layer
│   ├── __init__. py
│   ├── console_view.py           # All console I/O operations
│   └── formatters.py             # Table and text formatting
│
├── 📂 controllers/               # Application Logic Layer
│   ├── __init__. py
│   ├── habit_controller.py       # Coordinates habit operations
│   ├── tracker_controller.py     # Coordinates tracking operations
│   ├── analytics_controller.py   # Coordinates analytics operations
│   ├── completion_controller.py  # Coordinates completion table operations
│   └── menu_controller.py        # Main menu navigation
│
├── 📂 database/                  # Database Infrastructure
│   ├── __init__.py
│   └── connection.py             # Database connection & schema
│
├── 📂 utils/                     # Utilities
│   ├── __init__. py
│   └── seed_data.py              # Database seeding
│
├── 📂 tests/                     # Test Suite
│   └── test_project.py           # Unit tests
│
├── cli.py                        # CLI entry point (Click commands)
├── main.py                       # Application entry point
├── config.py                     # Configuration settings
├── requirements.txt              # Dependencies
└── README.md                     # This file
```

---

## 🎯 Architecture Layers Explained

### 1️⃣ **Models Layer** (Pure Data)
**Responsibility**: Define data structures with no business logic

**Files**:  `models/habit.py`, `models/tracker.py`

- Pure Python dataclasses
- No database operations
- No validation logic
- Just data structure definitions

Example:
```python
@dataclass
class Habit: 
    name: str
    periodicity: str
    habit_id: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    comments: str = ""
    is_active: bool = True
```

### 2️⃣ **Repositories Layer** (Data Access)
**Responsibility**: Handle all database operations (CRUD)

**Files**: `repositories/habit_repository.py`, `repositories/tracker_repository.py`

- All SQL queries live here
- No business logic
- No validation
- Just database CRUD operations

Example:
```python
class HabitRepository: 
    def save(self, habit: Habit) -> bool:
        # INSERT INTO habits ... 
        
    def find_by_name(self, name: str) -> Optional[Habit]:
        # SELECT * FROM habits WHERE name = ? 
```

### 3️⃣ **Services Layer** (Business Logic)
**Responsibility**: Implement business rules, validation, and complex operations

**Files**: `services/habit_service.py`, `services/tracker_service.py`, `services/analytics_service.py`

- All validation logic
- Business rules
- Complex calculations (streaks)
- Returns `Tuple[bool, str]` for operations

Example:
```python
class HabitService:
    def create_habit(self, name: str, periodicity: str) -> Tuple[bool, str]:
        # Validation
        if not name or not name.strip():
            return False, "Habit name cannot be empty"
        
        # Business logic
        # ...
        return True, "Habit created successfully"
```

### 4️⃣ **Controllers Layer** (Coordination)
**Responsibility**:  Coordinate between services and views

**Files**: `controllers/habit_controller.py`, `controllers/tracker_controller.py`, `controllers/analytics_controller.py`, `controllers/completion_controller.py`, `controllers/menu_controller.py`

- No business logic
- No database operations
- Just orchestration

Example:
```python
class HabitController:
    def create_habit(self):
        name = self.view. get_habit_name()
        periodicity = self.view.get_periodicity()
        
        success, message = self.service.create_habit(name, periodicity)
        
        if success: 
            self.view.show_habit_created(name)
        else:
            self.view. show_error(message)
```

### 5️⃣ **Views Layer** (Presentation)
**Responsibility**: Handle all user interface operations

**Files**: `views/console_view.py`, `views/formatters.py`

- All `console.print()` statements
- All `console.input()` statements
- Rich table formatting
- No business logic

Example:
```python
class ConsoleView:
    def show_menu(self):
        # Display menu
        
    def get_habit_name(self) -> str:
        return self.console.input("Enter habit name: ")
        
    def show_habit_created(self, name: str):
        self.console.print(f"✅ Habit '{name}' created!", style="green")
```

---

## 📊 Data Flow

```
User Input
    ↓
[View] - ConsoleView.get_habit_name()
    ↓
[Controller] - HabitController.create_habit()
    ↓
[Service] - HabitService.create_habit() → Validates input
    ↓
[Repository] - HabitRepository.save() → Executes SQL
    ↓
[Database] - SQLite stores data
    ↓
[Repository] - Returns success/failure
    ↓
[Service] - Returns (bool, message)
    ↓
[Controller] - Decides what to show
    ↓
[View] - ConsoleView.show_habit_created()
```

---

## 🚀 Getting Started

### Prerequisites

- **Python 3.7 or higher**
- **pip** (Python package manager)

### Installation

1. **Clone or download the repository**
   ```bash
   git clone https://github.com/fabiodecena/habit_tracker.git
   cd habit_tracker
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python main.py
   ```
   Or: 
   ```bash
   python cli.py
   ```

---

## 💻 Usage

### Interactive Mode (Recommended)

Run without arguments to enter the beautiful interactive menu:

```bash
python main.py
```

**You'll see:**
```
✨ HABIT TRACKER ✨

1.   ➕ Create a new habit
2.  ❌ Delete a habit
3.  ✅ Check-off a habit (Complete task)
4.  📝 Edit a habit
5.  📋 List all habits
6.  🔍 List habits by periodicity
7.  🏆 Show longest streak of all habits
8.  🎯 Show longest streak for a specific habit
9.  📊 View completion table
10. ✏️ Edit completion notes
11. 👋 Exit

Enter your choice (1-11): _
```

---

### Direct CLI Commands

#### Create a New Habit
```bash
python cli.py create "Exercise" daily
python cli.py create "Clean House" weekly
```

#### Check Off a Habit
```bash
# Simple check-off
python cli.py checkoff "Exercise"

# With notes
python cli.py checkoff "Exercise" --notes "30 minutes cardio"
```

#### List All Habits
```bash
python cli.py list
```

Output:
```
📋 Currently tracked habits:

Name              Periodicity
☀️  Drink Water   daily
☀️  Read Book     daily
📆 Clean House    weekly
```

#### Filter Habits by Periodicity
```bash
python cli.py filter daily
python cli.py filter weekly
```

#### Edit a Habit
```bash
# Change name only
python cli.py edit "Exercise" --new-name "Workout"

# Change periodicity only
python cli.py edit "Exercise" --periodicity weekly

# Change both
python cli.py edit "Exercise" --new-name "Workout" --periodicity weekly
```

#### Delete a Habit
```bash
python cli.py delete "Exercise"
```

#### View Longest Streaks
```bash
# Show the habit with the longest streak
python cli. py champion

# Show streak for a specific habit
python cli. py streak "Exercise"
```

---

## 📋 Menu Options

| Option | Feature | Description |
|--------|---------|-------------|
| **1** | ➕ Create a new habit | Add a new daily or weekly habit |
| **2** | ❌ Delete a habit | Remove a habit (soft delete by default) |
| **3** | ✅ Check-off a habit | Mark a habit as completed with optional notes |
| **4** | 📝 Edit a habit | Change habit name or periodicity |
| **5** | 📋 List all habits | Display all active habits in a table |
| **6** | 🔍 List habits by periodicity | Filter habits by daily or weekly |
| **7** | 🏆 Show longest streak of all habits | Find the champion habit |
| **8** | 🎯 Show longest streak for a specific habit | View streak for a selected habit |
| **9** | 📊 View completion table | Comprehensive overview with statistics and detailed history |
| **10** | ✏️ Edit completion notes | Update notes for existing check-offs |
| **11** | 👋 Exit | Close the application |

---

## 🧪 Running Tests

```bash
# Run all tests
python -m unittest tests/test_project.py

# Run with verbose output
python -m unittest tests/test_project.py -v

# Run from tests directory
cd tests
python test_project.py
```

**Test Coverage:**
- ✅ Habit creation and validation
- ✅ Habit updates
- ✅ Soft delete and hard delete
- ✅ Check-off functionality
- ✅ Streak calculations (daily and weekly)
- ✅ Broken streak detection
- ✅ Filtering by periodicity
- ✅ Input validation (empty names, invalid periodicity, duplicates)
- ✅ Edge cases (future dates, non-existent habits)

---

## 🗄️ Database Schema

### Habits Table
```sql
CREATE TABLE habits (
    habit_id TEXT PRIMARY KEY,        -- UUID
    name TEXT NOT NULL,                -- Habit name
    periodicity TEXT NOT NULL,         -- 'daily' or 'weekly'
    created_at TEXT NOT NULL,          -- ISO format datetime
    updated_at TEXT NOT NULL,          -- ISO format datetime
    comments TEXT DEFAULT '',          -- User notes
    is_active INTEGER DEFAULT 1        -- Soft delete flag (1=active, 0=inactive)
);
```

### Tracker Table
```sql
CREATE TABLE tracker (
    event_id TEXT PRIMARY KEY,         -- UUID
    habit_id TEXT NOT NULL,            -- Foreign key to habits
    checked_at TEXT NOT NULL,          -- ISO format datetime
    notes TEXT DEFAULT '',             -- Notes for this completion
    FOREIGN KEY (habit_id) REFERENCES habits(habit_id) ON DELETE CASCADE
);
```

**Indexes** (for performance):
```sql
CREATE INDEX idx_habit_name ON habits(name);
CREATE INDEX idx_tracker_habit ON tracker(habit_id);
CREATE INDEX idx_tracker_date ON tracker(checked_at);
```

---

## ⚙️ Configuration

Edit `config.py` to customize settings:

```python
class Config:
    DATABASE_NAME = "main.db"
    DEFAULT_PERIODICITY_OPTIONS = ['daily', 'weekly']
    SEED_WEEKS = 4
    SEED_SUCCESS_RATE = 0.8  # 80% completion rate for seed data
    
    SEED_HABITS = [
        ("Drink Water", "daily"),
        ("Read Book", "daily"),
        ("Exercise", "daily"),
        ("Clean House", "weekly"),
        ("Meditate", "weekly")
    ]
```

---

## 🎨 Key Features in Detail

### 1. Soft Delete (Archive)
By default, habits are marked as inactive rather than permanently deleted: 

```python
# Soft delete (default) - habit is archived
success, message = habit_service.delete_habit("Exercise", soft_delete=True)

# Hard delete - permanently removes from database
success, message = habit_service.delete_habit("Exercise", soft_delete=False)
```

### 2. UUID-based Identification
Every habit and tracker event has a unique UUID: 
```python
Habit(
    habit_id='550e8400-e29b-41d4-a716-446655440000',
    name='Exercise',
    ... 
)
```

Benefits:
- No naming conflicts
- Better for future features (sync, API, etc.)
- Industry-standard approach

### 3. Streak Calculation Algorithm
Smart streak calculation that handles: 

**Daily Habits:**
- Checks for consecutive days
- Example:  Completed on Jan 1, 2, 3, 5 → Longest streak = 3

**Weekly Habits:**
- Normalizes to Monday of each week
- Example: Completed on Jan 1 (Mon), Jan 8 (Mon), Jan 15 (Mon) → Streak = 3

### 4. Input Validation
All user input is validated in the service layer: 

```python
# Empty name
create_habit("", "daily")
→ (False, "Habit name cannot be empty")

# Invalid periodicity
create_habit("Exercise", "monthly")
→ (False, "Periodicity must be one of ['daily', 'weekly']")

# Duplicate name
create_habit("Exercise", "daily")  # Already exists
→ (False, "Habit 'Exercise' already exists")

# Future date
check_off_habit("Exercise", datetime(2099, 1, 1))
→ (False, "Cannot check off a habit in the future")
```

### 5. Completion Notes
Add context to each habit completion:

**When checking off:**
```bash
✅ Check-off a habit

Current habits:
  1. ☀️ Play Music (daily)

Enter the number of the habit to check-off:  1

Do you want to add notes for this completion? (y/n): y
Enter notes (press Enter to skip): Amazing 30-minute session! 

✅ Habit 'Play Music' marked as done!
   📝 Notes: Amazing 30-minute session!
```

**Edit existing notes (Option 10):**
```bash
✏️  Edit Completion Notes

[Select habit → Select completion → Enter new notes]

✅ Notes updated successfully!
```

### 6. Completion Table & History
Comprehensive visualization of your habits (Option 9):

**Summary Table:**
```
📊 Habit Completion Summary

╭───┬────────────────┬─────────────┬────────────┬────────────┬────────┬───────┬────────────────╮
│ # │ Habit Name     │ Periodicity │ Created    │ Last Done  │ Streak │ Total │ Notes          │
├───┼────────────────┼─────────────┼────────────┼────────────┼────────┼───────┼────────────────┤
│ 1 │ Play Music     │   Daily     │ 2025-01-15 │ 2025-01-20 │      5 │    15 │ Great session! │
│ 2 │ Skin Care      │   Daily     │ 2025-01-16 │ 2025-01-20 │      3 │    10 │                │
│ 3 │ Finance Check  │   Weekly    │ 2025-01-10 │ 2025-01-15 │      2 │     3 │                │
╰───┴────────────────┴─────────────┴────────────┴────────────┴────────┴───────┴────────────────╯

Enter the number of a habit to view detailed history (or 'q' to quit): _
```

**Detailed History (after selecting a habit):**
```
☀️ Play Music (daily)

╭──────────── Habit Statistics ────────────╮
│ Created: 2025-01-15 10:30                │
│ Total Completions: 15                    │
│ Current Streak: 5                        │
│ Longest Streak: 7                        │
╰──────────────────────────────────────────╯

📅 Completion History: 

   #  Date        Time      Notes
────────────────────────────────────────────
   1  2025-01-15  10:30:00  Started the habit
   2  2025-01-16  09:15:00  Piano practice
   3  2025-01-17  10:00:00  Amazing 30-minute session!
  ... 
```

### 7. Functional Programming
Data sorting uses functional programming approach:

```python
# Repositories return data without sorting
habits = map(Habit.from_tuple, results)

# Filter inactive habits if needed
if not include_inactive:
    habits = filter(lambda h: h.is_active, habits)

# Sort using functional key
def get_sort_key(habit:  Habit) -> tuple:
    periodicity_map = {'daily': 1, 'weekly': 2}
    periodicity_priority = periodicity_map.get(habit.periodicity, 3)
    creation_time = -habit.created_at.timestamp()
    return (periodicity_priority, creation_time)

return sorted(habits, key=get_sort_key)
```

Benefits:
- More flexible than SQL ORDER BY
- Easier to test
- Clean separation of concerns

---

## 🔍 Example Workflow

Here's a complete workflow from start to finish:

```bash
# 1. Start the application (auto-seeds with 5 sample habits)
python main.py

# 2. Create a new habit
python cli.py create "Morning Run" daily

# 3. Check it off with notes
python cli.py checkoff "Morning Run" --notes "5km in 30 minutes"

# Or use interactive mode: 
# Option 3 → Select habit → Add notes

# 4. Do it again the next day (building a streak!)
python cli.py checkoff "Morning Run" --notes "Felt great today!"

# 5. Check your streak
python cli.py streak "Morning Run"
# Output: 🎯 Longest streak for 'Morning Run': 2

# 6. View completion table
# Option 9 → See all habits with statistics
# Select a habit number → View detailed history

# 7. Edit completion notes if needed
# Option 10 → Select habit → Select completion → Edit notes

# 8. See all your habits
python cli.py list

# 9. Edit a habit
python cli.py edit "Morning Run" --new-name "Daily Run"

# 10. Find the champion habit
python cli.py champion
# Output: 🏆 Champion: 'Daily Run' with streak of 5! 
```

---

## 🏆 Benefits of This Architecture

| Benefit | Description | Example |
|---------|-------------|---------|
| **Maintainability** | Each layer has one responsibility | View only handles UI, Service only handles logic |
| **Testability** | Can test each layer independently | Mock repository in service tests |
| **Flexibility** | Easy to change implementations | Swap SQLite for PostgreSQL by changing repository |
| **Reusability** | Services can be used anywhere | Same service for CLI, API, or GUI |
| **Validation Centralized** | All business rules in one place | All validation in `HabitService` |
| **Separation of Concerns** | UI, logic, and data are separate | Change UI without touching business logic |

---

## 📚 Understanding the Code Flow

### Example: Creating a Habit

**1. User runs command:**
```bash
python cli.py create "Exercise" daily
```

**2. CLI entry point (`cli.py`):**
```python
@cli.command()
def create(ctx, name, periodicity):
    view = ConsoleView()
    service = HabitService(db)
    
    success, message = service.create_habit(name, periodicity)
    
    if success: 
        view.show_habit_created(name)
```

**3. Service validates and processes (`services/habit_service.py`):**
```python
def create_habit(self, name, periodicity):
    # Validation
    if not name. strip():
        return False, "Name cannot be empty"
    
    # Check duplicates
    if self.repository. find_by_name(name):
        return False, "Already exists"
    
    # Create model
    habit = Habit(name=name, periodicity=periodicity)
    
    # Save via repository
    success = self.repository.save(habit)
    
    return success, "Created successfully"
```

**4. Repository saves to database (`repositories/habit_repository.py`):**
```python
def save(self, habit:  Habit) -> bool:
    cur. execute(
        "INSERT INTO habits VALUES (?, ?, ... )",
        (habit.habit_id, habit.name, ...)
    )
    con.commit()
    return True
```

**5. View shows result (`views/console_view.py`):**
```python
def show_habit_created(self, name:  str):
    self.console.print(
        f"✅ Habit '{name}' created! ",
        style="green"
    )
```

---

## 🛠️ Dependencies

### `requirements.txt`
```
click>=8.0.0
rich>=13.0.0
```

**Why these libraries? **
- **click**: Professional CLI framework with command parsing, options, and arguments
- **rich**: Beautiful terminal formatting with colors, tables, and panels

---

## 📖 Learning from This Project

This project demonstrates professional software engineering practices:

### Design Patterns Used
- ✅ **MVC (Model-View-Controller)** - Separation of concerns
- ✅ **Repository Pattern** - Data access abstraction
- ✅ **Service Layer Pattern** - Business logic centralization
- ✅ **Data Transfer Objects (DTOs)** - Pure data models

### SOLID Principles
- ✅ **Single Responsibility** - Each class has one job
- ✅ **Open/Closed** - Open for extension, closed for modification
- ✅ **Dependency Inversion** - Depend on abstractions, not concretions

### Best Practices
- ✅ Type hints throughout
- ✅ Docstrings for all public methods
- ✅ Comprehensive error handling
- ✅ Input validation at service layer
- ✅ Unit tests for critical functionality
- ✅ Clear separation of concerns
- ✅ Functional programming for data transformation

### What You'll Learn

By studying this codebase, you'll learn: 

1. **How to structure a professional Python application**
2. **Separation of concerns** - Why it matters and how to do it
3. **Service layer pattern** - Centralizing business logic
4. **Repository pattern** - Abstracting data access
5. **Clean architecture** - Making code maintainable
6. **Type hints and dataclasses** - Modern Python features
7. **Click framework** - Building professional CLIs
8. **Rich library** - Beautiful terminal UIs
9. **Unit testing** - Testing layered applications
10. **SQLite with Python** - Database operations
11. **Functional programming** - Using `map`, `filter`, `sorted`

---

## 🤝 Contributing

Contributions are welcome! Please follow these guidelines:

1. **Maintain the architecture** - Keep layers separated
2. **No business logic in models or repositories** - Put it in services
3. **Add tests** - Test new features
4. **Follow the pattern** - Look at existing code for examples
5. **Update docs** - Update README if adding major features

---

## 📄 License

MIT License - Free to use for learning or personal projects.

---

## 📞 Support

- **Issues**: Open an issue on GitHub
- **Questions**: Review the code examples above
- **Examples**: Check `tests/test_project.py` for usage patterns

---

**Built with ❤️ using clean architecture principles** 🚀

---

## 🎓 Additional Resources

- [Python Dataclasses Documentation](https://docs.python.org/3/library/dataclasses.html)
- [Click Documentation](https://click.palletsprojects.com/)
- [Rich Documentation](https://rich.readthedocs.io/)
- [SQLite Documentation](https://www.sqlite.org/docs.html)
- [MVC Pattern](https://en.wikipedia.org/wiki/Model%E2%80%93view%E2%80%93controller)
- [Repository Pattern](https://martinfowler.com/eaaCatalog/repository.html)
- [Service Layer Pattern](https://martinfowler.com/eaaCatalog/serviceLayer. html)