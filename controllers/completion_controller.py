"""
Completion Controller - Coordinates completion table operations
"""
from views.console_view import ConsoleView
from services.habit_service import HabitService
from services.analytics_service import AnalyticsService


class CompletionController:
    """
    Controller for completion table operations.
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

    def show_completion_table(self):
        """Display completion summary table with an option to view details."""
        while True:
            # Get a completion summary for all habits
            summary_data = self.analytics_service.get_completion_summary()

            if not summary_data:
                self.view.show_no_habits_found()
                return

            # Show the summary table
            self.view.show_completion_table(summary_data)

            # Ask the user to select a habit for a detailed view
            choice = self.view.get_number_choice(
                "Enter the number of a habit to view detailed history (or 'q' to quit): "
            )

            if choice.lower() == 'q':
                return

            try:
                choice_num = int(choice)
                if 1 <= choice_num <= len(summary_data):
                    selected_habit_name = summary_data[choice_num - 1]['name']

                    # Get a detailed history
                    habit_data = self.analytics_service.get_habit_completion_history(selected_habit_name)

                    if habit_data:
                        self.view.show_habit_completion_history(habit_data)

                        # Ask if the user wants to continue
                        continue_choice = self.view.get_confirmation(
                            "Press Enter to return to completion table (or 'q' to quit): "
                        )

                        if continue_choice.lower() == 'q':
                            return
                    else:
                        self.view.show_error("Habit not found.")
                        return
                else:
                    self.view.show_error(
                        f"Invalid number.  Please enter a number between 1 and {len(summary_data)}."
                    )
                    self.view.show_retry_message()
            except ValueError:
                self.view.show_error("Invalid input. Please enter a number.")
                self.view.show_retry_message()

    def edit_completion_notes(self):
        """Edit notes for a specific completion."""
        while True:
            self.view.show_header("✏️  [bold yellow]Edit Completion Notes[/bold yellow]")

            # Get all habits
            habits = self.habit_service.get_all_habits()
            if not habits:
                self.view.show_no_habits_found()
                return

            # Show habits
            habit_tuples = [(h.name, h.periodicity) for h in habits]
            self.view.show_habits_numbered_list(habit_tuples)

            habit_choice = self.view.get_number_choice(
                "\nEnter the number of the habit (or 'q' to quit): "
            )

            if habit_choice.lower() == 'q':
                return

            try:
                habit_num = int(habit_choice)
                if 1 <= habit_num <= len(habits):
                    selected_habit_name = habits[habit_num - 1].name

                    # Get completion history
                    habit_data = self.analytics_service.get_habit_completion_history(selected_habit_name)

                    if not habit_data or not habit_data['completions']:
                        self.view.console.print("\n  [dim]No completions found for this habit.[/dim]\n")
                        return

                    # Show completions
                    self.view.show_habit_completion_history(habit_data)

                    # Ask which completion to edit
                    completion_choice = self.view.get_number_choice(
                        "Enter the number of the completion to edit (or 'q' to quit): "
                    )

                    if completion_choice.lower() == 'q':
                        return

                    try:
                        completion_num = int(completion_choice)
                        if 1 <= completion_num <= len(habit_data['completions']):
                            selected_completion = habit_data['completions'][completion_num - 1]

                            # Show current notes
                            current_notes = selected_completion['notes'] or "(no notes)"
                            self.view.console.print(f"\n[bold]Current notes:[/bold] [italic]{current_notes}[/italic]")

                            # Get new notes
                            new_notes = self.view.console.input("\nEnter new notes (press Enter to clear): ").strip()

                            # Update notes
                            from services.tracker_service import TrackerService
                            tracker_service = TrackerService(self.habit_service.repository.db)

                            success, message = tracker_service.update_completion_notes(
                                selected_completion['event_id'],
                                new_notes
                            )

                            if success:
                                self.view.console.print("\n✅ [green]Notes updated successfully![/green]\n")
                            else:
                                self.view.show_error(message)
                            return
                        else:
                            self.view.show_error(
                                f"Invalid number.  Please enter between 1 and {len(habit_data['completions'])}."
                            )
                            self.view.show_retry_message()
                    except ValueError:
                        self.view.show_error("Invalid input. Please enter a number.")
                        self.view.show_retry_message()
                else:
                    self.view.show_error(
                        f"Invalid number. Please enter between 1 and {len(habits)}."
                    )
                    self.view.show_retry_message()
            except ValueError:
                self.view.show_error("Invalid input. Please enter a number.")
                self.view.show_retry_message()