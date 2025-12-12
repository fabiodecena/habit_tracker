"""
Menu Controller - Handles main menu navigation
"""
from views.console_view import ConsoleView
from controllers.habit_controller import HabitController
from controllers.tracker_controller import TrackerController
from controllers.analytics_controller import AnalyticsController


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

    def run(self):
        """Main menu loop."""
        while True:
            self.view.show_menu()
            choice = self.view.get_menu_choice()

            if choice == '1':
                self.habit_controller.create_habit()
            elif choice == '2':
                self.habit_controller.delete_habit()
            elif choice == '3':
                self.tracker_controller.check_off_habit()
            elif choice == '4':
                self.habit_controller.edit_habit()
            elif choice == '5':
                self.habit_controller.list_all_habits()
            elif choice == '6':
                self.habit_controller.list_habits_by_periodicity()
            elif choice == '7':
                self.analytics_controller.show_longest_streak_all()
            elif choice == '8':
                self.analytics_controller.show_longest_streak_specific()
            elif choice == '9':
                self.view.show_goodbye()
                break
            else:
                self.view.show_invalid_choice()