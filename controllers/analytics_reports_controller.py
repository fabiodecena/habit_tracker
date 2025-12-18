"""
Analytics & Reports submenu controller
"""
from database import Database
from services import AnalyticsService

class AnalyticsReportsController:
    """Handles analytics and reports submenu navigation"""

    def __init__(self, view, analytics_controller):
        """
        Initialize analytics reports controller.

        Args:
            view: ConsoleView instance
            analytics_controller: AnalyticsController instance
        """
        self.view = view
        self. analytics_controller = analytics_controller

    def run(self):
        """Analytics & reports submenu loop"""
        actions = {
            '1': self.analytics_controller.show_longest_streak_all,
            '2': self.analytics_controller.show_longest_streak_specific,
            '3': self._show_completion_statistics,
        }

        while True:
            self.view.show_analytics_reports_menu()
            choice = self.view.get_submenu_choice().lower()

            if choice == '4':
                break  # Back to the main menu

            action = actions.get(choice)
            if action:
                action()
            else:
                self.view.show_invalid_choice()

    def _show_completion_statistics(self):
        """Display comprehensive completion statistics for all habits"""

        db = Database.get_connection()
        analytics_service = AnalyticsService(db)

        summary = analytics_service.get_completion_summary()
        self.view.show_completion_statistics(summary)
        db.close()