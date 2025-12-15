"""
Database seeding utility
"""
from datetime import datetime, timedelta
from views.console_view import ConsoleView
from services.habit_service import HabitService
from services.tracker_service import TrackerService
from repositories.habit_repository import HabitRepository
from config import Config


def seed_predefined_data(db):
    """
    Populates the database with predefined habits and sample data.

    Args:
        db: Database connection
    """
    # Check if data already exists using a repository
    habit_repo = HabitRepository(db)

    if habit_repo.count() > 0:
        return  # Data already exists, don't overwrite

    view = ConsoleView()
    view.show_seeding_start()

    habit_service = HabitService(db)
    tracker_service = TrackerService(db)

    end_date = datetime.now()
    start_date = end_date - timedelta(weeks=Config.SEED_WEEKS)

    # Seed habits with comments
    for name, periodicity, comments in Config. SEED_HABITS:
        # Create habit with comments
        success, message = habit_service.create_habit(name, periodicity, comments)

        if not success:
            print(f"Warning: {message}")
            continue

        # Generate tracking data
        current = start_date
        while current <= end_date:
            if periodicity == 'daily':
                # Skip some days based on the success rate
                if int(current.timestamp()) % int(1 / Config.SEED_SUCCESS_RATE) != 0:
                    tracker_service.check_off_habit(name, current)
                current += timedelta(days=1)
            elif periodicity == 'weekly':
                tracker_service.check_off_habit(name, current)
                current += timedelta(weeks=1)

    view.show_seeding_complete()