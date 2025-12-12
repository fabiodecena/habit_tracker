"""
Tracker Service - Business logic for tracking operations
"""
from datetime import datetime
from typing import List, Tuple
from models.tracker import TrackerEvent
from repositories.tracker_repository import TrackerRepository
from repositories.habit_repository import HabitRepository


class TrackerService:
    """
    Handles business logic for tracking operations.
    """

    def __init__(self, db=None):
        """
        Initialize service.

        Args:
            db: Database connection (optional)
        """
        self.tracker_repo = TrackerRepository(db)
        self.habit_repo = HabitRepository(db)

    def check_off_habit(
            self,
            habit_name: str,
            checked_at: datetime = None,
            notes: str = ""
    ) -> Tuple[bool, str]:
        """
        Records a habit completion with validation.

        Args:
            habit_name: Name of the habit
            checked_at: When completed (defaults to now)
            notes: Optional notes about this completion

        Returns:
            Tuple of (success:  bool, message: str)
        """
        # Check if the habit exists
        habit = self.habit_repo.find_by_name(habit_name)
        if not habit:
            return False, f"Habit '{habit_name}' not found"

        # Check if habit is active
        if not habit.is_active:
            return False, f"Habit '{habit_name}' is inactive"

        # Default to now if not specified
        if checked_at is None:
            checked_at = datetime.now()

        # Validate date is not in the future
        if checked_at > datetime.now():
            return False, "Cannot check off a habit in the future"

        # Create and save event
        event = TrackerEvent(
            habit_id=habit.habit_id,
            checked_at=checked_at,
            notes=notes
        )
        success = self.tracker_repo.save(event)

        if success:
            return True, f"Habit '{habit_name}' checked off successfully"
        else:
            return False, "Failed to check off habit"

    def get_habit_history(self, habit_name: str) -> List[datetime]:
        """
        Returns completion history for a habit.

        Args:
            habit_name: Name of the habit

        Returns:
            List of datetime objects (sorted)
        """
        events = self.tracker_repo.find_by_habit_name(habit_name)
        return [event.checked_at for event in events]

    def get_habit_history_with_notes(self, habit_name: str) -> List[Tuple[datetime, str]]:
        """
        Returns completion history with notes for a habit.

        Args:
            habit_name: Name of the habit

        Returns:
            List of tuples (datetime, notes)
        """
        events = self.tracker_repo.find_by_habit_name(habit_name)
        return [(event.checked_at, event.notes) for event in events]

    def update_completion_notes(self, event_id: str, notes: str) -> Tuple[bool, str]:
        """
        Updates notes for a specific completion.

        Args:
            event_id: Event ID
            notes: New notes

        Returns:
            Tuple of (success:  bool, message: str)
        """
        # Verify event exists
        event = self.tracker_repo.find_by_event_id(event_id)
        if not event:
            return False, "Completion not found"

        success = self.tracker_repo.update_notes(event_id, notes)

        if success:
            return True, "Notes updated successfully"
        else:
            return False, "Failed to update notes"