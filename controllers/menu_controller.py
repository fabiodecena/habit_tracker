"""
Menu Controller - Handles main menu navigation
"""
from views.console_view import ConsoleView
from controllers.habit_controller import HabitController
from controllers.tracker_controller import TrackerController
from controllers.analytics_controller import AnalyticsController
from controllers.completion_controller import CompletionController  # NEW


class MenuController:
    """
    Main menu controller that coordinates all operations.
    """

    def __init__(self, db=None):
        """
        Initialize the menu controller.

        Args:
            db: Database connection (optional)
        """
        self.db = db
        self.view = ConsoleView()
        self.habit_controller = HabitController(self.view, db)
        self.tracker_controller = TrackerController(self.view, db)
        self.analytics_controller = AnalyticsController(self.view, db)
        self.completion_controller = CompletionController(self.view, db)  # NEW

    def run(self):
        """Main menu loop."""
        # Define menu actions mapping
        menu_actions = {
            '1': self.habit_controller.create_habit,
            '2': self.habit_controller.delete_habit,
            '3': self.tracker_controller.check_off_habit,
            '4': self.habit_controller.edit_habit,
            '5': self.habit_controller.list_active_habits,
            '6': self.habit_controller.list_all_habits_including_inactive,
            '7': self.habit_controller.list_habits_by_periodicity,
            '8': self.analytics_controller.show_longest_streak_all,
            '9': self.analytics_controller.show_longest_streak_specific,
            '10': self.completion_controller.show_completion_table,
            '11': self.completion_controller.edit_completion_notes,
        }

        while True:
            self.view.show_menu()
            choice = self.view.get_menu_choice()

            if choice == '12':  # Exit
                self.view.show_goodbye()
                break
            elif choice in menu_actions:
                menu_actions[choice]()  # Call the corresponding method
            else:
                self.view.show_invalid_choice()