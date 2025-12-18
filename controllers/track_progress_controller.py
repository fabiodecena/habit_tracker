"""
Track Progress submenu controller
"""


class TrackProgressController:
    """Handles progress tracking submenu navigation"""

    def __init__(self, view, tracker_controller, completion_controller):
        """
        Initialize track progress controller.

        Args:
            view: ConsoleView instance
            tracker_controller: TrackerController instance
            completion_controller: CompletionController instance
        """
        self.view = view
        self.tracker_controller = tracker_controller
        self.completion_controller = completion_controller

    def run(self):
        """Track progress submenu loop"""
        actions = {
            '1': self.tracker_controller.check_off_habit,
            '2': self.completion_controller.show_completion_table,
            '3': self._show_detailed_history,
            '4': self.completion_controller.edit_completion_notes,
        }

        while True:
            self.view.show_track_progress_menu()
            choice = self.view.get_submenu_choice().lower()

            if choice == '5':
                break  # Back to the main menu

            action = actions.get(choice)
            if action:
                action()
            else:
                self.view.show_invalid_choice()

    def _show_detailed_history(self):
        """Show detailed history for a selected habit"""
        from services.habit_service import HabitService
        from services.analytics_service import AnalyticsService
        from database.connection import Database

        db = Database. get_connection()
        habit_service = HabitService(db)
        analytics_service = AnalyticsService(db)

        # Get all habits
        habits = habit_service.get_all_habits(include_inactive=True)
        if not habits:
            self.view.show_no_habits_found()
            db.close()
            return

        # Show a numbered list
        self.view.show_header("📝 [bold cyan]Select Habit for Detailed History[/bold cyan]")
        habit_tuples = [(h.name, h.periodicity, h.is_active) for h in habits]
        self.view.show_habits_numbered_list_with_status(habit_tuples)

        # Get user selection
        choice = self.view.get_number_choice(
            "\nEnter the number of the habit to view (or 'q' to quit): "
        )

        if choice. lower() == 'q':
            db.close()
            return

        try:
            choice_num = int(choice)
            if 1 <= choice_num <= len(habits):
                selected_habit = habits[choice_num - 1]
                history = analytics_service.get_habit_completion_history(selected_habit.name)

                if history:
                    self.view.show_habit_completion_history(history)
                else:
                    self.view. show_error(f"No history found for '{selected_habit.name}'")
            else:
                self.view.show_error(f"Invalid number.  Please enter 1-{len(habits)}")
        except ValueError:
            self.view.show_error("Invalid input. Please enter a number.")

        db.close()