"""
Formatting utilities for console output
"""
from rich.table import Table
from rich import box
from typing import List, Tuple


def create_habits_table(habits: List[Tuple[str, str]]) -> Table:
    """
    Creates a formatted table of habits.

    Args:
        habits: List of tuples (name, periodicity)

    Returns:
        Rich Table object
    """
    table = Table(
        show_header=True,
        show_edge=False,
        padding=(0, 2),
        box=box.SIMPLE_HEAD
    )
    table.add_column("Name", style="cyan")
    table.add_column("Periodicity", style="yellow", justify="left")

    for habit in habits:
        periodicity_icon = "🕐" if habit[1] == "daily" else "📆"
        table.add_row(f"{periodicity_icon}  {habit[0]}", habit[1])

    return table


def create_menu_table() -> Table:
    """
    Creates the main menu table.

    Returns:
        Rich Table object
    """
    menu_items = [
        ("1.", "➕", "[gold1]Create a new habit[/gold1]"),
        ("2.", "❌", "[gold1]Delete a habit[/gold1]"),
        ("3.", "✅", "[gold1]Check-off a habit (Complete task)[/gold1]"),
        ("4.", "📝", "[gold1]Edit a habit[/gold1]"),
        ("5.", "📋", "[gold1]List all habits[/gold1]"),
        ("6.", "🔍", "[gold1]List habits by periodicity[/gold1]"),
        ("7.", "🏆", "[gold1]Show longest streak of all habits[/gold1]"),
        ("8.", "🎯", "[gold1]Show longest streak for a specific habit[/gold1]"),
        ("9.", "📊", "[gold1]View completion table[/gold1]"),
        ("10.", "📌", "[gold1]Edit completion notes[/gold1]"),
        ("11.", "👋", "[red]Exit[/red]")
    ]

    table = Table(
        show_header=False,
        show_edge=False,
        padding=(0, 1),
        box=None
    )
    table.add_column("Number", style="bold yellow", width=3, no_wrap=True)
    table.add_column("Icon", width=4, no_wrap=True)
    table.add_column("Description")

    for item in menu_items:
        table.add_row(*item)

    return table


def get_periodicity_icon(periodicity: str) -> str:
    """
    Returns the appropriate icon for periodicity.

    Args:
        periodicity: 'daily' or 'weekly'

    Returns:
        Icon string
    """
    return "🕐" if periodicity == "daily" else "📆"