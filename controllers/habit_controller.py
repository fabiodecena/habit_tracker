"""
Habit Controller - Coordinates habit operations
"""
from views.console_view import ConsoleView
from services.habit_service import HabitService


class HabitController:
    """
    Controller for habit-related operations.
    """

    def __init__(self, view: ConsoleView, db=None):
        """
        Initialize the controller.

        Args:
            view: ConsoleView instance
            db: Database connection (optional)
        """
        self.view = view
        self.service = HabitService(db)

    def create_habit(self):
        """Interactive habit creation with optional comments."""
        self.view.show_header("✨ [bold cyan]Create a new habit[/bold cyan]")

        name = self.view.get_habit_name()
        periodicity = self.view.get_periodicity()

        # Ask if the user wants to add comments
        add_comments = self.view.get_confirmation(
            "\nDo you want to add a description/comment for this habit?  (y/n): "
        )

        comments = ""
        if add_comments.lower() == 'y':
            comments = self.view.get_habit_comments()

        success, message = self.service.create_habit(name, periodicity, comments)

        if success:
            self.view.show_habit_created(name)
            if comments:
                self.view.console.print(f"   💬 Description: [italic]{comments}[/italic]", style="dim cyan")
        else:
            self.view.show_error(message)

    def delete_habit(self):
        """Interactive habit deletion with numbered selection."""
        while True:
            self.view.show_header("🗑️  [bold red]Delete a habit[/bold red]")

            habits = self.service.get_all_habits()
            if not habits:
                self.view.show_no_habits_found()
                return

            # Convert to tuples for display
            habit_tuples = [(h.name, h.periodicity) for h in habits]
            self.view.show_habits_numbered_list(habit_tuples)

            choice = self.view.get_number_choice(
                "\nEnter the number of the habit to delete (or 'q' to quit): "
            )

            if choice.lower() == 'q':
                return

            try:
                choice_num = int(choice)
                if 1 <= choice_num <= len(habits):
                    selected_habit = habits[choice_num - 1]
                    name = selected_habit.name

                    # Add confirmation to prevent accidental deletion
                    confirm = self.view.get_confirmation(
                        f"\n⚠️  Are you sure you want to delete '{name}'?  (y/n): "
                    )

                    if confirm.lower() != 'y':
                        self.view.console.print("\n❌ Deletion cancelled.", style="yellow")
                        return

                    success, message = self.service.delete_habit(name)

                    if success:
                        self.view.show_habit_deleted(name)
                    else:
                        self.view.show_error(message)
                    return
                else:
                    self.view.show_error(
                        f"Invalid number. Please enter a number between 1 and {len(habits)}."
                    )
                    self.view.show_retry_message()
            except ValueError:
                self.view.show_error("Invalid input. Please enter a number.")
                self.view.show_retry_message()

    def edit_habit(self):
        """Interactive habit editing with numbered selection."""
        while True:
            self.view.show_header("✏️  [bold yellow]Edit a habit[/bold yellow]")

            habits = self.service.get_all_habits()
            if not habits:
                self.view.show_no_habits_found()
                return

            # Convert to tuples for display
            habit_tuples = [(h.name, h.periodicity) for h in habits]
            self.view.show_habits_numbered_list(habit_tuples)

            choice = self.view.get_number_choice(
                "\nEnter the number of the habit to edit (or 'q' to quit): "
            )

            if choice.lower() == 'q':
                return

            try:
                choice_num = int(choice)
                if 1 <= choice_num <= len(habits):
                    selected_habit = habits[choice_num - 1]

                    # Show current habit info including comments
                    self.view.show_current_habit_info(
                        selected_habit.name,
                        selected_habit.periodicity,
                        selected_habit.comments
                    )

                    # Get new values
                    new_name = self.view.get_new_name(selected_habit.name)
                    new_periodicity = self.view.get_new_periodicity(selected_habit.periodicity)
                    new_comments = self.view.get_new_comments(selected_habit.comments)

                    # Keep current values if the user pressed Enter
                    if not new_name:
                        new_name = selected_habit.name
                    if not new_periodicity:
                        new_periodicity = selected_habit.periodicity
                    if new_comments is None:  # User skipped
                        new_comments = selected_habit.comments

                    # Update habit
                    success, message = self.service.update_habit(
                        selected_habit.name,
                        new_name,
                        new_periodicity,
                        new_comments
                    )

                    if success:
                        self.view.show_habit_updated(selected_habit.name, new_name, new_periodicity)
                    else:
                        self.view.show_error(message)
                    return
                else:
                    self.view.show_error(
                        f"Invalid number.  Please enter a number between 1 and {len(habits)}."
                    )
                    self.view.show_retry_message()
            except ValueError:
                self.view.show_error("Invalid input. Please enter a number.")
                self.view.show_retry_message()

    def list_all_habits(self):
        """Display all habits with icon, name, periodicity, and comments."""
        habits = self.service.get_all_habits()
        # Convert to tuples with comments: (name, periodicity, comments)
        habit_tuples = [(h.name, h.periodicity, h.comments) for h in habits]
        self.view.show_habits_list(habit_tuples)

    def list_habits_by_periodicity(self):
        """Display habits filtered by periodicity with menu selection."""
        while True:
            self.view.show_header("🔍 [bold blue]Filter habits by periodicity[/bold blue]")

            # Show periodicity options
            self.view.show_periodicity_menu()

            choice = self.view.get_number_choice(
                "\nEnter your choice (1-2, or 'q' to quit): "
            )

            if choice.lower() == 'q':
                return

            try:
                choice_num = int(choice)
                if choice_num == 1:
                    periodicity = 'daily'
                elif choice_num == 2:
                    periodicity = 'weekly'
                else:
                    self.view.show_error(
                        "Invalid choice. Please enter 1 for daily or 2 for weekly."
                    )
                    self.view.show_retry_message()
                    continue

                # Get and display filtered habits
                habits = self.service.get_habits_by_periodicity(periodicity)
                habit_tuples = [(h.name, h.periodicity) for h in habits]
                self.view.show_filtered_habits(periodicity, habit_tuples)
                return

            except ValueError:
                self.view.show_error("Invalid input. Please enter a number (1 or 2).")
                self.view.show_retry_message()