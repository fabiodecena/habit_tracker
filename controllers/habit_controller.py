"""
Habit Controller - Coordinates habit operations
"""

from services.habit_service import HabitService


class HabitController:
    """
    Controller for habit-related operations.
    """

    def __init__(self, db, view):
        """
        Initialize the controller.

        Args:
            view: ConsoleView instance
            db: Database connection (optional)
        """
        self.view = view
        self.service = HabitService(db)

    def create_habit(self):
        """Interactive habit creation with optional description."""
        self.view.show_header("✨ [bold cyan]Create a new habit[/bold cyan]")

        name = self.view.get_habit_name()
        periodicity = self.view.get_periodicity()

        # Ask if the user wants to add a description
        add_description = self.view.get_confirmation(
            "\nDo you want to add a description for this habit?  (y/n): "
        )

        description = ""
        if add_description.lower() == 'y':
            description = self.view.get_habit_description()

        success, message = self.service.create_habit(name, periodicity, description)

        if success:
            self.view.show_habit_created(name)
            if description:
                self.view.console.print(f"   💬 Description: [italic]{description}[/italic]", style="dim cyan")
        else:
            self.view.show_error(message)

    def delete_habit(self):
        """Interactive habit deletion with soft/hard delete choice."""
        while True:
            self.view.show_header("🗑️  [bold red]Delete a habit[/bold red]")

            habits = self.service.get_all_habits(include_inactive=True)
            if not habits:
                self.view.show_no_habits_found()
                return

            # Convert to tuples for display
            habit_tuples = [(h.name, h.periodicity, h.is_active) for h in habits]
            self.view.show_habits_numbered_list_with_status(habit_tuples)

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

                    # Ask for a deletion type
                    self.view.console.print()
                    deletion_type = self.view.get_deletion_type()

                    if deletion_type == 'cancel':
                        self.view.console.print("❌ Deletion cancelled.", style="yellow")
                        return

                    # Confirm deletion
                    if deletion_type == 'soft':
                        confirm_message = f"⚠️  Archive '{name}'? (You can restore it later) (y/n): "
                    else:
                        confirm_message = f"⚠️  PERMANENTLY delete '{name}' and all its data? This cannot be undone!  (y/n): "

                    confirm = self.view.get_confirmation(confirm_message)

                    if confirm.lower() != 'y':
                        self.view.console.print("❌ Deletion cancelled.", style="yellow")
                        return

                    # Perform deletion
                    soft_delete = (deletion_type == 'soft')
                    success, message = self.service.delete_habit(name, soft_delete=soft_delete)

                    if success:
                        if soft_delete:
                            self.view.show_habit_archived(name)
                        else:
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

            habits = self.service.get_all_habits(include_inactive=True)
            if not habits:
                self.view.show_no_habits_found()
                return

            # Convert to tuples for display
            habit_tuples = [(h.name, h.periodicity, h.is_active) for h in habits]
            self.view.show_habits_numbered_list_with_status(habit_tuples)

            choice = self.view.get_number_choice(
                "\nEnter the number of the habit to edit (or 'q' to quit): "
            )

            if choice.lower() == 'q':
                return

            try:
                choice_num = int(choice)
                if 1 <= choice_num <= len(habits):
                    selected_habit = habits[choice_num - 1]


                    self.view.show_current_habit_info(
                        selected_habit.name,
                        selected_habit.periodicity,
                        selected_habit.is_active,
                        selected_habit.description
                    )

                    # Get new values
                    new_name = self.view.get_new_name(selected_habit.name)
                    new_periodicity = self.view.get_new_periodicity(selected_habit.periodicity)
                    new_description = self.view.get_new_description(selected_habit.description)
                    new_status = self.view.get_new_status(selected_habit.is_active)

                    # Keep current values if the user pressed Enter
                    if not new_name:
                        new_name = selected_habit.name
                    if not new_periodicity:
                        new_periodicity = selected_habit.periodicity
                    if new_description is None:  # User skipped
                        new_description = selected_habit.description
                    if new_status is None:
                        new_status = selected_habit.is_active

                    # Update habit
                    success, message = self.service.update_habit(
                        selected_habit.name,
                        new_name,
                        new_periodicity,
                        new_status,
                        new_description
                    )

                    if success:
                        self.view.show_habit_updated(selected_habit.name, new_name, new_status, new_periodicity)
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

    def list_all_habits(self, include_inactive=False):
        """
        Display all habits.

        Args:
            include_inactive:  If True, shows inactive habits as well
        """
        habits = self.service.get_all_habits(include_inactive=include_inactive)
        habit_tuples = [(h.name, h.periodicity, h.description, h.is_active) for h in habits]

        if include_inactive:
            self.view.show_all_habits_list(habit_tuples)
        else:
            self.view.show_active_habits_list(habit_tuples)

    def list_active_habits(self):
        """Display only active habits."""
        self.list_all_habits(include_inactive=False)

    def list_all_habits_including_inactive(self):
        """Display all habits including inactive."""
        self.list_all_habits(include_inactive=True)

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