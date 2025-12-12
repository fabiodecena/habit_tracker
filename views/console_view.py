"""
Console View - Handles all console output and user input
"""
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.align import Align
from rich.console import Group
from rich.rule import Rule
from rich import box
from typing import List, Tuple
from views.formatters import (
    create_habits_table,
    create_menu_table,
    get_periodicity_icon
)


class ConsoleView:
    """
    Handles all console input/output using a Rich library.
    """

    def __init__(self):
        self.console = Console()

    # ============ Menu Display ============

    def show_menu(self):
        """Displays the main menu."""
        title = Text("✨ HABIT TRACKER ✨\n", style="bold magenta")
        horizontal_line = Rule(style="bright_blue")
        spacing = Text("")

        panel = Panel(
            Group(
                Align.center(title),
                horizontal_line,
                spacing,
                create_menu_table()
            ),
            box=box.HORIZONTALS,
            border_style="bright_blue",
            padding=(1, 2),
            title="[bold white]Main Menu[/bold white]",
            title_align="center",
            expand=False
        )

        self.console.print("\n", panel)

    # ============ User Input ============

    def get_menu_choice(self) -> str:
        """Gets user's menu choice."""
        return self.console.input(
            "[bold yellow]Enter your choice (1-9): [/bold yellow]"
        )

    def get_habit_name(self, prompt: str = "Enter habit name: ") -> str:
        """Gets a habit name from a user."""
        return self.console.input(prompt)

    def get_periodicity(
            self,
            prompt: str = "Enter periodicity (daily/weekly): "
    ) -> str:
        """Gets periodicity from the user."""
        return self.console.input(prompt).lower()

    def get_number_choice(self, prompt: str) -> str:
        """Gets a numbered choice from the user."""
        return self.console.input(prompt)

    # ============ Success Messages ============

    def show_habit_created(self, name: str):
        """Shows success message for habit creation."""
        self.console.print(
            f"✅ Habit '[bold green]{name}[/bold green]' created! ",
            style="green"
        )

    def show_habit_deleted(self, name: str):
        """Shows a message for habit deletion."""
        self.console.print(
            f"🗑️  Habit '[bold]{name}[/bold]' deleted.",
            style="yellow"
        )

    def show_habit_checked_off(self, name: str):
        """Shows a success message for check-off."""
        self.console.print(
            f"✅ Habit '[bold green]{name}[/bold green]' marked as done! ",
            style="green"
        )

    def show_habit_updated(
            self,
            old_name: str,
            new_name: str,
            new_periodicity: str
    ):
        """Shows a success message for habit update."""
        self.console.print("✅ Habit updated successfully!", style="bold green")
        self.console.print(
            f"   [cyan]{old_name}[/cyan] → [green]{new_name}[/green] "
            f"([yellow]{new_periodicity}[/yellow])"
        )

    def show_seeding_start(self):
        """Shows a message when seeding starts."""
        self.console.print(
            "🌱 Seeding database with 5 predefined habits and 4 weeks of data...",
            style="cyan"
        )

    def show_seeding_complete(self):
        """Shows a message when seeding completes."""
        self.console.print(
            "✅ Database seeded successfully.",
            style="bold green"
        )

    # ============ Error Messages ============

    def show_error(self, message: str):
        """Shows an error message."""
        self.console.print(f"❌ {message}", style="red")

    def show_invalid_periodicity(self):
        """Shows invalid periodicity error."""
        self.show_error("Invalid periodicity. Use 'daily' or 'weekly'.")

    def show_invalid_choice(self):
        """Shows an invalid menu choice error."""
        self.show_error("Invalid choice, please try again.")

    def show_habit_not_found(self, name: str):
        """Shows habit not found error."""
        self.show_error(f"Habit '{name}' not found.")

    def show_no_habits_found(self):
        """Shows no habits found a message."""
        self.show_error("No habits found.")

    def show_retry_message(self):
        """Shows retry message."""
        self.console.print("[dim]Please try again.. .[/dim]\n")

    # ============ Info Display ============

    def show_header(self, text: str, style: str = "bold cyan"):
        """Shows a section header."""
        self.console.print(f"\n{text}", style=style)

    def show_goodbye(self):
        """Shows goodbye message."""
        self.console.print(
            "\n👋 [bold magenta]Goodbye!  Keep building those habits![/bold magenta] ✨",
            style="magenta"
        )

    # ============ Habit Lists ============

    def show_habits_list(self, habits: List[Tuple[str, str]]):
        """
        Displays a list of all habits in a table.

        Args:
            habits: List of tuples (name, periodicity)
        """
        self.show_header("📋 [bold blue]Currently tracked habits:[/bold blue]\n")

        if habits:
            table = create_habits_table(habits)
            self.console.print(table)
        else:
            self.console.print("  No habits found.", style="dim")

    def show_habits_numbered_list(
            self,
            habits: List[Tuple[str, str]],
            header: str = "[bold cyan]Current habits:[/bold cyan]"
    ):
        """
        Displays habits as a numbered list.

        Args:
            habits: List of tuples (name, periodicity)
            header: Header text
        """
        self.console.print(f"\n{header}")

        for i, habit in enumerate(habits, 1):
            icon = get_periodicity_icon(habit[1])
            self.console.print(
                f"  {i}. {icon} [cyan]{habit[0]}[/cyan] "
                f"([yellow]{habit[1]}[/yellow])"
            )

    def show_filtered_habits(self, periodicity: str, habits: List[Tuple[str, str]]):
        """
        Shows habits filtered by periodicity.

        Args:
            periodicity: 'daily' or 'weekly'
            habits: List of tuples (name, periodicity)
        """
        self.console.print(
            f"\n{periodicity.capitalize()} habits:",
            style="bold cyan"
        )

        if habits:
            for habit in habits:
                icon = get_periodicity_icon(periodicity)
                self.console.print(f"  {icon} [cyan]{habit[0]}[/cyan]")
        else:
            self.console.print(f"  No {periodicity} habits found.", style="dim")

    # ============ Analytics Display ============

    def show_longest_streak_all(self, habit_name: str, streak: int):
        """
        Shows the habit with the longest streak.

        Args:
            habit_name: Name of the habit
            streak:  Streak length
        """
        self.show_header("🏆 [bold gold1]Longest streak analysis[/bold gold1]")
        self.console.print(
            f"🏆 The champion is '[bold green]{habit_name}[/bold green]' "
            f"with a streak of [bold yellow]{streak}[/bold yellow]! ",
            style="gold1"
        )

    def show_longest_streak_specific(self, habit_name: str, streak: int):
        """
        Shows a streak for a specific habit.

        Args:
            habit_name: Name of the habit
            streak: Streak length
        """
        self.console.print(
            f"🎯 Longest streak for '[bold green]{habit_name}[/bold green]':  "
            f"[bold yellow]{streak}[/bold yellow]",
            style="gold1"
        )

    # ============ Edit Helpers ============

    def show_current_habit_info(self, name: str, periodicity: str):
        """Shows current habit information during edit."""
        self.console.print(
            f"\n[bold cyan]Editing:[/bold cyan] [green]{name}[/green] "
            f"([yellow]{periodicity}[/yellow])"
        )
        self.console.print("\n[dim]Press Enter to keep current value[/dim]")

    def get_new_name(self, current_name: str) -> str:
        """Gets a new name during edit."""
        return self.console.input(
            f"New name (current: {current_name}): "
        ).strip()

    def get_new_periodicity(self, current_periodicity: str) -> str:
        """Gets new periodicity during edit."""
        return self.console.input(
            f"New periodicity (current: {current_periodicity}): "
        ).lower().strip()