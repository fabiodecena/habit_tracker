"""
Tracker Controller - Coordinates tracking operations
"""
from datetime import datetime
from views.console_view import ConsoleView
from services.habit_service import HabitService
from services.tracker_service import TrackerService


class TrackerController:
    """
    Controller for tracking habit completions.
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
        self.tracker_service = TrackerService(db)

    def check_off_habit(self):
        """Interactive habit check-off with optional notes."""
        while True:
            self.view.show_header("✅ [bold green]Check-off a habit[/bold green]")

            habits = self.habit_service.get_all_habits()
            if not habits:
                self.view.show_no_habits_found()
                return

            habit_tuples = [(h.name, h.periodicity) for h in habits]
            self.view.show_habits_numbered_list(habit_tuples)

            choice = self.view.get_number_choice(
                "\nEnter the number of the habit to check-off (or 'q' to quit): "
            )

            if choice. lower() == 'q':
                return

            try:
                choice_num = int(choice)
                if 1 <= choice_num <= len(habits):
                    selected_habit = habits[choice_num - 1]

                    # Ask if the user wants to add notes
                    add_notes = self.view. get_confirmation(
                        "\nDo you want to add notes for this completion? (y/n): "
                    )

                    notes = ""
                    if add_notes.lower() == 'y':
                        notes = self. view.get_completion_notes()

                    success, message = self.tracker_service.check_off_habit(
                        selected_habit. name,
                        datetime.now(),
                        notes
                    )

                    if success:
                        self.view.show_habit_checked_off(selected_habit.name)
                        if notes:
                            self.view.console.print(f"   📝 Notes: [italic]{notes}[/italic]", style="dim")
                    else:
                        self.view.show_error(message)
                    return
                else:
                    self.view.show_error(
                        f"Invalid number.  Please enter a number between 1 and {len(habits)}."
                    )
                    self.view.show_retry_message()
            except ValueError:
                self.view.show_error("Invalid input.  Please enter a number.")
                self.view.show_retry_message()