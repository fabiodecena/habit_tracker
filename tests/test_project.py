"""
Unit tests for Habit Tracker
"""
import unittest
from datetime import datetime, timedelta

from models.habit import Habit
from models.tracker import Tracker
from models.database import get_connection


class TestHabitTracker(unittest.TestCase):
    """Test cases for Habit Tracker functionality"""

    def setUp(self):
        """Set up test database and habits"""
        # Use an in-memory DB for testing
        self.db = get_connection(": memory:")
        self.habit_daily = Habit("Test Daily", "daily")
        self.habit_daily.create(self.db)
        self.habit_weekly = Habit("Test Weekly", "weekly")
        self.habit_weekly.create(self.db)

    def tearDown(self):
        """Clean up test database"""
        self.db.close()

    def test_habit_creation(self):
        """Test that habits are created correctly"""
        habits = Habit.get_all(self.db)
        self.assertEqual(len(habits), 2)
        self.assertEqual(habits[0][0], "Test Daily")

    def test_check_off(self):
        """Test checking off a habit"""
        Tracker.check_off("Test Daily", datetime.now(), self.db)
        history = Tracker.get_history("Test Daily", self.db)
        self.assertEqual(len(history), 1)

    def test_daily_streak_calculation(self):
        """Test streak calculation for daily habits"""
        # Day 1: Done
        d1 = datetime.now() - timedelta(days=2)
        Tracker.check_off("Test Daily", d1, self.db)

        # Day 2: Done (Consecutive)
        d2 = datetime.now() - timedelta(days=1)
        Tracker.check_off("Test Daily", d2, self.db)

        streak = Tracker.calculate_longest_streak("Test Daily", "daily", self.db)
        self.assertEqual(streak, 2)

    def test_broken_streak(self):
        """Test that broken streaks are calculated correctly"""
        # Day 1: Done
        d1 = datetime.now() - timedelta(days=5)
        Tracker.check_off("Test Daily", d1, self.db)

        # Gap of 3 days

        # Day 5: Done
        d2 = datetime.now()
        Tracker.check_off("Test Daily", d2, self.db)

        streak = Tracker.calculate_longest_streak("Test Daily", "daily", self.db)
        # Max streak should be 1, because the run was broken
        self.assertEqual(streak, 1)

    def test_habit_update(self):
        """Test updating a habit"""
        success = Habit.update("Test Daily", "Updated Daily", "weekly", self.db)
        self.assertTrue(success)

        updated_habit = Habit.find_by_name("Updated Daily", self.db)
        self.assertIsNotNone(updated_habit)
        self.assertEqual(updated_habit[1], "weekly")

    def test_habit_delete(self):
        """Test deleting a habit"""
        self.habit_daily.delete(self.db)
        habits = Habit.get_all(self.db)
        self.assertEqual(len(habits), 1)

    def test_get_by_periodicity(self):
        """Test filtering habits by periodicity"""
        daily_habits = Habit.get_by_periodicity("daily", self.db)
        weekly_habits = Habit.get_by_periodicity("weekly", self.db)

        self.assertEqual(len(daily_habits), 1)
        self.assertEqual(len(weekly_habits), 1)


if __name__ == '__main__':
    unittest.main()