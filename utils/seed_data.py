"""
Database seeding utility with predefined test fixtures
"""
from datetime import datetime, timedelta
from views.console_view import ConsoleView
from services.habit_service import HabitService
from services.tracker_service import TrackerService
from repositories.habit_repository import HabitRepository


def seed_predefined_data(db):
    """
    Populates the database with predefined habits and test fixture data.

    Each habit has exactly 4 weeks of tracking data with specific patterns
    for testing purposes.  Includes one inactive habit (Skin Care) for testing
    archive functionality.

    Args:
        db: Database connection
    """
    # Check if data already exists
    habit_repo = HabitRepository(db)

    if habit_repo.count() > 0:
        return  # Data already exists, don't overwrite

    view = ConsoleView()
    view.show_seeding_start()

    habit_service = HabitService(db)
    tracker_service = TrackerService(db)

    # Calculate date range: exactly 4 weeks from today backward
    end_date = datetime.now()
    start_date = end_date - timedelta(weeks=4)

    # Define predefined habits with descriptions and status
    # Format: (name, periodicity, description, is_active)
    predefined_habits = [
        ("Read Journal", "daily", "Read a journal (20-35 minutes)", True),
        ("Skin Care", "daily", "Complete your skincare routine", False),  # Inactive/Archived
        ("Play Music", "daily", "Practice an instrument for at least 15–30 minutes", True),
        ("Finance Check", "weekly", "Review spending and update your budget/accounts", True),
        ("Water Plants", "weekly", "Water plants and check soil moisture/leaves", True)
    ]

    # Create habits with status
    for name, periodicity, description, is_active in predefined_habits:
        # Create habit (always active initially)
        success, message = habit_service.create_habit(name, periodicity, description)
        if not success:
            print(f"Warning: {message}")
            continue

        # If habit should be inactive, update its status
        if not is_active:
            habit = habit_service.get_habit_by_name(name)
            if habit:
                habit.is_active = False
                habit_repo.update(habit)

    # Generate predefined tracking data (test fixtures)
    _seed_read_journal(tracker_service, start_date, end_date)
    _seed_skin_care(tracker_service, start_date, end_date)  # Has data but is archived
    _seed_play_music(tracker_service, start_date, end_date)
    _seed_finance_check(tracker_service, start_date, end_date)
    _seed_water_plants(tracker_service, start_date, end_date)

    view.show_seeding_complete()


def _seed_read_journal(tracker_service, start_date, end_date):
    """
    Seed data for 'Read Journal' habit.
    Pattern: Perfect streak for 28 days (the best daily performer)
    Status:  ACTIVE
    """
    current = start_date
    day_count = 0

    while current <= end_date:
        day_count += 1
        # Alternate between morning and evening reading
        notes = "Morning reading session" if day_count % 2 == 1 else "Evening reading session"
        tracker_service.check_off_habit("Read Journal", current, notes)
        current += timedelta(days=1)


def _seed_skin_care(tracker_service, start_date, end_date):
    """
    Seed data for 'Skin Care' habit.
    Pattern: Was tracked for 3 weeks with good consistency, then archived
    Status: INACTIVE (archived after 3 weeks)

    This habit demonstrates:
    - Inactive habits retain historical data
    - Inactive habits don't appear in active lists
    - Archived habits can be reactivated
    """
    current = start_date
    day_count = 0
    three_weeks = start_date + timedelta(weeks=3)

    # Tracked for 3 weeks, then archived (routine changed)
    while current <= three_weeks and current <= end_date:
        day_count += 1
        # Missed 2 days in week 2 (days 10, 11 - busy weekend)
        if day_count not in [10, 11]:
            notes = "Full routine completed" if day_count % 3 == 0 else "Morning routine"
            tracker_service.check_off_habit("Skin Care", current, notes)
        current += timedelta(days=1)


def _seed_play_music(tracker_service, start_date, end_date):
    """
    Seed data for 'Play Music' habit.
    Pattern: Consistent practice with rest days (every 5th day missed)
    Status: ACTIVE
    """
    current = start_date
    day_count = 0

    while current <= end_date:
        day_count += 1
        # Rest day every 5th day (prevent burnout)
        if day_count % 5 != 0:
            instruments = ["Piano practice", "Guitar session", "Vocal exercises", "Music theory"]
            notes = instruments[day_count % 4]
            tracker_service.check_off_habit("Play Music", current, notes)
        current += timedelta(days=1)


def _seed_finance_check(tracker_service, start_date, end_date):
    """
    Seed data for 'Finance Check' habit (weekly).
    Pattern: Perfect weekly completion (every Sunday)
    Status: ACTIVE
    """
    current = start_date
    # Move to the first Sunday
    while current.weekday() != 6:  # 6 = Sunday
        current += timedelta(days=1)

    week = 0
    while current <= end_date:
        week += 1
        tasks = [
            "Budget review and expense tracking",
            "Investment portfolio check",
            "Bill payments verified",
            "Savings goals updated"
        ]
        notes = tasks[week % 4]
        tracker_service.check_off_habit("Finance Check", current, notes)
        current += timedelta(weeks=1)


def _seed_water_plants(tracker_service, start_date, end_date):
    """
    Seed data for 'Water Plants' habit (weekly).
    Pattern: Missed week 2 (broken weekly streak - was traveling)
    Status: ACTIVE
    """
    current = start_date
    # Move to the first Saturday
    while current.weekday() != 5:  # 5 = Saturday
        current += timedelta(days=1)

    week = 0
    while current <= end_date:
        week += 1
        # Skip week 2 (traveling)
        if week != 2:
            plant_notes = [
                "Watered all plants, checked for pests",
                "Deep watering session, trimmed dead leaves",
                "Regular watering, soil looks healthy",
                "Watered and fertilized indoor plants"
            ]
            notes = plant_notes[week % 4]
            tracker_service.check_off_habit("Water Plants", current, notes)
        current += timedelta(weeks=1)