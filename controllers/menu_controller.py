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
                self.habit_controller.list_active_habits()  # CHANGED
            elif choice == '6':  # NEW
                self.habit_controller.list_all_habits_including_inactive()
            elif choice == '7':  # Changed from 6
                self.habit_controller.list_habits_by_periodicity()
            elif choice == '8':  # Changed from 7
                self.analytics_controller.show_longest_streak_all()
            elif choice == '9':  # Changed from 8
                self.analytics_controller.show_longest_streak_specific()
            elif choice == '10':  # Changed from 9
                self.completion_controller.show_completion_table()
            elif choice == '11':  # Changed from 10
                self.completion_controller.edit_completion_notes()
            elif choice == '12':  # Changed from 11
                self.view.show_goodbye()
                break
            else:
                self.view.show_invalid_choice()