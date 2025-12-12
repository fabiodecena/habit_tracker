"""
Analytics Controller - Coordinates analytics operations
"""
from views.console_view import ConsoleView
from services.habit_service import HabitService
from services.analytics_service import AnalyticsService


class AnalyticsController:
    """
    Controller for analytics operations.
    """

    def __init__(self, view: ConsoleView, db=None):
        """
        Initialize the controller.

        Args:
            view: ConsoleView instance
            db: Database connection (optional)
        """
        self.view = view
        self.habit_service = HabitService(db)
        self.analytics_service = AnalyticsService(db)

    def show_longest_streak_all(self):
        """Display the habit with the longest streak."""
        habit_name, streak = self.analytics_service.get_longest_streak_all_habits()
        self.view.show_longest_streak_all(habit_name, streak)

    def show_longest_streak_specific(self):
        """Display streak for a specific habit."""
        self.view.show_header("🎯 [bold gold1]Specific habit streak analysis[/bold gold1]")

        name = self.view.get_habit_name()
        habit = self.habit_service.get_habit_by_name(name)

        if habit:
            streak = self.analytics_service.calculate_longest_streak(name)
            self.view.show_longest_streak_specific(name, streak)
        else:
            self.view.show_habit_not_found(name)