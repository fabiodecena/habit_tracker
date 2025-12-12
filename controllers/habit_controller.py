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
        """Interactive habit creation."""
        self.view.show_header("✨ [bold cyan]Create a new habit[/bold cyan]")

        name = self.view.get_habit_name()
        periodicity = self.view.get_periodicity()

        success, message = self.service.create_habit(name, periodicity)

        if success:
            self.view.show_habit_created(name)
        else:
            self.view.show_error(message)

    def delete_habit(self):
        """Interactive habit deletion."""
        self.view.show_header("🗑️  [bold red]Delete a habit[/bold red]")

        habits = self.service.get_all_habits()
        if not habits:
            self.view.show_no_habits_found()
            return

        # Convert to tuples for display
        habit_tuples = [(h.name, h.periodicity) for h in habits]
        self.view.show_habits_numbered_list(habit_tuples)

        name = self.view.get_habit_name("\nEnter the name of the habit to delete:  ")

        success, message = self.service.delete_habit(name)

        if success:
            self.view.show_habit_deleted(name)
        else:
            self.view.show_error(message)

    def edit_habit(self):
        """Interactive habit editing."""
        self.view.show_header("✏️  [bold yellow]Edit a habit[/bold yellow]")

        habits = self.service.get_all_habits()
        if not habits:
            self.view.show_no_habits_found()
            return

        habit_tuples = [(h.name, h.periodicity) for h in habits]
        self.view.show_habits_numbered_list(habit_tuples)

        old_name = self.view.get_habit_name("\nEnter the name of the habit to edit: ")

        target_habit = self.service.get_habit_by_name(old_name)
        if not target_habit:
            self.view.show_habit_not_found(old_name)
            return

        self.view.show_current_habit_info(target_habit.name, target_habit.periodicity)

        new_name = self.view.get_new_name(old_name)
        new_periodicity = self.view.get_new_periodicity(target_habit.periodicity)

        # Keep current values if the user pressed Enter
        if not new_name:
            new_name = old_name
        if not new_periodicity:
            new_periodicity = target_habit.periodicity

        success, message = self.service.update_habit(old_name, new_name, new_periodicity)

        if success:
            self.view.show_habit_updated(old_name, new_name, new_periodicity)
        else:
            self.view.show_error(message)

    def list_all_habits(self):
        """Display all habits."""
        habits = self.service.get_all_habits()
        habit_tuples = [(h.name, h.periodicity) for h in habits]
        self.view.show_habits_list(habit_tuples)

    def list_habits_by_periodicity(self):
        """Display habits filtered by periodicity."""
        self.view.show_header("🔍 [bold blue]Filter habits by periodicity[/bold blue]")

        periodicity = self.view.get_periodicity("Which periodicity?   (daily/weekly): ")
        habits = self.service.get_habits_by_periodicity(periodicity)
        habit_tuples = [(h.name, h.periodicity) for h in habits]
        self.view.show_filtered_habits(periodicity, habit_tuples)