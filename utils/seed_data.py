"""
Database seeding utility
"""
from datetime import datetime, timedelta
from views.console_view import ConsoleView
from services.habit_service import HabitService
from services.tracker_service import TrackerService
from config import Config


def seed_predefined_data(db):
    """
    Populates the database with predefined habits and sample data.

    Args:
        db: Database connection
    """
    habit_service = HabitService(db)

    # Check if data already exists
    if habit_service.has_habits():
        return

    view = ConsoleView()
    view.show_seeding_start()

    tracker_service = TrackerService(db)
    end_date = datetime.now()
    start_date = end_date - timedelta(weeks=Config.SEED_WEEKS)

    for name, periodicity in Config.SEED_HABITS:
        # Create habit
        habit_service.create_habit(name, periodicity)

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