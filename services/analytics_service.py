"""
Analytics Service - Business logic for analytics and streaks
"""
from datetime import datetime, timedelta
from typing import Tuple
from repositories.habit_repository import HabitRepository
from repositories.tracker_repository import TrackerRepository


class AnalyticsService:
    """
    Handles business logic for analytics operations.
    """

    def __init__(self, db=None):
        """
        Initialize service.

        Args:
            db: Database connection (optional)
        """
        self.habit_repo = HabitRepository(db)
        self.tracker_repo = TrackerRepository(db)

    def calculate_longest_streak(self, habit_name: str) -> int:
        """
        Calculates the longest streak for a habit.

        Args:
            habit_name:  Name of the habit

        Returns:
            Length of the longest streak
        """
        habit = self.habit_repo.find_by_name(habit_name)
        if not habit:
            return 0

        events = self.tracker_repo.find_by_habit(habit_name)
        if not events:
            return 0

        history = [event.checked_at for event in events]
        periodicity = habit.periodicity

        # Normalize dates based on periodicity
        if periodicity == 'daily':
            normalized_dates = sorted({d.date() for d in history})
            step = timedelta(days=1)
        else:
            # Normalize to the start (Monday) of the ISO week
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

        return max(longest_streak, current_streak)

    def get_longest_streak_all_habits(self) -> Tuple[str, int]:
        """
        Returns the habit with the longest streak.

        Returns:
            Tuple of (habit_name, streak_length)
        """
        habits = self.habit_repo.find_all()
        if not habits:
            return "", 0

        streaks = [
            (habit.name, self.calculate_longest_streak(habit.name))
            for habit in habits
        ]

        return max(streaks, key=lambda x: x[1]) if streaks else ("", 0)

    def get_current_streak(self, habit_name: str) -> int:
        """
        Calculates the current active streak for a habit.

        Args:
            habit_name: Name of the habit

        Returns:
            Length of current streak
        """
        habit = self.habit_repo.find_by_name(habit_name)
        if not habit:
            return 0

        events = self.tracker_repo.find_by_habit(habit_name)
        if not events:
            return 0

        history = [event.checked_at for event in events]
        periodicity = habit.periodicity

        # Normalize dates
        if periodicity == 'daily':
            normalized_dates = sorted({d.date() for d in history})
            step = timedelta(days=1)
            today = datetime.now().date()
        else:
            normalized_dates = sorted({
                datetime.fromisocalendar(
                    d.isocalendar()[0],
                    d.isocalendar()[1],
                    1
                ).date()
                for d in history
            })
            step = timedelta(weeks=1)
            today = datetime.fromisocalendar(
                datetime.now().isocalendar()[0],
                datetime.now().isocalendar()[1],
                1
            ).date()

        if not normalized_dates:
            return 0

        # Check if the last entry is recent enough
        last_date = normalized_dates[-1]
        if today - last_date > step:
            return 0  # Streak is broken

        # Count backwards from the end
        current_streak = 1
        for i in range(len(normalized_dates) - 2, -1, -1):
            if normalized_dates[i + 1] - normalized_dates[i] == step:
                current_streak += 1
            else:
                break

        return current_streak