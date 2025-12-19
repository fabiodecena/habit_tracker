"""
Main menu controller
"""
from controllers.habit_controller import HabitController
from controllers.tracker_controller import TrackerController
from controllers.analytics_controller import AnalyticsController
from controllers.completion_controller import CompletionController
from controllers.manage_habits_controller import ManageHabitsController
from controllers.track_progress_controller import TrackProgressController
from controllers.analytics_reports_controller import AnalyticsReportsController
from views.console_view import ConsoleView


class MenuController:
    """Handles main menu navigation"""

    def __init__(self, db):
        """
        Initialize menu controller.

        Args:
            db: Database connection
        """
        self.view = ConsoleView()

        # Initialize base controllers
        self.habit_controller = HabitController(db, self.view)
        self.tracker_controller = TrackerController(db, self.view)
        self.analytics_controller = AnalyticsController(db, self.view)
        self.completion_controller = CompletionController(db, self.view)

        # Initialize submenu controllers
        self.manage_habits_controller = ManageHabitsController(
            self.view,
            self.habit_controller
        )
        self.track_progress_controller = TrackProgressController(
            self.view,
            self.tracker_controller,
            self.completion_controller
        )
        self.analytics_reports_controller = AnalyticsReportsController(
            self.view,
            self.analytics_controller,
            self.habit_controller
        )

    def run(self):
        """Main menu loop"""
        menu_actions = {
            '1': self.manage_habits_controller.run,  # Manage Habits submenu
            '2': self.track_progress_controller.run,  # Track Progress submenu
            '3': self.analytics_reports_controller.run,  # Analytics & Reports submenu
        }

        while True:
            self.view.show_menu()
            choice = self.view.get_menu_choice()

            if choice == '4':  # Exit
                self.view.show_goodbye()
                break
            elif choice in menu_actions:
                menu_actions[choice]()
            else:
                self.view.show_invalid_choice()