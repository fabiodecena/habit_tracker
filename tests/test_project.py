"""
Unit tests for Habit Tracker
"""
import unittest
from datetime import datetime, timedelta
from services.habit_service import HabitService
from services.tracker_service import TrackerService
from services.analytics_service import AnalyticsService
from database.connection import Database


class TestHabitTracker(unittest.TestCase):
    """Test cases for Habit Tracker functionality"""

    def setUp(self):
        """Set up test database and services"""
        # Use an in-memory DB for testing
        self.db = Database. get_connection(": memory:")

        # Initialize services
        self.habit_service = HabitService(self. db)
        self.tracker_service = TrackerService(self. db)
        self.analytics_service = AnalyticsService(self.db)

        # Create test habits
        self.habit_service.create_habit("Test Daily", "daily")
        self.habit_service.create_habit("Test Weekly", "weekly")

    def tearDown(self):
        """Clean up test database"""
        self.db.close()

    def test_habit_creation(self):
        """Test that habits are created correctly"""
        habits = self.habit_service.get_all_habits()
        self.assertEqual(len(habits), 2)
        self.assertEqual(habits[0].name, "Test Daily")

    def test_habit_has_id(self):
        """Test that habits have unique IDs"""
        habit = self.habit_service. get_habit_by_name("Test Daily")
        self.assertIsNotNone(habit.habit_id)
        self.assertTrue(len(habit.habit_id) > 0)

    def test_check_off(self):
        """Test checking off a habit"""
        success, message = self.tracker_service.check_off_habit("Test Daily", datetime.now())
        self.assertTrue(success)

        history = self.tracker_service.get_habit_history("Test Daily")
        self.assertEqual(len(history), 1)

    def test_check_off_with_notes(self):
        """Test checking off a habit with notes"""
        success, message = self.tracker_service.check_off_habit(
            "Test Daily",
            datetime.now(),
            "Felt great today!"
        )
        self.assertTrue(success)

        history_with_notes = self.tracker_service.get_habit_history_with_notes("Test Daily")
        self.assertEqual(len(history_with_notes), 1)
        self.assertEqual(history_with_notes[0][1], "Felt great today!")

    def test_daily_streak_calculation(self):
        """Test streak calculation for daily habits"""
        # Day 1: Done
        d1 = datetime.now() - timedelta(days=2)
        self.tracker_service.check_off_habit("Test Daily", d1)

        # Day 2: Done (Consecutive)
        d2 = datetime.now() - timedelta(days=1)
        self.tracker_service.check_off_habit("Test Daily", d2)

        streak = self.analytics_service.calculate_longest_streak("Test Daily")
        self.assertEqual(streak, 2)

    def test_broken_streak(self):
        """Test that broken streaks are calculated correctly"""
        # Day 1: Done
        d1 = datetime. now() - timedelta(days=5)
        self.tracker_service.check_off_habit("Test Daily", d1)

        # Gap of 3 days

        # Day 5: Done
        d2 = datetime.now()
        self.tracker_service. check_off_habit("Test Daily", d2)

        streak = self.analytics_service.calculate_longest_streak("Test Daily")
        # Max streak should be 1, because the run was broken
        self.assertEqual(streak, 1)

    def test_habit_update(self):
        """Test updating a habit"""
        success, message = self.habit_service.update_habit(
            "Test Daily",
            "Updated Daily",
            "weekly"
        )
        self.assertTrue(success)

        updated_habit = self.habit_service.get_habit_by_name("Updated Daily")
        self.assertIsNotNone(updated_habit)
        self.assertEqual(updated_habit.periodicity, "weekly")

    def test_habit_soft_delete(self):
        """Test soft deleting a habit"""
        success, message = self.habit_service.delete_habit("Test Daily", soft_delete=True)
        self.assertTrue(success)

        # Should not appear in active habits
        active_habits = self.habit_service.get_all_habits(include_inactive=False)
        self.assertEqual(len(active_habits), 1)

        # Should appear when including inactive
        all_habits = self.habit_service.get_all_habits(include_inactive=True)
        self.assertEqual(len(all_habits), 2)

    def test_habit_hard_delete(self):
        """Test permanently deleting a habit"""
        success, message = self.habit_service.delete_habit("Test Daily", soft_delete=False)
        self.assertTrue(success)

        habits = self.habit_service.get_all_habits(include_inactive=True)
        self.assertEqual(len(habits), 1)

    def test_get_by_periodicity(self):
        """Test filtering habits by periodicity"""
        daily_habits = self.habit_service.get_habits_by_periodicity("daily")
        weekly_habits = self.habit_service.get_habits_by_periodicity("weekly")

        self.assertEqual(len(daily_habits), 1)
        self.assertEqual(len(weekly_habits), 1)

    def test_longest_streak_all_habits(self):
        """Test getting the longest streak across all habits"""
        # Add some check-offs
        for i in range(5):
            d = datetime.now() - timedelta(days=i)
            self.tracker_service.check_off_habit("Test Daily", d)

        habit_name, streak = self.analytics_service. get_longest_streak_all_habits()
        self.assertEqual(habit_name, "Test Daily")
        self.assertEqual(streak, 5)

    def test_validation_empty_name(self):
        """Test that empty habit names are rejected"""
        success, message = self.habit_service.create_habit("", "daily")
        self.assertFalse(success)
        self.assertIn("empty", message. lower())

    def test_validation_invalid_periodicity(self):
        """Test that invalid periodicity is rejected"""
        success, message = self.habit_service.create_habit("Test", "monthly")
        self.assertFalse(success)
        self.assertIn("periodicity", message.lower())

    def test_validation_duplicate_name(self):
        """Test that duplicate habit names are rejected"""
        success, message = self. habit_service.create_habit("Test Daily", "daily")
        self.assertFalse(success)
        self.assertIn("already exists", message.lower())

    def test_validation_future_checkoff(self):
        """Test that future check-offs are rejected"""
        future_date = datetime.now() + timedelta(days=1)
        success, message = self.tracker_service.check_off_habit("Test Daily", future_date)
        self.assertFalse(success)
        self.assertIn("future", message.lower())


if __name__ == '__main__':
    unittest.main()