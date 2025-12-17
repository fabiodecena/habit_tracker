"""
Analytics Service - Business logic for analytics and streaks
"""
from datetime import datetime, timedelta
from typing import Tuple, List, Optional
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
            habit_name: Name of the habit

        Returns:
            Length of the longest streak
        """
        habit = self.habit_repo.find_by_name(habit_name)
        if not habit:
            return 0

        events = self.tracker_repo.find_by_habit_id(habit.habit_id)  # Use habit_id
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
        habits = self.habit_repo. find_all()
        if not habits:
            return "", 0

        streaks = [
            (habit.name, self. calculate_longest_streak(habit. name))
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
        habit = self.habit_repo. find_by_name(habit_name)
        if not habit:
            return 0

        events = self.tracker_repo.find_by_habit_id(habit.habit_id)  # Use habit_id
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
                    d. isocalendar()[1],
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

    def get_completion_summary(self) -> List[dict]:
        """
        Get a completion summary for all active habits.

        Returns:
            List of dictionaries with habit summary data
        """
        habits = self.habit_repo.find_all(include_inactive=False)
        summary_data = []

        for habit in habits:
            # Get all completions for this habit
            events = self.tracker_repo.find_by_habit_id(habit.habit_id)

            # Calculate the last completion date
            last_completion = events[-1].checked_at if events else None

            # Calculate current streak
            current_streak = self.get_current_streak(habit.name)

            # Get latest notes (from most recent completion)
            latest_notes = events[-1].notes if events else ""

            summary_data.append({
                'habit_id': habit.habit_id,
                'name': habit.name,
                'periodicity': habit.periodicity,
                'created_at': habit.created_at,
                'notes': latest_notes,
                'last_completion': last_completion,
                'current_streak': current_streak,
                'total_completions': len(events)
            })

        # Sort by periodicity (daily first), then by creation date
        periodicity_order = {'daily': 1, 'weekly': 2}
        summary_data.sort(
            key=lambda x: (
                periodicity_order.get(x['periodicity'], 3),
                x['created_at']
            )
        )

        return summary_data

    def get_habit_completion_history(self, habit_name: str) -> Optional[dict]:
        """
        Get a detailed completion history for a specific habit.

        Args:
            habit_name: Name of the habit

        Returns:
            Dictionary with habit details and completion history
        """
        habit = self.habit_repo.find_by_name(habit_name)
        if not habit:
            return None

        events = self.tracker_repo.find_by_habit_id(habit.habit_id)

        # Sort by date (oldest first)
        completions = [
            {
                'event_id': event.event_id,  # ADDED
                'checked_at': event.checked_at,
                'notes': event.notes
            }
            for event in sorted(events, key=lambda e: e.checked_at)
        ]

        return {
            'habit_id': habit.habit_id,
            'name': habit.name,
            'periodicity': habit.periodicity,
            'created_at': habit.created_at,
            'description': habit.description,
            'completions': completions,
            'total_completions': len(completions),
            'longest_streak': self.calculate_longest_streak(habit_name),
            'current_streak': self.get_current_streak(habit_name)
        }