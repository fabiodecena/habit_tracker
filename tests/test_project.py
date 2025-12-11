import unittest
import os
import sys
from datetime import datetime, timedelta

# Ensure import paths work
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from habit import Habit
import analytics
from database import get_connection


class TestHabitTracker(unittest.TestCase):

    def setUp(self):
        # Use an in-memory DB for testing
        self.db = get_connection(":memory:")
        self.habit_daily = Habit("Test Daily", "daily")
        self.habit_daily.store(self.db)
        self.habit_weekly = Habit("Test Weekly", "weekly")
        self.habit_weekly.store(self.db)

    def tearDown(self):
        self.db.close()

    def test_habit_creation(self):
        habits = analytics.get_all_habits(self.db)
        self.assertEqual(len(habits), 2)
        self.assertEqual(habits[0][0], "Test Daily")

    def test_check_off(self):
        self.habit_daily.check_off(datetime.now(), self.db)
        history = analytics.get_habit_history("Test Daily", self.db)
        self.assertEqual(len(history), 1)

    def test_daily_streak_calculation(self):
        # Day 1: Done
        d1 = datetime.now() - timedelta(days=2)
        self.habit_daily.check_off(d1, self.db)

        # Day 2: Done (Consecutive)
        d2 = datetime.now() - timedelta(days=1)
        self.habit_daily.check_off(d2, self.db)

        streak = analytics.calculate_longest_streak("Test Daily", "daily", self.db)
        self.assertEqual(streak, 2)

    def test_broken_streak(self):
        # Day 1: Done
        d1 = datetime.now() - timedelta(days=5)
        self.habit_daily.check_off(d1, self.db)

        # Gap of 3 days

        # Day 5: Done
        d2 = datetime.now()
        self.habit_daily.check_off(d2, self.db)

        streak = analytics.calculate_longest_streak("Test Daily", "daily", self.db)
        # Max streak should be 1, because the run was broken
        self.assertEqual(streak, 1)


if __name__ == '__main__':
    unittest.main()