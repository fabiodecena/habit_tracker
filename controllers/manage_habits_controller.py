"""
Manage Habits submenu controller
"""


class ManageHabitsController:
    """Handles habit management submenu navigation"""

    def __init__(self, view, habit_controller):
        """
        Initialize manage habits controller.

        Args:
            view: ConsoleView instance
            habit_controller: HabitController instance
        """
        self.view = view
        self.habit_controller = habit_controller

    def run(self):
        """Manage habits submenu loop"""
        actions = {
            '1': self.habit_controller.create_habit,
            '2': self.habit_controller.edit_habit,
            '3': self.habit_controller.delete_habit
        }

        while True:
            self.view.show_manage_habits_menu()
            choice = self.view.get_submenu_choice()

            if choice == '4':
                break  # Back to the main menu

            action = actions.get(choice)
            if action:
                action()
            else:
                self.view.show_invalid_choice()