"""
Console View - Handles all console output and user input
"""
from typing import List, Tuple

from rich import box
from rich.align import Align
from rich.console import Console
from rich.console import Group
from rich.panel import Panel
from rich.rule import Rule
from rich.text import Text

from views.formatters import (
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
            "[bold yellow]Enter your choice (1-12): [/bold yellow]"  # Changed from 1-11
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

    def get_confirmation(self, prompt: str) -> str:
        """
        Gets a confirmation from a user.

        Args:
            prompt: Prompt text to display

        Returns:
            User's input as string
        """
        return self.console.input(prompt)

    def get_habit_description(self) -> str:
        """
        Gets habit description/description from the user.

        Returns:
            User's description as string
        """
        return self.console.input("Enter a short description (press Enter to skip): ").strip()

    def get_completion_notes(self) -> str:
        """
        Gets completion notes from the user.

        Returns:
            User's notes as string
        """
        return self.console.input("Enter notes (press Enter to skip): ").strip()

    def get_deletion_type(self) -> str:
        """
        Asks user to choose a deletion type.

        Returns:
            'soft', 'hard', or 'cancel'
        """
        from rich.panel import Panel
        from rich import box

        deletion_menu = """[yellow]1.[/yellow] [cyan]Soft Delete (Archive)[/cyan] - Hide habit but keep all data
    [yellow]2.[/yellow] [red]Hard Delete (Permanent)[/red] - Delete habit and all completion history
    [yellow]q.[/yellow] [dim]Cancel[/dim]"""

        panel = Panel(
            deletion_menu,
            title="[bold magenta]Choose Deletion Type[/bold magenta]",
            border_style="yellow",
            box=box.ROUNDED,
            padding=(1, 2)
        )

        self.console.print(panel)

        while True:
            choice = self.console.input(
                "\n[bold yellow]Enter your choice (1-2, or 'q' to cancel): [/bold yellow]").strip()

            if choice == '1':
                return 'soft'
            elif choice == '2':
                return 'hard'
            elif choice.lower() == 'q':
                return 'cancel'
            else:
                self.console.print("[red]Invalid choice. Please enter 1, 2, or 'q'.[/red]")

    # ============ Success Messages ============

    def show_habit_created(self, name: str):
        """Shows success message for habit creation."""
        self.console.print(
            f"✅ Habit '[bold green]{name}[/bold green]' created! ",
            style="green"
        )

    def show_habit_archived(self, name: str):
        """
        Shows habit archived confirmation.

        Args:
            name: Habit name
        """
        self.console.print()
        self.console.print(f"📦 [yellow]Habit '{name}' archived successfully![/yellow]")
        self.console.print("[dim]The habit is now hidden but all data is preserved.[/dim]")
        self.console.print()

    def show_habit_deleted(self, name: str):
        """
        Shows habit deleted confirmation.

        Args:
            name: Habit name
        """
        self.console.print()
        self.console.print(f"🗑️  [red bold]Habit '{name}' permanently deleted![/red bold]")
        self.console.print("[dim]All completion history has been removed.[/dim]")
        self.console.print()

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
        self.console.print(f"\n❌ {message}", style="red")

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
        self.console.print("\n[dim]Please try again.. .[/dim]\n")

    # ============ Info Display ============

    def show_header(self, text: str, style: str = "bold cyan"):
        """Shows a section header."""
        self.console.print(f"\n{text}", style=style)

    def show_goodbye(self):
        """Shows goodbye message."""
        self.console.print(
            "\n👋 [bold magenta]Goodbye!  Keep building those habits![/bold magenta] ✨\n",
            style="magenta"
        )

    # ============ Habit Lists ============

    def show_habits_list(self, habits: List[Tuple[str, str, str, bool]]):
        """
        Displays a list of active habits only.

        Args:
            habits: List of tuples (name, periodicity, comments, is_active)
        """
        from rich.table import Table
        from rich import box
        from views.formatters import get_periodicity_icon

        self.show_header("📋 [bold blue]Currently tracked habits:[/bold blue]")

        # Add a blank line for spacing
        self.console.print()

        # Filter only active habits
        active_habits = [h for h in habits if h[3]]  # h[3] is is_active

        if active_habits:
            table = Table(
                show_header=True,
                header_style="bold magenta",
                box=box.ROUNDED,
                padding=(0, 2),
                expand=False
            )

            # Column definitions
            table.add_column("", width=3, justify="center")  # Icon
            table.add_column("Habit Name", style="cyan bold", min_width=20, justify="center")
            table.add_column("Periodicity", style="yellow", width=12, justify="center", no_wrap=True)
            table.add_column("Description", style="dim italic", no_wrap=True, justify="center")

            for habit in active_habits:
                icon = get_periodicity_icon(habit[1])
                name = habit[0]
                periodicity = habit[1].capitalize()
                comments = habit[2] if habit[2] else "-"

                table.add_row(icon, name, periodicity, comments)

            self.console.print(table)
        else:
            self.console.print("  No active habits found.", style="dim")

        self.console.print()

    def show_all_habits_list(self, habits: List[Tuple[str, str, str, bool]]):
        """
        Displays a list of all habits, including inactive ones.

        Args:
            habits: List of tuples (name, periodicity, comments, is_active)
        """
        from rich.table import Table
        from rich import box
        from views.formatters import get_periodicity_icon

        self.show_header("📚 [bold blue]All habits (including inactive):[/bold blue]")

        # Add a blank line for spacing
        self.console.print()

        if habits:
            table = Table(
                show_header=True,
                header_style="bold magenta",
                box=box.ROUNDED,
                padding=(0, 2),
                expand=False
            )

            # Column definitions
            table.add_column("", width=3, justify="center")  # Icon
            table.add_column("Habit Name", style="cyan bold", min_width=20, justify="center")
            table.add_column("Periodicity", style="yellow", width=12, justify="center", no_wrap=True)
            table.add_column("Status", style="white", width=10, justify="center")
            table.add_column("Description", style="dim italic", no_wrap=True, justify="center")

            for habit in habits:
                icon = get_periodicity_icon(habit[1])
                name = habit[0]
                periodicity = habit[1].capitalize()
                is_active = habit[3]
                comments = habit[2] if habit[2] else "-"

                # Status indicator
                if is_active:
                    status = "[green]Active[/green]"
                    name_style = f"[cyan]{name}[/cyan]"
                else:
                    status = "[red]Archived[/red]"
                    name_style = f"[dim strikethrough]{name}[/dim strikethrough]"
                    icon = f"[dim]{icon}[/dim]"
                    periodicity = f"[dim]{periodicity}[/dim]"
                    comments = f"[dim]{comments}[/dim]"

                table.add_row(icon, name_style, periodicity, status, comments)

            self.console.print(table)
        else:
            self.console.print("  No habits found.", style="dim")

        self.console.print()

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
        self.console.print(f"\n{header}\n")

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
            f"\n{periodicity.capitalize()} habits:\n",
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
        self.show_header("\n🏆 [bold gold1]Longest streak analysis[/bold gold1]")
        self.console.print(
            f"\n🏆 The champion is '[bold green]{habit_name}[/bold green]' "
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

    def show_periodicity_menu(self):
        """
        Displays the periodicity filter menu.
        """
        from rich.table import Table

        table = Table(
            show_header=False,
            show_edge=False,
            padding=(0, 1),
            box=None
        )
        table.add_column("Number", style="bold yellow", width=3, no_wrap=True)
        table.add_column("Icon", width=4, no_wrap=True)
        table.add_column("Description", style="cyan")

        menu_items = [
            ("1.", "☀️", "Daily habits"),
            ("2.", "📆", "Weekly habits"),
        ]

        for item in menu_items:
            table.add_row(*item)

        self.console.print("\n")
        self.console.print(table)

    def show_completion_table(self, summary_data: List[dict]):
        """
        Displays a comprehensive completion table for all habits.

        Args:
            summary_data: List of habit summary dictionaries
        """
        from rich.table import Table
        from rich import box

        self.show_header("📊 [bold magenta]Habit Completion Summary[/bold magenta]")
        self.console.print()

        if not summary_data:
            self.console.print("  No habits found.", style="dim")
            return

        table = Table(
            show_header=True,
            header_style="bold magenta",
            box=box.ROUNDED,
            padding=(0, 1),
            expand=True
        )

        table.add_column("#", style="bold yellow", width=3, justify="right")
        table.add_column("Habit Name", style="cyan", min_width=20)
        table.add_column("Periodicity", style="yellow", width=11, justify="center")  # CHANGED
        table.add_column("Created", style="dim", width=10)
        table.add_column("Last Done", style="green", width=10)
        table.add_column("Streak", style="bold yellow", width=6, justify="right")
        table.add_column("Total", style="blue", width=5, justify="right")

        for idx, habit_data in enumerate(summary_data, 1):
            created_date = habit_data['created_at'].strftime('%Y-%m-%d')

            last_done = (
                habit_data['last_completion'].strftime('%Y-%m-%d')
                if habit_data['last_completion']
                else "Never"
            )

            streak = str(habit_data['current_streak'])
            total = str(habit_data['total_completions'])

            # Capitalize periodicity for display
            periodicity_display = habit_data['periodicity'].capitalize()

            table.add_row(
                str(idx),
                habit_data['name'],
                periodicity_display,
                created_date,
                last_done,
                streak,
                total
            )

        self.console.print(table)
        self.console.print()

    def show_habit_completion_history(self, habit_data: dict):
        """
        Displays a detailed completion history for a specific habit.

        Args:
            habit_data: Dictionary with habit details and completions
        """
        from rich.table import Table
        from rich.panel import Panel
        from rich import box
        from views.formatters import get_periodicity_icon

        icon = get_periodicity_icon(habit_data['periodicity'])

        # Header with habit info
        header_text = f"{icon} [bold cyan]{habit_data['name']}[/bold cyan] ([yellow]{habit_data['periodicity']}[/yellow])"
        self.console.print()
        self.console.print(header_text)
        self.console.print()

        # Summary stats
        stats = f"""[bold]Created:[/bold] {habit_data['created_at'].strftime('%Y-%m-%d %H:%M')}
                [bold]Total Completions:[/bold] {habit_data['total_completions']}
                [bold]Current Streak:[/bold] {habit_data['current_streak']}
                [bold]Longest Streak:[/bold] {habit_data['longest_streak']}
                [bold]Description:[/bold] {habit_data['description']}"""

        panel = Panel(
            stats,
            title="[bold white]Habit Statistics[/bold white]",
            border_style="cyan",
            box=box.ROUNDED,
            padding=(1, 2)
        )
        self.console.print(panel)
        self.console.print()

        # Completion history table
        if habit_data['completions']:
            self.console.print("[bold magenta]📅 Completion History:[/bold magenta]")
            self.console.print()

            table = Table(
                show_header=True,
                header_style="bold cyan",
                box=box.SIMPLE,
                padding=(0, 2)
            )

            table.add_column("#", style="dim", width=4, justify="right")
            table.add_column("Date", style="green", width=10)
            table.add_column("Time", style="cyan", width=8)
            table.add_column("Notes", style="italic", max_width=50)

            for idx, completion in enumerate(habit_data['completions'], 1):
                date_str = completion['checked_at'].strftime('%Y-%m-%d')
                time_str = completion['checked_at'].strftime('%H:%M:%S')
                notes = completion['notes'] if completion['notes'] else "-"

                table.add_row(str(idx), date_str, time_str, notes)

            self.console.print(table)
        else:
            self.console.print("  [dim]No completions recorded yet.[/dim]")

        self.console.print()

    # ============ Edit Helpers ============

    def show_current_habit_info(self, name: str, periodicity: str, description: str = ""):
        """Shows current habit information during edit."""
        self.console.print(
            f"\n[bold cyan]Editing:[/bold cyan] [green]{name}[/green] "
            f"([yellow]{periodicity}[/yellow])"
        )
        if description:
            self.console.print(f"[bold cyan]Current description:[/bold cyan] [italic]{description}[/italic]")
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

    def get_new_description(self, current_description: str) -> str | None:
        """
        Gets a new description during edit.

        Args:
            current_description: Current description

        Returns:
            New description or None if the user wants to keep current
        """
        display_description = current_description if current_description else "(no description)"
        user_input = self.console.input(
            f"New description (current: {display_description}): "
        ).strip()

        # Return None if the user pressed Enter (keep current)
        # Return empty string if the user wants to clear
        # Return new value if the user entered something
        if user_input == "":
            return None  # Keep current
        return user_input