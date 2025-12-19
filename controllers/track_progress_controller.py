"""
Track Progress submenu controller
"""
from database import Database
from services import HabitService, AnalyticsService


class TrackProgressController:
    """Handles progress tracking submenu navigation"""

    def __init__(self, view, tracker_controller, completion_controller):
        """
        Initialize track progress controller.

        Args:
            view: ConsoleView instance
            tracker_controller: TrackerController instance
            completion_controller: CompletionController instance
        """
        self.view = view
        self.tracker_controller = tracker_controller
        self.completion_controller = completion_controller

    def run(self):
        """Track progress submenu loop"""
        actions = {
            '1': self.tracker_controller.check_off_habit,
            '2': self.completion_controller.show_completion_table,
            '3': self.completion_controller.edit_completion_notes,
        }

        while True:
            self.view.show_track_progress_menu()
            choice = self.view.get_submenu_choice().lower()

            if choice == '4':
                break  # Back to the main menu

            action = actions.get(choice)
            if action:
                action()
            else:
                self.view.show_invalid_choice()