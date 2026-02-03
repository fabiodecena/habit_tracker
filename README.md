# Habit Tracker Application

A Python-based command-line habit tracking application that helps users build and maintain positive habits through periodic task completion and streak tracking.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [System Requirements](#system-requirements)
- [Installation](#installation)
  - [1. Clone the Repository](#1-clone-the-repository)
  - [2. Set Up Virtual Environment](#2-set-up-virtual-environment)
  - [3. Install Dependencies](#3-install-dependencies)
- [Quick Start](#quick-start)
- [Usage](#usage)
  - [Interactive Menu Mode](#interactive-menu-mode)
  - [Main Menu Options](#main-menu-options)
  - [Direct CLI Commands](#direct-cli-commands)
  - [Creating a New Habit](#creating-a-new-habit)
  - [Completing a Habit Task](#completing-a-habit-task)
  - [Viewing All Habits](#viewing-all-habits)
  - [Editing a Habit](#editing-a-habit)
  - [Deleting a Habit](#deleting-a-habit)
  - [Analyzing Habits](#analyzing-habits)
- [Predefined Habits](#predefined-habits)
- [Analytics Features](#analytics-features)
- [Project Structure](#project-structure)
- [Architecture](#architecture)
  - [Object-Oriented Components](#object-oriented-components)
  - [Functional Programming Components](#functional-programming-components)
  - [Data Persistence](#data-persistence)
- [Testing](#testing)
- [Code Documentation](#code-documentation)
- [Development](#development)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)
- [Author](#author)

## Overview

This habit tracker application was developed as a backend system for managing personal habits and goals. It provides essential functionality for creating, tracking, and analyzing habits without requiring a graphical user interface.  The application is built using modern Python practices, combining object-oriented and functional programming paradigms. 

**Key Concepts:**
- **Habit**: A clearly defined task with a specific periodicity (e.g., daily or weekly)
- **Check-off**: Marking a habit as completed for the current period
- **Streak**:  Consecutive periods where a habit was successfully completed
- **Break**: Missing a habit completion during its defined period

## Features

✅ Create and manage multiple habits with daily or weekly periodicity  
✅ Track habit completions with timestamps and notes  
✅ Maintain streak counts for consistent habit completion  
✅ Analyze habit performance with comprehensive analytics  
✅ Persistent storage using SQLite database  
✅ Interactive menu and direct CLI commands for easy interaction  
✅ Pre-loaded with 5 example habits and 4 weeks of tracking data  
✅ Comprehensive unit test suite  
✅ Full Python docstring documentation  
✅ Built with Click framework for professional CLI experience  

## System Requirements

- **Python**:  3.7 or later
- **Operating System**: Windows, macOS, or Linux
- **Storage**:  Minimum 10 MB free space
- **Dependencies**: Listed in `requirements.txt`

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/fabiodecena/habit_tracker.git
cd habit_tracker
```

### 2. Set Up Virtual Environment

**On Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**On macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

**Note:** The application requires the following packages:
- `click` - For CLI interface
- `rich` - For beautiful console formatting
- `pytest` - For testing (development)
- Built-in libraries: `sqlite3`, `datetime`, `json`

## Quick Start

After installation, you can launch the application in two ways:

**Option 1: Interactive Menu Mode (Recommended)**
```bash
python main.py
```

**Option 2: Direct CLI Commands**
```bash
python main.py --help
```

## Usage

### Interactive Menu Mode

Launch the interactive menu by running: 

```bash
python main.py
```

You'll see the main menu: 

```
╔════════════════════════════════════════════╗
║     HABIT TRACKER - MAIN MENU             ║
╚════════════════════════════════════════════╝

1. 📝 Manage Habits
2. ✅ Track Progress  
3. 📊 Analytics & Reports
4. 🚪 Exit

Enter your choice (1-4):
```

### Main Menu Options

#### 1. 📝 Manage Habits

This submenu allows you to: 
- Create new habits
- View all habits (active and inactive)
- Edit existing habits
- Delete or archive habits
- List all tracked habits
- Filter habits by periodicity (daily/weekly)

#### 2. ✅ Track Progress

This submenu allows you to:
- Check off habits (mark as complete)
- View completion history
- Add notes to completions
- See current streaks


#### 3. 📊 Analytics & Reports

This submenu provides:
- View longest streaks across all habits
- View longest streak for specific habits
- Analyze completion patterns

#### 4. 🚪 Exit

Exit the application.

### Direct CLI Commands

For quick actions without entering the interactive menu, use direct commands:

```bash
# Show all available commands
python main.py --help
```

**Available Commands:**

| Command | Description |
|---------|-------------|
| `menu` | 🎯 Launch interactive menu |
| `create` | ✨ Create a new habit |
| `checkoff` | ✅ Check off a habit |
| `habit-list` | 📋 List all habits |
| `edit` | 📝 Edit a habit |
| `delete` | ❌ Delete a habit |
| `champion` | 🏆 Show the habit with the longest streak |
| `streak` | 🎯 Show the longest streak for a specific habit |

### Creating a New Habit

**Interactive Menu:**
1. Select option `1` (Manage Habits)
2. Choose "Create new habit"
3. Enter the habit name (e.g., "Read Journal")
4. Choose periodicity:  `daily` or `weekly`
5. Add an optional description

**Direct CLI Command:**
```bash
python main.py create "Read Journal" daily --description "Read a journal for 20-35 minutes"
```

**Example Output:**
```
✨ Habit 'Read Journal' created successfully! 
   💬 Description: Read a journal for 20-35 minutes
```

### Completing a Habit Task

**Interactive Menu:**
1. Select option `2` (Track Progress)
2. Choose "Check off habit"
3. Select the habit from the list
4. Optionally add notes about the completion

**Direct CLI Command:**
```bash
python main.py checkoff "Read Journal" --notes "Finished Chapter 3"
```

**Example Output:**
```
✅ Habit 'Read Journal' checked off! 
   📝 Notes:  Finished Chapter 3
```

### Viewing All Habits

**Interactive Menu:**
1. Select option `1` (Manage Habits)
2. Choose "List all habits"

**Direct CLI Commands:**

```bash
# Show active habits only
python main.py habit-list

# Show all habits including archived
python main.py habit-list --all
```

**Example Output:**
```
📋 Active Habits: 

Name             | Periodicity | Description
-----------------|-------------|------------------------------------------
Read Journal     | Daily       | Read a journal (20-35 minutes)
Play Music       | Daily       | Practice an instrument for 15–30 minutes
Finance Check    | Weekly      | Review spending and update budget/accounts
Water Plants     | Weekly      | Water plants and check soil moisture
```

### Editing a Habit

**Interactive Menu:**
1. Select option `1` (Manage Habits)
2. Choose "Edit habit"
3. Select the habit to edit
4. Choose what to modify (name, periodicity, description, status)

**Direct CLI Commands:**

```bash
# Change habit name
python main.py edit "Read Journal" --new-name "Daily Reading"

# Change periodicity
python main.py edit "Play Music" --periodicity weekly

# Update description
python main.py edit "Finance Check" --description "Complete financial review"

# Activate/deactivate a habit
python main.py edit "Skin Care" --activate
python main.py edit "Skin Care" --deactivate
```

### Deleting a Habit

**Interactive Menu:**
1. Select option `1` (Manage Habits)
2. Choose "Delete habit"
3. Select the habit to delete
4. Confirm deletion (soft or hard delete)

**Direct CLI Commands:**

```bash
# Soft delete (archive) - can be restored later
python main.py delete "Old Habit"

# Hard delete (permanent) - cannot be undone
python main.py delete "Old Habit" --hard
```

**Example:**
```
⚠️  Archive 'Old Habit'? (You can restore it later) (y/n): y
✓ Habit 'Old Habit' archived successfully
```

### Analyzing Habits

**Interactive Menu:**
1. Select option `3` (Analytics & Reports)
2. Choose from various analytics options: 
   - Show all habits
   - Show habits by periodicity
   - Show longest streak (all habits)
   - Show longest streak for specific habit

**Direct CLI Commands:**

```bash
# Show champion habit (longest overall streak)
python main.py champion

# Show longest streak for a specific habit
python main.py streak "Read Journal"
```

**Example Output:**

```
🏆 Champion Habit: Read Journal
   Longest streak: 28 days
```

```
🎯 Habit:  Play Music
   Longest streak: 22 days
```

## Predefined Habits

The application comes with **5 predefined habits** and **4 weeks of tracking data** (28 days):

| Habit Name | Periodicity | Description | Status |
|-----------|-------------|-------------|--------|
| **Read Journal** | Daily | Read a journal (20-35 minutes) | Active |
| **Skin Care** | Daily | Complete your skincare routine | Inactive |
| **Play Music** | Daily | Practice an instrument for 15–30 minutes | Active |
| **Finance Check** | Weekly | Review spending and update budget/accounts | Active |
| **Water Plants** | Weekly | Water plants and check soil moisture/leaves | Active |

### Tracking Data Patterns

Each predefined habit demonstrates different tracking behaviors:

1. **Read Journal** (Daily)
   - Perfect 28-day streak
   - Demonstrates consistent daily completion
   - Alternates between morning and evening sessions

2. **Skin Care** (Daily) - INACTIVE
   - Tracked for 3 weeks, then archived
   - Missed 2 days in week 2 (days 10-11)
   - Shows how archived habits retain historical data

3. **Play Music** (Daily)
   - Consistent practice with rest days
   - Missed every 5th day (intentional rest)
   - Demonstrates realistic habit tracking with breaks

4. **Finance Check** (Weekly)
   - Perfect weekly completion (every Sunday)
   - 4 weeks of consistent tracking
   - Shows weekly habit success pattern

5. **Water Plants** (Weekly)
   - Missed week 2 (broken streak)
   - Demonstrates recovery after missing a period
   - 3 out of 4 weeks completed

## Analytics Features

The analytics module implements functional programming paradigms and provides: 

### 1. List All Habits
Returns a complete list of all tracked habits with creation dates and current status.

```bash
python main.py habit-list
```

### 2. Filter by Periodicity
Retrieve all daily habits or all weekly habits separately for focused analysis.

**Via Interactive Menu:**
- Navigate to Analytics & Reports
- Select "Show habits by periodicity"
- Choose daily or weekly

### 3. Champion Habit (Longest Overall Streak)
Calculates and displays the longest streak achieved across all habits: 

```bash
python main.py champion
```

**Output:**
```
🏆 Champion Habit: Read Journal
   Longest streak: 28 days
```

### 4. Longest Streak for Specific Habit
Analyzes a single habit's performance history to find its best streak:

```bash
python main.py streak "Play Music"
```

**Output:**
```
🎯 Habit: Play Music
   Longest streak: 22 days
```

### 5. Current Streak Tracking
View your current active streak for any habit to stay motivated. 

## Project Structure

```
habit_tracker/
│
├── main.py                      # Application entry point
├── cli.py                       # CLI interface using Click
├── requirements.txt             # Python dependencies
├── README.md                    # This file
│
├── controllers/
│   ├── menu_controller.py       # Main menu controller
│   ├── manage_habits_controller.py      # Manage Habits submenu
│   ├── track_progress_controller.py     # Track Progress submenu
│   ├── analytics_reports_controller.py  # Analytics & Reports submenu
│   ├── habit_controller.py      # Habit management logic
│   ├── tracker_controller.py    # Tracking logic
│   ├── analytics_controller.py  # Analytics logic
│   └── completion_controller.py # Completion management
│
├── database/
│   └── connection. py            # Database connection management
│
├── repositories/
│   ├── habit_repository.py      # Habit data access layer
│   └── tracker_repository.py   # Check-off data access layer
│
├── models/
│   ├── habit.py                 # Habit class definition (OOP)
│   └── tracker.py              # Check-off model
│
├── services/
│   ├── habit_service.py         # Habit business logic
│   ├── tracker_service.py       # Tracking functionality
│   └── analytics_service.py     # Analytics functions (Functional)
│
├── views/
│   └── console_view.py          # Console output formatting
│
├── utils/
│   └── seed_data.py             # Pre-defined habit data loader
│
└── tests/
    └── test_*. py                # Unit test suite
```

## Architecture

### Object-Oriented Components

**Habit Class** (`models/habit.py`)

The core of the application is the `Habit` class, which encapsulates: 

- **Attributes:**
  - `name`: habit name
  - `periodicity`: 
  - `habit_id`: unique identifier (generated by database)
  - `created_at`: timestamp of habit creation
  - `updated_at`: timestamp of last update 
  - `is_active`: boolean indicating whether the habit is active or archived
  - `description`: optional description

- **Methods:**
  - Getter and setter methods for encapsulation
  - Data validation
  - Object representation

**Tracker Model** (`models/tracker.py`)

Represents a single completion event: 
- `habit_id`: reference to the parent habit 
- `checked_at`: completion timestamp 
- `event_id`: optional unique identifier 
- `notes`: optional notes about the completion 

**MVC Architecture:**

The application follows the Model-View-Controller pattern:

- **Models**:  Data structures (Habit, Tracker)
- **Views**: Console output formatting (ConsoleView)
- **Controllers**: Business logic and flow control
  - MenuController: Main menu navigation
  - HabitController: Habit CRUD operations
  - TrackerController: Completion tracking
  - AnalyticsController: Data analysis

### Functional Programming Components

**Analytics Module** (`services/analytics_service.py`)

All analytics functions follow functional programming principles:

- Pure functions without side effects
- Immutable data handling
- Higher-order functions (filter, map, reduce)
- List comprehensions

**Key Functions:**
```python
calculate_longest_streak(habit_name)
get_longest_streak_all_habits()
get_current_streak(habit_name)
get_completion_summary()
get_habit_completion_history(habit_name)
```

### Data Persistence

**Database Layer** (`database/`)

- **Technology**: SQLite3 (embedded relational database)
- **Schema:**
  - `habits` table: Stores habit definitions
  - `tracker` table: Tracks completion timestamps
- **Operations:**
  - CRUD operations for habits
  - Transaction management
  - Data integrity enforcement

**Database Schema:**

```sql
-- Habits table
CREATE TABLE IF NOT EXISTS habits (
                habit_id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                periodicity TEXT NOT NULL,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                description TEXT DEFAULT '',
                is_active INTEGER DEFAULT 1
            );

-- Tracker table
CREATE TABLE IF NOT EXISTS tracker (
                event_id TEXT PRIMARY KEY,
                habit_id TEXT NOT NULL,
                checked_at TEXT NOT NULL,
                notes TEXT DEFAULT '',
                FOREIGN KEY (habit_id) REFERENCES habits(habit_id) ON DELETE CASCADE
            );
```

**Advantages over file-based storage:**
- ACID compliance
- Concurrent access support
- Efficient querying
- Built-in data validation
- Relational integrity

## Testing

The application includes a comprehensive unit test suite using Python's built-in `unittest` framework.

### Running Tests

**Run all tests:**
```bash
python -m unittest
```

### Test Coverage

The test suite covers:

✅ Habit creation and initialization  
✅ Habit editing and deletion (soft delete / hard delete)  
✅ Task completion functionality  
✅ Streak calculation logic (daily and weekly)  
✅ Habit breaking detection  
✅ Analytics functions (longest streak, current streak, completion summary, completion history)  
✅ Database operations using an in-memory SQLite database  
✅ Edge cases and error handling  
✅ Habit restoration (reactivation)  

### Example Test Output

```
tests/test_habit_service.py::test_create_habit PASSED
tests/test_tracker_service.py::test_checkoff_habit PASSED
tests/test_analytics_service.py::test_longest_streak PASSED
tests/test_analytics_service.py::test_champion_habit PASSED
==================== 28 passed in 4.12s ====================
```

## Code Documentation

All Python code includes comprehensive docstring documentation following PEP 257 conventions. 

### Viewing HTML Documentation

The project uses **pdoc** to generate HTML documentation from Python docstrings. 

**Access the documentation:**

**Option 1: Open in Browser**
```bash
# macOS
open docs/html/index.html

# Linux
xdg-open docs/html/index.html

# Windows
start docs/html/index.html
```

**Option 2: Direct File Path**
Navigate to `docs/html/index.html` in your file explorer and open it with your browser.

**Option 3: GitHub Repository**
Browse the documentation directly on GitHub:  [docs/html/index.html](https://github.com/fabiodecena/habit_tracker/blob/master/docs/html/index.html)

### Generating Documentation

To regenerate the HTML documentation after making code changes:

```bash
# Install pdoc if not already installed
pip install pdoc3

# Generate HTML documentation
pdoc --html --output-dir docs --force . 
```

**Command options explained:**
- `--html`: Generate HTML output
- `--output-dir docs`: Save documentation to the `docs/` folder
- `--force`: Overwrite existing documentation
- `.`: Document the current directory (entire project)

**Generate docs for specific modules:**
```bash
# Document only models
pdoc --html --output-dir docs --force models/

# Document only services
pdoc --html --output-dir docs --force services/

# Document only controllers
pdoc --html --output-dir docs --force controllers/
```

### Documentation Coverage

The HTML documentation includes: 

✅ All class definitions and methods  
✅ Function signatures with type hints  
✅ Parameter descriptions  
✅ Return value specifications  
✅ Usage examples  
✅ Module-level documentation  
✅ Interactive search functionality

## Development

### Adding New Features

1. **Create a new branch:**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Implement your changes** following the existing MVC structure

3. **Add tests** for new functionality in the `tests/` directory

4. **Update documentation** in docstrings and README

5. **Run tests** to ensure nothing breaks: 
   ```bash
   python -m unittest
   ```

6. **Commit and push:**
   ```bash
   git add .
   git commit -m "Add feature:  your feature description"
   git push origin feature/your-feature-name
   ```

### Code Style

The project follows **PEP 8** Python style guidelines: 
- 4 spaces for indentation
- Maximum line length: 79-100 characters
- Descriptive variable names
- Comprehensive comments and docstrings
- MVC pattern separation

## Troubleshooting

### Common Issues

**Issue:** `ModuleNotFoundError: No module named 'click'` or `'rich'`  
**Solution:** Install dependencies:  `pip install -r requirements.txt`

**Issue:** Database locked error  
**Solution:** Ensure no other instance is running; close the application and restart

**Issue:** Virtual environment not activating  
**Solution:** Check Python installation; recreate venv:  `python -m venv venv`

**Issue:** Tests failing after installation  
**Solution:** Ensure you're in the project root directory; verify Python version ≥3.7

**Issue:** Command not found when running `python main.py`  
**Solution:** Try `python3 main.py` or ensure Python is in your PATH

**Issue:** Predefined habits not showing  
**Solution:** Delete the database file and restart to re-seed data

### Getting Help

If you encounter issues not listed here:
1. Check the [GitHub Issues](https://github.com/fabiodecena/habit_tracker/issues) page
2. Create a new issue with: 
   - Error message
   - Python version (`python --version`)
   - Operating system
   - Steps to reproduce

## Contributing

Contributions are welcome!  Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

**Contribution Guidelines:**
- Write tests for new features
- Follow PEP 8 style guidelines
- Update documentation
- Keep commits atomic and well-described
- Follow the MVC architecture pattern

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Author

**Fabio Decena**  
GitHub: [@fabiodecena](https://github.com/fabiodecena)  
Repository: [habit_tracker](https://github.com/fabiodecena/habit_tracker)

---

**Repository Link**:  [https://github.com/fabiodecena/habit_tracker](https://github.com/fabiodecena/habit_tracker)

For questions, feedback, or support, please open an issue on GitHub. 