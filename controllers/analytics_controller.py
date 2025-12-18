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
        """Display a streak for a specific habit with a numbered selection."""
        while True:
            self.view.show_header("🎯 [bold gold1]Specific habit streak analysis[/bold gold1]")

            habits = self.habit_service.get_all_habits()
            if not habits:
                self.view.show_no_habits_found()
                return

            # Convert to tuples for display
            habit_tuples = [(h.name, h.periodicity, h.is_active) for h in habits]
            self.view.show_habits_numbered_list_with_status(habit_tuples)

            choice = self.view.get_number_choice(
                "\nEnter the number of the habit to analyze (or 'q' to quit): "
            )

            if choice.lower() == 'q':
                return

            try:
                choice_num = int(choice)
                if 1 <= choice_num <= len(habits):
                    selected_habit = habits[choice_num - 1]
                    name = selected_habit.name

                    streak = self.analytics_service.calculate_longest_streak(name)

                    # Add a blank line before showing a result
                    self.view.console.print()
                    self.view.show_longest_streak_specific(name, streak)
                    return
                else:
                    self.view.show_error(
                        f"Invalid number. Please enter a number between 1 and {len(habits)}."
                    )
                    self.view.show_retry_message()
            except ValueError:
                self.view.show_error("Invalid input. Please enter a number.")
                self.view.show_retry_message()