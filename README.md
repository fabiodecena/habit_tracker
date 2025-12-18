# Habit Tracker CLI

A professional Python command-line application to track and analyze your habits, built with clean **MVC architecture** and **business logic separation** using **functional programming paradigms**.

![Python](https://img.shields.io/badge/Python-3.7%2B-blue)
![Architecture](https://img.shields.io/badge/Architecture-MVC-green)
![License](https://img.shields.io/badge/License-MIT-yellow)
![Code Style](https://img.shields.io/badge/Code%20Style-Functional-purple)

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
- [Key Features in Detail](#-key-features-in-detail)
  - [Habit Descriptions](#1-habit-descriptions)
  - [Completion Notes](#2-completion-notes)
  - [Edit Completion Notes](#3-edit-completion-notes)
  - [Comprehensive Completion Table](#4-comprehensive-completion-table)
  - [Soft Delete (Archive)](#5-soft-delete-archive)
  - [UUID-based Identification](#6-uuid-based-identification)
  - [Streak Calculation Algorithm](#7-streak-calculation-algorithm)
  - [Input Validation](#8-input-validation)
  - [Functional Programming](#9-functional-programming)
- [Analytics Module](#-analytics-module)
  - [Required Functionality](#required-functionality)
  - [Implementation with Functional Programming](#implementation-with-functional-programming)
- [Example Workflows](#-example-workflows)
- [Running Tests](#-running-tests)
- [Database Schema](#️-database-schema)
- [Configuration](#️-configuration)
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
- ✅ **Add habit descriptions** when creating or editing habits
- ✅ **Track daily and weekly habits** with optional notes
- ✅ **Add and edit completion notes** for each check-off
- ✅ **Calculate longest streaks** with smart date normalization
- ✅ **Filter habits by periodicity** (daily/weekly)
- ✅ **Soft delete support** - archive habits instead of deleting
- ✅ **Comprehensive completion table** - overview with statistics
- ✅ **Detailed completion history** - view all check-offs with timestamps and notes
- ✅ **Beautiful CLI interface** powered by Rich with centered, aligned tables
- ✅ **Pre-seeded sample data** for quick start with descriptions
- ✅ **UUID-based unique identifiers** for all entities
- ✅ **Comprehensive test suite** with functional programming tests
- ✅ **Functional programming** approach throughout analytics module

---

## 🏗️ Architecture

This application follows **professional software engineering practices** with a clean separation of concerns and **functional programming paradigms** in the analytics layer. 

### Directory Structure

```
📁 habit_tracker/
│
├── 📂 models/                    # Pure data models (DTOs)
│   ├── __init__.py
│   ├── habit.py                  # Habit entity (dataclass with description)
│   └── tracker.py                # TrackerEvent entity (dataclass with notes)
│
├── 📂 repositories/              # Data Access Layer (DAL)
│   ├── __init__.py
│   ├── habit_repository.py       # CRUD operations for habits (functional sorting)
│   └── tracker_repository.py     # CRUD operations for tracker events
│
├── 📂 services/                  # Business Logic Layer (BLL)
│   ├── __init__.py
│   ├── habit_service. py          # Habit business logic & validation
│   ├── tracker_service.py        # Tracking business logic
│   └── analytics_service.py      # Analytics with functional programming
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
│   └── seed_data.py              # Database seeding with descriptions
│
├── 📂 tests/                     # Test Suite
│   └── test_project.py           # Unit tests including functional tests
│
├── cli. py                        # CLI entry point (Click commands)
├── main.py                       # Application entry point
├── config.py                     # Configuration settings with seed data
├── requirements.txt              # Dependencies (click, rich)
└── README.md                     # This file
```

---

## 🎯 Architecture Layers Explained

### 1️⃣ **Models Layer** (Pure Data)
**Responsibility**:  Define data structures with no business logic

**Files**:  `models/habit.py`, `models/tracker.py`

- Pure Python dataclasses
- No database operations
- No validation logic
- Just data structure definitions

```python
@dataclass
class Habit: 
    name: str
    periodicity: str
    habit_id: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    description: str = ""              # NEW:  Habit descriptions
    is_active: bool = True
```

```python
@dataclass
class TrackerEvent:
    habit_id: str
    checked_at: datetime
    event_id: Optional[str] = None
    notes: str = ""                 # Completion notes
```

### 2️⃣ **Repositories Layer** (Data Access)
**Responsibility**: Handle all database operations (CRUD) with functional data transformation

**Files**: `repositories/habit_repository.py`, `repositories/tracker_repository.py`

- All SQL queries live here
- Functional programming for data transformation
- Uses `map()`, `filter()`, `sorted()` for data processing

```python
def find_all(self, include_inactive: bool = False) -> List[Habit]:
    # ... SQL query ... 
    
    # Functional approach: map, filter, sort
    habits = map(Habit.from_tuple, results)
    
    if not include_inactive:
        habits = filter(lambda h: h.is_active, habits)
    
    def get_sort_key(habit: Habit) -> tuple:
        periodicity_map = {'daily': 1, 'weekly': 2}
        periodicity_priority = periodicity_map.get(habit.periodicity, 3)
        creation_time = -habit.created_at.timestamp()
        return (periodicity_priority, creation_time)
    
    return sorted(habits, key=get_sort_key)
```

### 3️⃣ **Services Layer** (Business Logic)
**Responsibility**: Implement business rules, validation, and analytics using functional programming

**Files**: `services/habit_service.py`, `services/tracker_service.py`, `services/analytics_service.py`

- All validation logic
- Business rules
- **Functional programming** for analytics
- Complex calculations (streaks) using functional paradigm

```python
def get_longest_streak_all_habits(self) -> Tuple[str, int]:
    """Uses functional programming to find longest streak."""
    habits = self.habit_repo.find_all()
    
    # Functional approach: map to (name, streak) tuples
    streaks = [(h.name, self.calculate_longest_streak(h. name)) for h in habits]
    
    # Find max using functional key
    return max(streaks, key=lambda x: x[1]) if streaks else ("", 0)
```

### 4️⃣ **Controllers Layer** (Coordination)
**Responsibility**: Coordinate between services and views

**Files**: `controllers/habit_controller.py`, `controllers/tracker_controller.py`, `controllers/analytics_controller.py`, `controllers/completion_controller.py`, `controllers/menu_controller.py`

- No business logic
- No database operations
- Just orchestration
- Handles user interactions with numbered selection menus

### 5️⃣ **Views Layer** (Presentation)
**Responsibility**: Handle all user interface operations

**Files**: `views/console_view.py`, `views/formatters.py`

- All `console.print()` statements
- All `console.input()` statements
- Rich table formatting with centered headers
- No business logic

---

## 📊 Data Flow

```
User Input
    ↓
[View] - ConsoleView.get_habit_name() + get_habit_description()
    ↓
[Controller] - HabitController.create_habit()
    ↓
[Service] - HabitService.create_habit() → Validates input
    ↓
[Repository] - HabitRepository.save() → Executes SQL
    ↓
[Database] - SQLite stores data with description
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

1. **Clone the repository**
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

 1.  ➕  Create a new habit
 2.  ❌  Delete a habit
 3.  ✅  Check-off a habit (Complete task)
 4.  📝  Edit a habit
 5.  📋  List all habits
 6.  🔍  List habits by periodicity
 7.  🏆  Show longest streak of all habits
 8.  🎯  Show longest streak for a specific habit
 9.  📊  View completion table
10.  📝  Edit completion notes
11.  👋  Exit

Enter your choice (1-11): _
```

---

### Direct CLI Commands

#### Create a New Habit
```bash
# Simple creation
python cli.py create "Exercise" daily

# With description
python cli. py create "Morning Run" daily --description "5km jog in the park to start the day fresh"
```

#### Check Off a Habit
```bash
# Simple check-off
python cli.py checkoff "Exercise"

# With notes
python cli.py checkoff "Exercise" --notes "30 minutes cardio, felt great!"
```

#### List All Habits
```bash
python cli.py list
```

**Output:**
```
📋 Currently tracked habits: 

╭─────┬────────────────────┬──────────────┬──────────────────────────────────────────────╮
│     │    Habit Name      │ Periodicity  │                 Description                  │
├─────┼────────────────────┼──────────────┼──────────────────────────────────────────────┤
│ 📅  │ Play Music         │    Daily     │ Practice an instrument for at least 15–30...  │
│ 📅  │ Skin Care          │    Daily     │ Complete your skincare routine               │
│ 📅  │ Read Journal       │    Daily     │ Read a journal (20-35 minutes)               │
│ 📆  │ Water Plants       │   Weekly     │ Water plants and check soil moisture/leaves  │
│ 📆  │ Finance Check      │   Weekly     │ Review spending and update your budget/acc... │
╰─────┴────────────────────┴──────────────┴──────────────────────────────────────────────╯
```

#### Filter Habits by Periodicity
```bash
python cli.py filter daily
python cli.py filter weekly
```

#### Edit a Habit
```bash
# Interactive edit (recommended)
# Option 4 in menu → Select habit number → Edit name/periodicity/description

# CLI edit
python cli.py edit "Exercise" --new-name "Workout" --periodicity weekly
```

#### Delete a Habit
```bash
python cli.py delete "Exercise"
```

#### View Longest Streaks
```bash
# Show the habit with the longest streak (analytics)
python cli.py champion

# Show streak for a specific habit (analytics)
python cli.py streak "Exercise"
```

---

## 📋 Menu Options

| Option | Icon | Feature | Description |
|--------|------|---------|-------------|
| **1** | ➕ | Create a new habit | Add a new daily or weekly habit with optional description |
| **2** | ❌ | Delete a habit | Remove a habit (soft delete by default, with confirmation) |
| **3** | ✅ | Check-off a habit | Mark a habit as completed with optional notes |
| **4** | 📝 | Edit a habit | Change habit name, periodicity, or description |
| **5** | 📋 | List all habits | Display all active habits with icon, name, periodicity, and description |
| **6** | 🔍 | List habits by periodicity | Filter habits by daily or weekly with numbered selection |
| **7** | 🏆 | Show longest streak of all habits | Find the champion habit (analytics - functional programming) |
| **8** | 🎯 | Show longest streak for a specific habit | View streak for a selected habit (analytics - functional programming) |
| **9** | 📊 | View completion table | Comprehensive overview with statistics and detailed history |
| **10** | ✍️ | Edit completion notes | Update notes for existing check-offs |
| **11** | 👋 | Exit | Close the application |

---

## 🎨 Key Features in Detail

### 1. Habit Descriptions

Add meaningful descriptions to your habits for better context. 

**When creating:**
```
✨ Create a new habit

Enter habit name:  Morning Meditation
Enter periodicity (daily/weekly): daily

Do you want to add a description/comment for this habit? (y/n): y
Enter a short description (press Enter to skip): 10 minutes of mindfulness to start the day

✅ Habit 'Morning Meditation' created! 
   💬 Description: 10 minutes of mindfulness to start the day
```

**When editing:**
```
✏️ Edit a habit

Editing:  Morning Meditation (daily)
Current description: 10 minutes of mindfulness to start the day

New description (current:  10 minutes of mindfulness to start the day): 15 minutes meditation with breathing exercises

✅ Habit updated successfully!
```

### 2. Completion Notes

Add context to each habit completion: 

```
✅ Check-off a habit

Current habits:
  1. 📅 Play Music (daily)

Enter the number of the habit to check-off (or 'q' to quit): 1

Do you want to add notes for this completion? (y/n): y
Enter notes (press Enter to skip): Practiced piano for 45 minutes - learning new song

✅ Habit 'Play Music' marked as done!
   📝 Notes:  Practiced piano for 45 minutes - learning new song
```

### 3. Edit Completion Notes

Update notes for past completions:

```
✍️ Edit Completion Notes

[Select habit → View completion history → Select completion number]

Current notes: Practiced piano for 45 minutes

Enter new notes (press Enter to clear): Practiced piano for 45 minutes - mastered chorus section! 

✅ Notes updated successfully!
```

### 4. Comprehensive Completion Table

View all your habits with statistics (Option 9):

**Summary Table:**
```
📊 Habit Completion Summary

╭───┬────────────────┬─────────────┬────────────┬────────────┬────────┬───────┬──────────────────╮
│ # │ Habit Name     │ Periodicity │ Created    │ Last Done  │ Streak │ Total │ Notes            │
├───┼────────────────┼─────────────┼────────────┼────────────┼────────┼───────┼──────────────────┤
│ 1 │ Play Music     │   Daily     │ 2025-01-15 │ 2025-01-20 │      5 │    15 │ Mastered chorus!  │
│ 2 │ Skin Care      │   Daily     │ 2025-01-16 │ 2025-01-20 │      3 │    10 │ Morning routine  │
│ 3 │ Finance Check  │   Weekly    │ 2025-01-10 │ 2025-01-15 │      2 │     3 │ Budget updated   │
╰───┴────────────────┴─────────────┴────────────┴────────────┴────────┴───────┴──────────────────╯

Enter the number of a habit to view detailed history (or 'q' to quit): _
```

**Detailed History (after selecting a habit):**
```
📅 Play Music (daily)

╭ ──────────── Habit Statistics ────────────  ╮
│ Created: 2025-01-15 10:30                   │
│ Total Completions: 15                       │
│ Current Streak: 5                           │
│ Longest Streak: 7                           │
│ Description: Practice instrument 15-30 min  │
╰ ──────────────────────────────────────────  ╯

📅 Completion History: 

   #  Date        Time      Notes
────────────────────────────────────────────────────────────
   1  2025-01-15  10:30:00  Started the habit
   2  2025-01-16  09:15:00  Practiced piano for 30 minutes
   3  2025-01-17  10:00:00  Guitar session - learned new chords
  ... 
```

### 5. Soft Delete (Archive)

Habits are archived by default, not permanently deleted:

```python
# Soft delete (default) - habit is archived
success, message = habit_service.delete_habit("Exercise", soft_delete=True)

# Hard delete - permanently removes from database
success, message = habit_service.delete_habit("Exercise", soft_delete=False)
```

**User Experience:**
```
🗑️ Delete a habit

Current habits:
  1. 📅 Play Music (daily)

Enter the number of the habit to delete (or 'q' to quit): 1
⚠️ Are you sure you want to delete 'Play Music'? (y/n): y

🗑️ Habit 'Play Music' deleted. 
```

### 6. UUID-based Identification

Every habit and tracker event has a unique UUID: 
```python
Habit(
    habit_id='550e8400-e29b-41d4-a716-446655440000',
    name='Exercise',
    ... 
)
```

**Benefits:**
- No naming conflicts
- Better for future features (sync, API, etc.)
- Industry-standard approach
- Enables reliable data relationships

### 7. Streak Calculation Algorithm

Smart streak calculation using functional programming:

**Daily Habits:**
- Checks for consecutive days
- Example:  Completed on Jan 1, 2, 3, 5 → Longest streak = 3

**Weekly Habits:**
- Normalizes to Monday of each week
- Example: Completed on Jan 1 (Mon), Jan 8 (Mon), Jan 15 (Mon) → Streak = 3

**Implementation (Functional):**
```python
# Functional approach: transform dates using set comprehension
normalized_dates = sorted({d.date() for d in history})

# Calculate using functional iteration
return max(longest_streak, current_streak)
```

### 8. Input Validation

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

### 9. Functional Programming

Extensive use of functional programming throughout:

**Techniques Used:**
- `map()` - Transform data
- `filter()` - Filter data
- `sorted()` with key functions - Functional sorting
- `lambda` expressions - Anonymous functions
- List/set comprehensions - Functional data transformation
- `max()` with key functions - Find maximum functionally
- Pure functions - No side effects

**Example:**
```python
# Repository:  Functional data transformation
habits = map(Habit.from_tuple, results)
habits = filter(lambda h: h. is_active, habits)
return sorted(habits, key=get_sort_key)

# Analytics: Functional streak calculation
streaks = [(h.name, self.calculate_longest_streak(h.name)) for h in habits]
return max(streaks, key=lambda x: x[1])
```

---

## 📊 Analytics Module

The analytics module is implemented entirely using **functional programming paradigms** as required. 

### Required Functionality

All four required analytics functions are implemented:

| Requirement | Implementation | Functional Programming |
|-------------|----------------|----------------------|
| ✅ List all currently tracked habits | `get_all_habits()` | `map()`, `filter()`, `sorted()` |
| ✅ List habits with same periodicity | `get_habits_by_periodicity()` | `map()`, `filter()`, `sorted()` |
| ✅ Longest streak of all habits | `get_longest_streak_all_habits()` | List comprehension, `max()` |
| ✅ Longest streak for given habit | `calculate_longest_streak()` | Set comprehension, `sorted()`, `max()` |

### Implementation with Functional Programming

#### 1. Return all currently tracked habits

**Location:** `services/habit_service.py` + `repositories/habit_repository.py`

```python
def find_all(self, include_inactive: bool = False) -> List[Habit]:
    """Functional programming approach to retrieve and sort habits."""
    # ...  SQL query ...
    
    # Functional:  map tuples to Habit objects
    habits = map(Habit.from_tuple, results)
    
    # Functional: filter inactive habits
    if not include_inactive:
        habits = filter(lambda h: h.is_active, habits)
    
    # Functional: sort using key function
    def get_sort_key(habit:  Habit) -> tuple:
        periodicity_map = {'daily': 1, 'weekly': 2}
        return (periodicity_map. get(habit.periodicity, 3), 
                -habit.created_at.timestamp())
    
    return sorted(habits, key=get_sort_key)
```

**Access:**
- Menu Option 5
- CLI:  `python cli.py list`

#### 2. Return habits with same periodicity

**Location:** `repositories/habit_repository.py`

```python
def find_by_periodicity(self, periodicity: str, include_inactive: bool = False) -> List[Habit]:
    """Functional approach to filter by periodicity."""
    # ... SQL query ...
    
    # Functional: map and filter
    habits = list(map(Habit.from_tuple, results))
    
    if not include_inactive:
        habits = list(filter(lambda h: h. is_active, habits))
    
    # Functional: sort by name
    return sorted(habits, key=lambda h: h.name)
```

**Access:**
- Menu Option 6
- CLI: `python cli.py filter daily` or `python cli.py filter weekly`

#### 3. Return longest streak of all habits

**Location:** `services/analytics_service.py`

```python
def get_longest_streak_all_habits(self) -> Tuple[str, int]:
    """
    Functional programming:  Find habit with longest streak.
    """
    habits = self.habit_repo.find_all()
    if not habits:
        return ("", 0)

    # Functional: map habits to (name, streak) tuples using list comprehension
    streaks = [
        (habit.name, self.calculate_longest_streak(habit.name))
        for habit in habits
    ]

    # Functional: find maximum using key function
    return max(streaks, key=lambda x: x[1]) if streaks else ("", 0)
```

**Access:**
- Menu Option 7
- CLI: `python cli.py champion`

#### 4. Return longest streak for a given habit

**Location:** `services/analytics_service.py`

```python
def calculate_longest_streak(self, habit_name: str) -> int:
    """
    Functional programming: Calculate longest streak. 
    """
    habit = self.habit_repo.find_by_name(habit_name)
    if not habit:
        return 0

    events = self.tracker_repo.find_by_habit_id(habit.habit_id)
    if not events:
        return 0

    # Functional:  map events to datetime objects using list comprehension
    history = [event.checked_at for event in events]
    periodicity = habit.periodicity

    # Functional: transform dates using set comprehension
    if periodicity == 'daily': 
        normalized_dates = sorted({d.date() for d in history})
        step = timedelta(days=1)
    else:
        # Functional: transform to week starts using set comprehension
        normalized_dates = sorted({
            datetime.fromisocalendar(
                d.isocalendar()[0],
                d.isocalendar()[1],
                1
            ).date()
            for d in history
        })
        step = timedelta(weeks=1)

    if len(normalized_dates) < 2:
        return len(normalized_dates)

    # Calculate streak (functional iteration)
    longest_streak = 0
    current_streak = 1

    for i in range(1, len(normalized_dates)):
        prev = normalized_dates[i - 1]
        curr = normalized_dates[i]
        
        if curr - prev == step:
            current_streak += 1
        else: 
            longest_streak = max(longest_streak, current_streak)
            current_streak = 1

    # Functional: return maximum
    return max(longest_streak, current_streak)
```

**Access:**
- Menu Option 8
- CLI: `python cli.py streak "Habit Name"`

### Functional Programming Techniques Summary

| Technique | Usage Count | Examples |
|-----------|-------------|----------|
| `map()` | ✅✅✅ | Transform tuples to objects |
| `filter()` | ✅✅ | Filter inactive habits |
| `sorted()` with key | ✅✅✅✅ | Sort by multiple criteria |
| `lambda` expressions | ✅✅✅✅✅ | Anonymous sorting/filtering functions |
| List comprehension | ✅✅✅ | Transform and map data |
| Set comprehension | ✅✅ | Deduplicate dates |
| `max()` with key | ✅✅✅ | Find maximum streak |
| Higher-order functions | ✅✅ | Functions that take/return functions |
| Pure functions | ✅✅✅✅ | No side effects in calculations |

---

## 🔍 Example Workflows

### Workflow 1: Complete Habit Creation and Tracking

```bash
# 1. Start the application (auto-seeds with 5 sample habits)
python main.py

# 2. Create a new habit with description
python cli.py create "Morning Run" daily --description "5km jog in the park to start the day fresh"

# 3. Check it off with notes
python cli.py checkoff "Morning Run" --notes "Great run! 28 minutes, felt energized"

# 4. Do it again the next day (building a streak!)
python cli.py checkoff "Morning Run" --notes "29 minutes, slightly faster pace"

# 5. Check your streak (analytics - functional programming)
python cli.py streak "Morning Run"
# Output: 🎯 Longest streak for 'Morning Run': 2

# 6. View all habits with descriptions
python cli.py list
```

### Workflow 2: Using Interactive Menu

```bash
# 1. Start interactive mode
python main.py

# 2. Option 1: Create habit
#    → Enter name:  "Yoga"
#    → Enter periodicity: "daily"
#    → Add description: "30 minutes morning yoga routine"

# 3. Option 3: Check-off habit
#    → Select:  1 (Yoga)
#    → Add notes: "y"
#    → Notes: "Great stretching session, feeling flexible"

# 4. Option 9: View completion table
#    → See comprehensive overview
#    → Select habit number for detailed history

# 5. Option 10: Edit completion notes
#    → Select habit
#    → Select completion
#    → Update notes

# 6. Option 7: Find champion (analytics - functional programming)
#    → See which habit has longest streak
```

### Workflow 3: Analytics Workflow

```bash
# List all habits (functional:  map, filter, sorted)
python cli.py list

# Filter by periodicity (functional: map, filter, sorted)
python cli.py filter daily

# Find champion habit (functional: list comprehension, max)
python cli.py champion
# Output: 🏆 Champion:  'Exercise' with streak of 12! 

# Check specific habit streak (functional: set comprehension, sorted, max)
python cli.py streak "Exercise"
# Output:  🎯 Longest streak for 'Exercise': 12
```

---

## 🧪 Running Tests

The project includes comprehensive unit tests covering all functionality including functional programming: 

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
- ✅ Habit creation with description
- ✅ Habit updates (including description)
- ✅ Soft delete and hard delete
- ✅ Check-off functionality
- ✅ Check-off with notes
- ✅ Streak calculations (daily and weekly) - functional implementation
- ✅ Broken streak detection
- ✅ Filtering by periodicity - functional implementation
- ✅ Analytics functions - all using functional programming
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
    description TEXT DEFAULT '',       -- Habit description
    is_active INTEGER DEFAULT 1        -- Soft delete flag (1=active, 0=inactive)
);
```

### Tracker Table
```sql
CREATE TABLE tracker (
    event_id TEXT PRIMARY KEY,         -- UUID
    habit_id TEXT NOT NULL,            -- Foreign key to habits
    checked_at TEXT NOT NULL,          -- ISO format datetime
    notes TEXT DEFAULT '',             -- Completion notes
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
    """Application configuration settings"""
    DATABASE_NAME = "main.db"
    DEFAULT_PERIODICITY_OPTIONS = ['daily', 'weekly']
    SEED_WEEKS = 4
    SEED_SUCCESS_RATE = 0.8  # 80% completion rate for seed data
    
    # Predefined habits for seeding (name, periodicity, description)
    SEED_HABITS = [
        ("Drink Water", "daily", "Stay hydrated throughout the day - 8 glasses minimum"),
        ("Read Book", "daily", "Read at least 20 pages of a book before bed"),
        ("Exercise", "daily", "30 minutes of physical activity - cardio or strength training"),
        ("Clean House", "weekly", "Deep cleaning and organizing living spaces"),
        ("Meditate", "weekly", "Mindfulness meditation session for mental clarity")
    ]
```

**Configuration Options:**
- `DATABASE_NAME`: SQLite database filename
- `DEFAULT_PERIODICITY_OPTIONS`: Allowed habit types
- `SEED_WEEKS`: How many weeks of sample data to generate
- `SEED_SUCCESS_RATE`: Completion rate for seed data (0.8 = 80%)
- `SEED_HABITS`: Pre-defined habits with descriptions

---

## 🏆 Benefits of This Architecture

| Benefit | Description | Impact |
|---------|-------------|--------|
| **Maintainability** | Each layer has one responsibility | Easy to locate and fix bugs |
| **Testability** | Can test each layer independently | Comprehensive test coverage |
| **Flexibility** | Easy to change implementations | Swap database without changing business logic |
| **Reusability** | Services can be used anywhere | Same service for CLI, API, or GUI |
| **Validation Centralized** | All business rules in one place | Consistent validation everywhere |
| **Separation of Concerns** | UI, logic, and data are separate | Change UI without touching business logic |
| **Functional Programming** | Pure functions in analytics | Easier to test, reason about, and debug |
| **Scalability** | Clean architecture supports growth | Easy to add features without breaking code |

---

## 📚 Understanding the Code Flow

### Example: Creating a Habit with Description

**1. User runs command:**
```bash
python cli.py create "Yoga" daily --description "30 minutes morning routine"
```

**2. CLI entry point (`cli.py`):**

```python
@cli.command()
def create(ctx, name, periodicity, description):
    view = ConsoleView()
    service = HabitService(db)

    success, message = service.create_habit(name, periodicity, description)

    if success:
        view.show_habit_created(name)
        if description:
            view.console.print(f"   💬 Description: {description}")
```

**3. Service validates (`services/habit_service.py`):**

```python
def create_habit(self, name, periodicity, description=""):
    # Validation
    if not name.strip():
        return False, "Name cannot be empty"

    # Check duplicates
    if self.repository.find_by_name(name):
        return False, "Already exists"

    # Create model with description
    habit = Habit(name=name, periodicity=periodicity, description=description)

    # Save via repository
    success = self.repository.save(habit)
    return success, "Created successfully"
```

**4. Repository saves (`repositories/habit_repository.py`):**

```python
def save(self, habit: Habit) -> bool:
    cur.execute(
        "INSERT INTO habits VALUES (?, ?, ?, ?, ?, ?, ? )",
        (habit.habit_id, habit.name, habit.periodicity,
         habit.created_at, habit.updated_at, habit.description, habit.is_active)
    )
    con.commit()
    return True
```

**5. View shows result (`views/console_view.py`):**
```python
def show_habit_created(self, name:  str):
    self.console.print(f"✅ Habit '{name}' created!", style="green")
```

---

## 🛠️ Dependencies

### `requirements.txt`
```
click>=8.0.0
rich>=13.0.0
```

**Library Purposes:**

| Library | Purpose | Features Used |
|---------|---------|---------------|
| **click** | Professional CLI framework | Command parsing, options, arguments, command groups |
| **rich** | Beautiful terminal formatting | Colors, tables, panels, text styling, console input |

**Why These Libraries?**
- **click**: Industry-standard for Python CLIs, clean command structure
- **rich**: Modern, beautiful terminal UI with minimal code
- **No ORM**: Direct SQLite for simplicity and learning
- **Minimal dependencies**: Only what's necessary

---

## 📖 Learning from This Project

This project demonstrates professional software engineering practices:

### Design Patterns Used
- ✅ **MVC (Model-View-Controller)** - Separation of concerns
- ✅ **Repository Pattern** - Data access abstraction
- ✅ **Service Layer Pattern** - Business logic centralization
- ✅ **Data Transfer Objects (DTOs)** - Pure data models
- ✅ **Functional Programming** - Analytics implementation

### SOLID Principles
- ✅ **Single Responsibility** - Each class has one job
- ✅ **Open/Closed** - Open for extension, closed for modification
- ✅ **Liskov Substitution** - Objects can be replaced by instances of their subtypes
- ✅ **Interface Segregation** - Many specific interfaces
- ✅ **Dependency Inversion** - Depend on abstractions, not concretions

### Programming Paradigms
- ✅ **Object-Oriented Programming** - Controllers, Services, Repositories
- ✅ **Functional Programming** - Analytics module (map, filter, reduce concepts)
- ✅ **Declarative Programming** - SQL queries
- ✅ **Imperative Programming** - Business logic flow

### Best Practices
- ✅ Type hints throughout
- ✅ Docstrings for all public methods
- ✅ Comprehensive error handling
- ✅ Input validation at service layer
- ✅ Unit tests for critical functionality
- ✅ Clear separation of concerns
- ✅ Functional programming for data transformation
- ✅ Meaningful variable and function names
- ✅ DRY (Don't Repeat Yourself) principle
- ✅ KISS (Keep It Simple, Stupid) principle

### What You'll Learn

By studying this codebase, you'll learn: 

1. **How to structure a professional Python application** - MVC architecture
2. **Separation of concerns** - Why it matters and how to implement
3. **Service layer pattern** - Centralizing business logic
4. **Repository pattern** - Abstracting data access
5. **Clean architecture** - Making code maintainable and scalable
6. **Type hints and dataclasses** - Modern Python features
7. **Click framework** - Building professional CLIs
8. **Rich library** - Beautiful terminal UIs
9. **Unit testing** - Testing layered applications
10. **SQLite with Python** - Database operations without ORM
11. **Functional programming** - Using `map`, `filter`, `sorted`, `lambda`
12. **Data transformation** - List/set comprehensions
13. **Error handling** - Tuple returns for success/failure
14. **User experience design** - Intuitive numbered menus, confirmations
15. **Configuration management** - Centralized settings

---

## 🤝 Contributing

Contributions are welcome! Please follow these guidelines:

1. **Maintain the architecture** - Keep layers separated
2. **No business logic in models or repositories** - Put it in services
3. **Use functional programming for analytics** - Follow existing patterns
4. **Add tests** - Test new features thoroughly
5. **Follow the pattern** - Look at existing code for examples
6. **Update docs** - Update README if adding major features
7. **Type hints** - Add type hints to all functions
8. **Docstrings** - Document all public methods

### How to Contribute

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

MIT License - Free to use for learning or personal projects.

```
MIT License

Copyright (c) 2025 Fabio De Cena

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## 📞 Support

- **GitHub Issues**:  [Open an issue](https://github.com/fabiodecena/habit_tracker/issues)
- **Questions**: Review the code examples above
- **Examples**: Check `tests/test_project.py` for usage patterns
- **Documentation**: This README covers all features

---

## 🎓 Additional Resources

### Python Resources
- [Python Dataclasses Documentation](https://docs.python.org/3/library/dataclasses.html)
- [Python Type Hints (PEP 484)](https://www.python.org/dev/peps/pep-0484/)
- [Functional Programming in Python](https://docs.python.org/3/howto/functional.html)

### Library Documentation
- [Click Documentation](https://click.palletsprojects.com/)
- [Rich Documentation](https://rich.readthedocs.io/)
- [SQLite Documentation](https://www.sqlite.org/docs.html)

### Architecture Patterns
- [MVC Pattern](https://en.wikipedia.org/wiki/Model%E2%80%93view%E2%80%93controller)
- [Repository Pattern](https://martinfowler.com/eaaCatalog/repository.html)
- [Service Layer Pattern](https://martinfowler.com/eaaCatalog/serviceLayer.html)
- [Clean Architecture](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture. html)

### Functional Programming
- [Functional Programming HOWTO](https://docs.python.org/3/howto/functional.html)
- [Map, Filter, Reduce](https://realpython.com/python-map-function/)
- [List Comprehensions](https://docs.python.org/3/tutorial/datastructures.html#list-comprehensions)

---

## 🎯 Project Statistics

- **Language**: Python 100%
- **Lines of Code**: ~2000+
- **Architecture**: MVC with Service Layer
- **Test Coverage**:  Comprehensive unit tests
- **Dependencies**: 2 (click, rich)
- **Python Version**: 3.7+
- **Database**: SQLite
- **Paradigms**: OOP + Functional Programming

---

**Built with ❤️ using clean architecture principles and functional programming** 🚀

**Repository**: [github.com/fabiodecena/habit_tracker](https://github.com/fabiodecena/habit_tracker)

---

*Last Updated: January 2025*