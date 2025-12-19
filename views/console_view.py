"""
Console View - Handles all console output and user input
"""
from datetime import datetime
from typing import List, Tuple
from rich import box
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from views.formatters import (
    create_menu_table,
    get_periodicity_icon, create_manage_habits_menu_table, create_track_progress_menu_table,
    create_analytics_reports_menu_table
)


class ConsoleView:
    """
    Handles all console input/output using a Rich library.
    """

    def __init__(self):
        self.console = Console()

    # ============ Menu Display ============

    def show_menu(self):
        """Displays the main menu with a box border"""

        self.console.print()

        # Create a header with a double box border
        header = Panel(
            "🎯 HABIT TRACKER - MAIN MENU",
            style="bold cyan",
            box=box.DOUBLE,
            padding=(0, 2)
        )
        self.console.print(header)
        self.console.print()

        # Display menu options
        menu_table = create_menu_table()
        self.console.print(menu_table)
        self.console.print()

    def get_submenu_choice(self) -> str:
        """Gets a user's submenu choice (generic for all submenus)"""
        return self.console.input(
            "[bold yellow]Enter your choice: [/bold yellow]"
        )

    def show_manage_habits_menu(self):
        """Displays the Manage Habits submenu"""

        self.console.print()

        header = Panel(
            "📝 MANAGE HABITS",
            style="bold green",
            box=box.DOUBLE,
            padding=(0, 2)
        )
        self.console.print(header)
        self.console.print()

        menu_table = create_manage_habits_menu_table()
        self.console.print(menu_table)
        self.console.print()

    def show_track_progress_menu(self):
        """Displays the Track Progress submenu"""

        self.console.print()

        header = Panel(
            "✅ TRACK PROGRESS",
            style="bold blue",
            box=box.DOUBLE,
            padding=(0, 2)
        )
        self.console.print(header)
        self.console.print()

        menu_table = create_track_progress_menu_table()
        self.console.print(menu_table)
        self.console.print()

    def show_analytics_reports_menu(self):
        """Displays the Analytics & Reports submenu"""

        self.console.print()

        header = Panel(
            "📊 ANALYTICS & REPORTS",
            style="bold magenta",
            box=box.DOUBLE,
            padding=(0, 2)
        )
        self.console.print(header)
        self.console.print()

        menu_table = create_analytics_reports_menu_table()
        self.console.print(menu_table)
        self.console.print()

    def show_completion_statistics(self, summary):
        """
        Display comprehensive completion statistics.

        Args:
            summary: List of dictionaries with habit statistics
        """

        self.show_header("📈 [bold cyan]Completion Statistics[/bold cyan]")

        if not summary:
            self.console.print("  No habits found.", style="dim")
            return

        table = Table(
            show_header=True,
            header_style="bold magenta",
            box=box.ROUNDED,
            padding=(0, 2),
            expand=False
        )

        table.add_column("", width=3, justify="center")
        table.add_column("Habit Name", style="cyan bold", min_width=20, justify="left")
        table.add_column("Type", style="yellow", width=10, justify="center")
        table.add_column("Total", style="green", width=8, justify="center")
        table.add_column("Current", style="blue", width=10, justify="center")
        table.add_column("Longest", style="magenta", width=10, justify="center")
        table.add_column("Last Done", style="white", width=12, justify="center")

        for item in summary:
            icon = get_periodicity_icon(item['periodicity'])
            status_dot = "[green]●[/green]" if item.get('is_active', True) else "[red]○[/red]"
            name = f"{status_dot} {item['name']}"
            periodicity = item['periodicity'].capitalize()
            total = str(item.get('total_completions', 0))

            # Format streaks
            current_streak = item.get('current_streak', 0)
            longest_streak = item.get('longest_streak', 0)
            current_str = f"{current_streak} {'day' if item['periodicity'] == 'daily' else 'week'}{'s' if current_streak != 1 else ''}"
            longest_str = f"{longest_streak} {'day' if item['periodicity'] == 'daily' else 'week'}{'s' if longest_streak != 1 else ''}"

            # Format last completion
            last_completion = item.get('last_completion')
            if last_completion:
                if isinstance(last_completion, str):
                    last_completion = datetime.fromisoformat(last_completion)
                days_ago = (datetime.now() - last_completion).days
                if days_ago == 0:
                    last_done = "Today"
                elif days_ago == 1:
                    last_done = "Yesterday"
                else:
                    last_done = f"{days_ago}d ago"
            else:
                last_done = "Never"

            table.add_row(icon, name, periodicity, total, current_str, longest_str, last_done)

        self.console.print(table)
        self.console.print()

    # ============ User Input ============

    def get_menu_choice(self) -> str:
        """Gets a user's main menu choice"""
        return self.console.input(
            "[bold yellow]Enter your choice (1-4): [/bold yellow]"
        )

    def get_habit_name(self, prompt: str = "\nEnter habit name: ") -> str:
        """Gets a habit name from a user."""
        return self.console.input(prompt)

    def get_periodicity(
            self,
            prompt: str = "\nEnter periodicity (daily/weekly): "
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
        Gets habit description from the user.

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
            new_status: bool,
            new_periodicity: str
    ):
        """Shows a success message for habit update."""
        status_text = "[green]Active[/green]" if new_status else "[red]Inactive[/red]"
        self.console.print(
            "✅ Habit updated successfully!", style="bold green"
        )
        self.console.print(
            f"   {old_name} → {new_name} ([yellow]{new_periodicity}[/yellow]) - {status_text}"
        )
        self.console.print()

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

    def show_active_habits_list(self, habits: List[Tuple[str, str, str, bool]]):
        """
        Displays a list of active habits only.

        Args:
            habits: List of tuples (name, periodicity, comments, is_active)
        """
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

    def show_habits_numbered_list_with_status(
            self,
            habits: List[Tuple[str, str, bool]],
            header: str = "[bold cyan]Current habits:[/bold cyan]"
    ):
        """
        Displays habits as a numbered list.

        Args:
            habits: List of tuples (name, periodicity, is_active)
            header: Header text
        """
        self.console.print(f"\n{header}\n")

        for i, habit in enumerate(habits, 1):
            icon = get_periodicity_icon(habit[1])
            name = habit[0]
            periodicity = habit[1]
            is_active = habit[2]

            # Status indicator
            if is_active:
                status = "[green]●[/green]"  # Green dot for active
                name_style = f"{name}"
            else:
                status = "[red]○[/red]"  # Red hollow dot for inactive
                name_style = f"[dim strikethrough]{name}[/dim strikethrough]"

            self.console.print(
                f"  {i}. {status} {icon} {name_style} ([yellow]{periodicity}[/yellow])"
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
            ("1.", "🕐", "Daily habits"),
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

    def show_current_habit_info(self, name: str, periodicity: str, is_active: bool, description: str = ""):
        """
        Shows current habit information during edit.

        Args:
            name: Habit name
            periodicity: Habit periodicity
            is_active:  Habit status
            description: Habit description
        """
        status_text = "[green]Active[/green]" if is_active else "[red]Inactive[/red]"

        self.console.print(
            f"\n[bold cyan]Editing:[/bold cyan] [green]{name}[/green] "
            f"([yellow]{periodicity}[/yellow]) - Status: {status_text}"
        )
        if description:
            self.console.print(f"\n[bold cyan]Current description:[/bold cyan] [italic]{description}[/italic]")
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

    def get_new_status(self, current_status: bool) -> bool | None:
        """
        Gets a new status during edit.

        Args:
            current_status: Current status (True=active, False=inactive)

        Returns:
            New status or None if the user wants to keep current
        """

        current_text = "Active" if current_status else "Inactive"

        self.console.print(f"\n[bold cyan]Current status:[/bold cyan] {current_text}")
        self.console.print("[dim]Choose new status (or press Enter to keep current):[/dim]\n")

        # Create a status selection table
        table = Table(
            show_header=False,
            show_edge=False,
            padding=(0, 1),
            box=None
        )
        table.add_column("Number", style="bold yellow", width=3)
        table.add_column("Status")

        table.add_row("1.", "[green]Active[/green] - Habit is tracked and visible")
        table.add_row("2.", "[red]Inactive[/red] - Habit is archived/hidden")

        self.console.print(table)

        while True:
            user_input = self.console.input("\nEnter choice (1-2, or Enter to keep current): ").strip()

            if user_input == "":
                return None  # Keep current
            elif user_input == "1":
                return True  # Active
            elif user_input == "2":
                return False  # Inactive
            else:
                self.console.print("[red]Invalid choice. Please enter 1, 2, or press Enter.[/red]")

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