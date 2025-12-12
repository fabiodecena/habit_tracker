"""
Habit Service - Business logic for habit operations
"""
from typing import List, Optional
from models.habit import Habit
from repositories.habit_repository import HabitRepository
from config import Config


class HabitService:
    """
    Handles business logic for habit operations.
    """

    def __init__(self, db=None):
        """
        Initialize service.

        Args:
            db: Database connection (optional)
        """
        self.repository = HabitRepository(db)

    def create_habit(self, name: str, periodicity: str) -> tuple[bool, str]:
        """
        Creates a new habit with validation.

        Args:
            name: Habit name
            periodicity: 'daily' or 'weekly'

        Returns:
            Tuple of (success:  bool, message: str)
        """
        # Validation
        if not name or not name.strip():
            return False, "Habit name cannot be empty"

        if periodicity not in Config.DEFAULT_PERIODICITY_OPTIONS:
            return False, f"Periodicity must be one of {Config.DEFAULT_PERIODICITY_OPTIONS}"

        # Check if the habit already exists
        existing = self.repository.find_by_name(name)
        if existing:
            return False, f"Habit '{name}' already exists"

        # Create and save
        habit = Habit(name=name.strip(), periodicity=periodicity)
        success = self.repository.save(habit)

        if success:
            return True, f"Habit '{name}' created successfully"
        else:
            return False, "Failed to create habit"

    def update_habit(
            self,
            old_name: str,
            new_name: str,
            new_periodicity: str
    ) -> tuple[bool, str]:
        """
        Updates an existing habit with validation.

        Args:
            old_name: Current habit name
            new_name: New habit name
            new_periodicity: New periodicity

        Returns:
            Tuple of (success: bool, message: str)
        """
        # Validation
        if not new_name or not new_name.strip():
            return False, "Habit name cannot be empty"

        if new_periodicity not in Config.DEFAULT_PERIODICITY_OPTIONS:
            return False, f"Periodicity must be one of {Config.DEFAULT_PERIODICITY_OPTIONS}"

        # Check if old habit exists
        old_habit = self.repository.find_by_name(old_name)
        if not old_habit:
            return False, f"Habit '{old_name}' not found"

        # Check if new name conflicts with existing habit
        if new_name != old_name:
            existing = self.repository.find_by_name(new_name)
            if existing:
                return False, f"Habit '{new_name}' already exists"

        # Update
        updated_habit = Habit(name=new_name.strip(), periodicity=new_periodicity)
        success = self.repository.update(old_name, updated_habit)

        if success:
            return True, f"Habit updated successfully"
        else:
            return False, "Failed to update habit"

    def delete_habit(self, name: str) -> tuple[bool, str]:
        """
        Deletes a habit.

        Args:
            name: Habit name

        Returns:
            Tuple of (success: bool, message: str)
        """
        # Check if the habit exists
        habit = self.repository.find_by_name(name)
        if not habit:
            return False, f"Habit '{name}' not found"

        success = self.repository.delete(name)

        if success:
            return True, f"Habit '{name}' deleted successfully"
        else:
            return False, "Failed to delete habit"

    def get_all_habits(self) -> List[Habit]:
        """
        Returns all habits.

        Returns:
            List of Habit objects
        """
        return self.repository.find_all()

    def get_habit_by_name(self, name: str) -> Optional[Habit]:
        """
        Find a habit by name.

        Args:
            name: Habit name

        Returns:
            Habit object or None
        """
        return self.repository.find_by_name(name)

    def get_habits_by_periodicity(self, periodicity: str) -> List[Habit]:
        """
        Returns habits filtered by periodicity.

        Args:
            periodicity: 'daily' or 'weekly'

        Returns:
            List of Habit objects
        """
        return self.repository.find_by_periodicity(periodicity)

    def has_habits(self) -> bool:
        """
        Checks if any habits exist.

        Returns:
            True if habits exist, False otherwise
        """
        return self.repository.count() > 0