"""
Test suite for Habit Tracker application
"""
import unittest
import sqlite3
from datetime import datetime, timedelta
from services.habit_service import HabitService
from services.tracker_service import TrackerService
from services. analytics_service import AnalyticsService
from repositories.habit_repository import HabitRepository
from repositories.tracker_repository import TrackerRepository


class TestHabitTracker(unittest.TestCase):
    """Test cases for Habit Tracker application"""

    def setUp(self):
        """Set up test database and services"""
        # Create in-memory database
        self.db = sqlite3.connect(":memory:")
        self.db.execute("PRAGMA foreign_keys = ON")

        # Create schema directly
        self._create_schema()

        # Initialize repositories
        self.habit_repo = HabitRepository(self. db)
        self.tracker_repo = TrackerRepository(self. db)

        # Initialize services
        self.habit_service = HabitService(self.db)
        self.tracker_service = TrackerService(self.db)
        self.analytics_service = AnalyticsService(self. db)

        # Create test habits with descriptions
        self.habit_service.create_habit("Test Daily", "daily", "Daily test habit")
        self.habit_service.create_habit("Test Weekly", "weekly", "Weekly test habit")

    def _create_schema(self):
        """Create database schema for testing"""
        cur = self.db.cursor()

        # Create habits table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS habits (
                habit_id TEXT PRIMARY KEY,
                name TEXT NOT NULL UNIQUE,
                periodicity TEXT NOT NULL,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                description TEXT DEFAULT '',
                is_active INTEGER DEFAULT 1
            )
        """)

        # Create tracker table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS tracker (
                event_id TEXT PRIMARY KEY,
                habit_id TEXT NOT NULL,
                checked_at TEXT NOT NULL,
                notes TEXT DEFAULT '',
                FOREIGN KEY (habit_id) REFERENCES habits(habit_id) ON DELETE CASCADE
            )
        """)

        # Create indexes
        cur.execute("CREATE INDEX IF NOT EXISTS idx_habit_name ON habits(name)")
        cur.execute("CREATE INDEX IF NOT EXISTS idx_tracker_habit ON tracker(habit_id)")
        cur.execute("CREATE INDEX IF NOT EXISTS idx_tracker_date ON tracker(checked_at)")

        self.db.commit()
    def tearDown(self):
        """Clean up test database"""
        self.db. close()

    def test_habit_creation(self):
        """Test that habits are created correctly"""
        habits = self.habit_service.get_all_habits()
        self.assertEqual(len(habits), 2)
        self.assertEqual(habits[0].name, "Test Daily")

    def test_habit_creation_with_description(self):
        """Test creating a habit with description"""
        success, message = self.habit_service. create_habit(
            "Morning Yoga",
            "daily",
            "30 minutes of yoga every morning"
        )
        self.assertTrue(success)

        habit = self.habit_service.get_habit_by_name("Morning Yoga")
        self.assertIsNotNone(habit)
        self.assertEqual(habit.description, "30 minutes of yoga every morning")

    def test_habit_has_id(self):
        """Test that habits have unique IDs"""
        habit = self.habit_service.get_habit_by_name("Test Daily")
        self.assertIsNotNone(habit. habit_id)
        self.assertTrue(len(habit.habit_id) > 0)

    def test_habit_default_active_status(self):
        """Test that new habits are active by default"""
        habit = self.habit_service. get_habit_by_name("Test Daily")
        self.assertTrue(habit.is_active)

    def test_check_off(self):
        """Test checking off a habit"""
        success, message = self.tracker_service.check_off_habit("Test Daily", datetime.now())
        self.assertTrue(success)

        # Verify event was recorded
        habit = self.habit_service.get_habit_by_name("Test Daily")
        events = self.tracker_repo.find_by_habit_id(habit.habit_id)
        self.assertEqual(len(events), 1)

    def test_check_off_with_notes(self):
        """Test checking off a habit with notes"""
        success, message = self.tracker_service.check_off_habit(
            "Test Daily",
            datetime.now(),
            "Felt great today!"
        )
        self.assertTrue(success)

        # Verify notes were saved
        habit = self.habit_service.get_habit_by_name("Test Daily")
        events = self.tracker_repo.find_by_habit_id(habit.habit_id)
        self.assertEqual(len(events), 1)
        self.assertEqual(events[0].notes, "Felt great today!")

    def test_daily_streak_calculation(self):
        """Test streak calculation for daily habits"""
        # Day 1: Done
        d1 = datetime. now() - timedelta(days=2)
        self.tracker_service.check_off_habit("Test Daily", d1)

        # Day 2: Done (Consecutive)
        d2 = datetime. now() - timedelta(days=1)
        self.tracker_service.check_off_habit("Test Daily", d2)

        # Day 3: Done (Consecutive)
        d3 = datetime.now()
        self.tracker_service. check_off_habit("Test Daily", d3)

        streak = self.analytics_service.calculate_longest_streak("Test Daily")
        self.assertEqual(streak, 3)

    def test_broken_streak(self):
        """Test that broken streaks are calculated correctly"""
        # Day 1: Done
        d1 = datetime.now() - timedelta(days=5)
        self.tracker_service.check_off_habit("Test Daily", d1)

        # Gap of 3 days (days 2, 3, 4 missed)

        # Day 5: Done (new streak starts)
        d2 = datetime.now() - timedelta(days=1)
        self.tracker_service.check_off_habit("Test Daily", d2)

        # Day 6: Done (consecutive)
        d3 = datetime.now()
        self.tracker_service.check_off_habit("Test Daily", d3)

        streak = self.analytics_service.calculate_longest_streak("Test Daily")
        # Max streak should be 2 (days 5-6), not 3
        self.assertEqual(streak, 2)

    def test_weekly_streak_calculation(self):
        """Test streak calculation for weekly habits"""
        # Week 1
        w1 = datetime.now() - timedelta(weeks=2)
        self.tracker_service.check_off_habit("Test Weekly", w1)

        # Week 2
        w2 = datetime.now() - timedelta(weeks=1)
        self.tracker_service.check_off_habit("Test Weekly", w2)

        # Week 3
        w3 = datetime.now()
        self.tracker_service.check_off_habit("Test Weekly", w3)

        streak = self.analytics_service.calculate_longest_streak("Test Weekly")
        self.assertEqual(streak, 3)

    def test_habit_update(self):
        """Test updating a habit"""
        success, message = self.habit_service.update_habit(
            "Test Daily",
            "Updated Daily",
            "weekly",
            True,
            "Updated description"
        )
        self.assertTrue(success)

        updated_habit = self.habit_service. get_habit_by_name("Updated Daily")
        self.assertIsNotNone(updated_habit)
        self.assertEqual(updated_habit.periodicity, "weekly")
        self.assertEqual(updated_habit.description, "Updated description")

    def test_habit_update_with_status(self):
        """Test updating habit status (active/inactive)"""
        # Update to inactive
        success, message = self. habit_service.update_habit(
            "Test Daily",
            "Test Daily",
            "daily",
            False,
            "Updated description"
        )
        self.assertTrue(success)

        habit = self.habit_service.get_habit_by_name("Test Daily")
        self.assertFalse(habit.is_active)

    def test_habit_soft_delete(self):
        """Test soft deleting a habit"""
        success, message = self.habit_service.delete_habit("Test Daily", soft_delete=True)
        self.assertTrue(success)

        # Should not appear in active habits
        active_habits = self.habit_service.get_all_habits(include_inactive=False)
        self.assertEqual(len(active_habits), 1)
        self.assertNotIn("Test Daily", [h.name for h in active_habits])

        # Should appear when including inactive
        all_habits = self.habit_service.get_all_habits(include_inactive=True)
        self.assertEqual(len(all_habits), 2)

        # Verify it's marked as inactive
        deleted_habit = self.habit_repo.find_by_name("Test Daily")
        self.assertIsNotNone(deleted_habit)
        self.assertFalse(deleted_habit. is_active)

    def test_habit_hard_delete(self):
        """Test permanently deleting a habit"""
        success, message = self.habit_service.delete_habit("Test Daily", soft_delete=False)
        self.assertTrue(success)

        # Should not exist at all
        habits = self.habit_service.get_all_habits(include_inactive=True)
        self.assertEqual(len(habits), 1)
        self.assertNotIn("Test Daily", [h.name for h in habits])

    def test_soft_deleted_habit_retains_data(self):
        """Test that soft-deleted habits retain their tracking data"""
        # Add some completions
        for i in range(3):
            d = datetime. now() - timedelta(days=i)
            self.tracker_service.check_off_habit("Test Daily", d)

        # Get habit and count events
        habit = self.habit_service.get_habit_by_name("Test Daily")
        events_before = self.tracker_repo.find_by_habit_id(habit.habit_id)
        self.assertEqual(len(events_before), 3)

        # Soft delete
        self.habit_service.delete_habit("Test Daily", soft_delete=True)

        # Data should still exist
        deleted_habit = self.habit_repo.find_by_name("Test Daily")
        events_after = self.tracker_repo.find_by_habit_id(deleted_habit.habit_id)
        self.assertEqual(len(events_after), 3)

    def test_get_by_periodicity(self):
        """Test filtering habits by periodicity"""
        daily_habits = self.habit_service. get_habits_by_periodicity("daily")
        weekly_habits = self.habit_service.get_habits_by_periodicity("weekly")

        self.assertEqual(len(daily_habits), 1)
        self.assertEqual(len(weekly_habits), 1)
        self.assertEqual(daily_habits[0].name, "Test Daily")
        self.assertEqual(weekly_habits[0].name, "Test Weekly")

    def test_get_by_periodicity_excludes_inactive(self):
        """Test that periodicity filter excludes inactive habits by default"""
        # Archive one daily habit
        self.habit_service.delete_habit("Test Daily", soft_delete=True)

        daily_habits = self.habit_service.get_habits_by_periodicity("daily", include_inactive=False)
        self.assertEqual(len(daily_habits), 0)

        # Should appear when including inactive
        daily_all = self.habit_service.get_habits_by_periodicity("daily", include_inactive=True)
        self.assertEqual(len(daily_all), 1)

    def test_longest_streak_all_habits(self):
        """Test getting the longest streak across all habits"""
        # Add check-offs for daily habit (5 consecutive days)
        for i in range(5):
            d = datetime. now() - timedelta(days=i)
            self.tracker_service.check_off_habit("Test Daily", d)

        # Add check-offs for weekly habit (2 consecutive weeks)
        for i in range(2):
            w = datetime. now() - timedelta(weeks=i)
            self.tracker_service.check_off_habit("Test Weekly", w)

        habit_name, streak = self.analytics_service.get_longest_streak_all_habits()
        self.assertEqual(habit_name, "Test Daily")
        self.assertEqual(streak, 5)

    def test_longest_streak_only_active_habits(self):
        """Test that longest streak only considers active habits"""
        # Create completions for both habits
        for i in range(5):
            d = datetime.now() - timedelta(days=i)
            self.tracker_service.check_off_habit("Test Daily", d)

        for i in range(3):
            d = datetime.now() - timedelta(days=i)
            self.tracker_service.check_off_habit("Test Weekly", d)

        # Archive the habit with longer streak
        self.habit_service.delete_habit("Test Daily", soft_delete=True)

        # Should now return Test Weekly as champion
        habit_name, streak = self.analytics_service.get_longest_streak_all_habits()
        self.assertEqual(habit_name, "Test Weekly")

    def test_validation_empty_name(self):
        """Test that empty habit names are rejected"""
        success, message = self.habit_service.create_habit("", "daily")
        self.assertFalse(success)
        self.assertIn("empty", message.lower())

    def test_validation_whitespace_name(self):
        """Test that whitespace-only names are rejected"""
        success, message = self.habit_service.create_habit("   ", "daily")
        self.assertFalse(success)
        self.assertIn("empty", message.lower())

    def test_validation_invalid_periodicity(self):
        """Test that invalid periodicity is rejected"""
        success, message = self.habit_service.create_habit("Test", "monthly")
        self.assertFalse(success)
        self.assertIn("periodicity", message.lower())

    def test_validation_duplicate_name(self):
        """Test that duplicate habit names are rejected"""
        success, message = self.habit_service. create_habit("Test Daily", "daily")
        self.assertFalse(success)
        self.assertIn("already exists", message.lower())

    def test_validation_future_checkoff(self):
        """Test that future check-offs are rejected"""
        future_date = datetime.now() + timedelta(days=1)
        success, message = self.tracker_service.check_off_habit("Test Daily", future_date)
        self.assertFalse(success)
        self.assertIn("future", message.lower())

    def test_validation_nonexistent_habit(self):
        """Test that checking off non-existent habit fails"""
        success, message = self.tracker_service.check_off_habit("Nonexistent", datetime.now())
        self.assertFalse(success)
        self.assertIn("not found", message.lower())

    def test_inactive_habit_cannot_be_checked_off(self):
        """Test that inactive habits cannot be checked off"""
        # Archive the habit
        self.habit_service.delete_habit("Test Daily", soft_delete=True)

        # Try to check it off
        success, message = self.tracker_service.check_off_habit("Test Daily", datetime. now())
        self.assertFalse(success)
        self.assertIn("inactive", message.lower())

    def test_reactivate_archived_habit(self):
        """Test that archived habits can be reactivated"""
        # Archive the habit
        self.habit_service. delete_habit("Test Daily", soft_delete=True)

        # Verify it's inactive
        habit = self.habit_repo.find_by_name("Test Daily")
        self.assertFalse(habit.is_active)

        # Reactivate via update
        success, message = self. habit_service.update_habit(
            "Test Daily",
            "Test Daily",
            "daily",
            True,
            "Daily test habit"
        )
        self.assertTrue(success)

        # Verify it's now active
        reactivated = self.habit_service.get_habit_by_name("Test Daily")
        self.assertIsNotNone(reactivated)
        self.assertTrue(reactivated.is_active)

    def test_functional_sorting_daily_before_weekly(self):
        """Test that functional sorting puts daily habits before weekly"""
        # Create additional habits
        self.habit_service.create_habit("Another Daily", "daily")
        self.habit_service.create_habit("Another Weekly", "weekly")

        habits = self.habit_service.get_all_habits()

        # First two should be daily
        self.assertEqual(habits[0].periodicity, "daily")
        self.assertEqual(habits[1].periodicity, "daily")

        # Last two should be weekly
        self. assertEqual(habits[2].periodicity, "weekly")
        self.assertEqual(habits[3].periodicity, "weekly")

    def test_completion_summary(self):
        """Test getting completion summary for habits"""
        # Add some completions
        for i in range(3):
            d = datetime.now() - timedelta(days=i)
            self.tracker_service.check_off_habit("Test Daily", d, f"Day {i+1}")

        summary = self.analytics_service.get_completion_summary()
        self.assertIsNotNone(summary)
        self.assertGreater(len(summary), 0)

    def test_habit_completion_history(self):
        """Test getting detailed completion history for a habit"""
        # Add completions with notes
        for i in range(3):
            d = datetime.now() - timedelta(days=i)
            self.tracker_service.check_off_habit("Test Daily", d, f"Completion {i+1}")

        history = self.analytics_service.get_habit_completion_history("Test Daily")
        self.assertIsNotNone(history)
        self.assertEqual(history['name'], "Test Daily")
        self.assertEqual(history['periodicity'], "daily")
        self.assertEqual(history['description'], "Daily test habit")
        self.assertEqual(history['total_completions'], 3)
        self.assertTrue('completions' in history)
        self.assertEqual(len(history['completions']), 3)
        # We verify that each event has a valid timestamp
        for event in history['completions']:
            self.assertIsNotNone(event['checked_at'])
            self.assertIsInstance(event['checked_at'], (datetime, str))

# Test fixtures for seeded data
class TestSeedFixtures(unittest.TestCase):
    """Test cases for predefined seed data fixtures"""

    def setUp(self):
        """Set up test database with seed data"""
        from utils.seed_data import seed_predefined_data

        # Create in-memory database
        self.db = sqlite3.connect(":memory:")
        self.db.execute("PRAGMA foreign_keys = ON")

        # Create schema
        self._create_schema()

        # Initialize repositories and services
        self.habit_repo = HabitRepository(self.db)
        self.tracker_repo = TrackerRepository(self.db)
        self.habit_service = HabitService(self.db)
        self.analytics_service = AnalyticsService(self.db)

        # Seed the database
        seed_predefined_data(self.db)

    def _create_schema(self):
        """Create database schema for testing"""
        cur = self.db.cursor()

        # Create habits table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS habits (
                habit_id TEXT PRIMARY KEY,
                name TEXT NOT NULL UNIQUE,
                periodicity TEXT NOT NULL,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                is_active INTEGER DEFAULT 1,
                description TEXT DEFAULT ''
            )
        """)

        # Create tracker table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS tracker (
                event_id TEXT PRIMARY KEY,
                habit_id TEXT NOT NULL,
                checked_at TEXT NOT NULL,
                notes TEXT DEFAULT '',
                FOREIGN KEY (habit_id) REFERENCES habits(habit_id) ON DELETE CASCADE
            )
        """)

        # Create indexes
        cur.execute("CREATE INDEX IF NOT EXISTS idx_habit_name ON habits(name)")
        cur.execute("CREATE INDEX IF NOT EXISTS idx_tracker_habit ON tracker(habit_id)")
        cur.execute("CREATE INDEX IF NOT EXISTS idx_tracker_date ON tracker(checked_at)")

        self.db.commit()

    def tearDown(self):
        """Clean up test database"""
        self. db.close()

    def test_seed_creates_five_habits(self):
        """Test that seeding creates exactly 5 habits"""
        all_habits = self.habit_service.get_all_habits(include_inactive=True)
        self.assertEqual(len(all_habits), 5)

    def test_seed_creates_four_active_habits(self):
        """Test that 4 habits are active"""
        active_habits = self.habit_service.get_all_habits(include_inactive=False)
        self.assertEqual(len(active_habits), 4)

    def test_read_journal_perfect_streak(self):
        """Test Read Journal has perfect 28-day streak"""
        streak = self.analytics_service.calculate_longest_streak("Read Journal")
        self.assertEqual(streak, 28)

    def test_skin_care_is_inactive(self):
        """Test that Skin Care is inactive"""
        skin_care = self.habit_repo.find_by_name("Skin Care")
        self.assertIsNotNone(skin_care)
        self.assertFalse(skin_care. is_active)

    def test_skin_care_has_historical_data(self):
        """Test that Skin Care retains historical data even when inactive"""
        skin_care = self.habit_repo.find_by_name("Skin Care")
        self.assertIsNotNone(skin_care, "Skin Care should exist")
        events = self.tracker_repo.find_by_habit_id(skin_care.habit_id)
        # Should have around 19-20 events (3 weeks - 2 missed days)
        self.assertGreaterEqual(len(events), 19, "Should have at least 19 completions")
        self.assertLessEqual(len(events), 20, "Should have at most 20 completions")

    def test_skin_care_longest_streak(self):
        """Test Skin Care has an 11-day longest streak"""
        streak = self.analytics_service.calculate_longest_streak("Skin Care")
        self.assertEqual(streak, 11)

    def test_play_music_streak(self):
        """Test Play Music has 4-day longest streak"""
        streak = self.analytics_service.calculate_longest_streak("Play Music")
        self.assertEqual(streak, 4)

    def test_finance_check_perfect_weekly_streak(self):
        """Test Finance Check has perfect 4-week streak"""
        streak = self.analytics_service.calculate_longest_streak("Finance Check")
        self.assertEqual(streak, 4)

    def test_water_plants_broken_streak(self):
        """Test Water Plants has 2-week longest streak (missed week 2)"""
        streak = self.analytics_service.calculate_longest_streak("Water Plants")
        self.assertEqual(streak, 2)

    def test_champion_is_read_journal(self):
        """Test that Read Journal is the champion habit"""
        champion_name, champion_streak = self.analytics_service.get_longest_streak_all_habits()
        self.assertEqual(champion_name, "Read Journal")
        self.assertEqual(champion_streak, 28)

    def test_all_habits_have_descriptions(self):
        """Test that all seeded habits have descriptions"""
        all_habits = self.habit_service.get_all_habits(include_inactive=True)
        for habit in all_habits:
            self.assertIsNotNone(habit.description)
            self.assertGreater(len(habit.description), 0)


if __name__ == '__main__':
    unittest.main()