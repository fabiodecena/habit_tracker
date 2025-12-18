"""
View formatting utilities
"""
from rich.table import Table


def create_menu_table() -> Table:
    """
    Creates the main menu table.

    Returns:
        Rich Table object
    """
    menu_items = [
        ("1.", "📝", "[green bold]Manage Habits[/green bold]"),
        ("2.", "✅", "[blue bold]Track Progress[/blue bold]"),
        ("3.", "📊", "[magenta bold]Analytics & Reports[/magenta bold]"),
        ("4.", "👋", "[red]Exit[/red]")
    ]

    table = Table(
        show_header=False,
        show_edge=False,
        padding=(0, 1),
        box=None
    )
    table.add_column("Number", style="bold yellow", width=4, no_wrap=True)
    table.add_column("Icon", width=4, no_wrap=True)
    table.add_column("Description")

    for item in menu_items:
        table.add_row(*item)

    return table


def create_manage_habits_menu_table() -> Table:
    """Creates the Manage Habits submenu table"""
    menu_items = [
        ("1.", "➕", "[gold1]Create a new habit[/gold1]"),
        ("2.", "📝", "[gold1]Edit a habit[/gold1]"),
        ("3.", "❌", "[gold1]Delete a habit[/gold1]"),
        ("4.", "📋", "[gold1]List all active habits[/gold1]"),
        ("5.", "📚", "[gold1]List all habits (including inactive)[/gold1]"),
        ("6.", "🔍", "[gold1]List habits by periodicity[/gold1]"),
        ("7.", "↩️", "[dim]Back to main menu[/dim]")
    ]

    table = Table(
        show_header=False,
        show_edge=False,
        padding=(0, 1),
        box=None
    )
    table.add_column("Number", style="bold yellow", width=4, no_wrap=True)
    table.add_column("Icon", width=4, no_wrap=True)
    table.add_column("Description")

    for item in menu_items:
        table.add_row(*item)

    return table


def create_track_progress_menu_table() -> Table:
    """Creates the Track Progress submenu table"""
    menu_items = [
        ("1.", "✅", "[gold1]Check-off a habit (mark as complete)[/gold1]"),
        ("2.", "📊", "[gold1]View completion table (summary)[/gold1]"),
        ("3.", "📈", "[gold1]View detailed habit history[/gold1]"),
        ("4.", "📝", "[gold1]Edit completion notes[/gold1]"),
        ("5.", "↩️", "[dim]Back to main menu[/dim]")
    ]

    table = Table(
        show_header=False,
        show_edge=False,
        padding=(0, 1),
        box=None
    )
    table.add_column("Number", style="bold yellow", width=4, no_wrap=True)
    table.add_column("Icon", width=4, no_wrap=True)
    table.add_column("Description")

    for item in menu_items:
        table.add_row(*item)

    return table


def create_analytics_reports_menu_table() -> Table:
    """Creates the Analytics & Reports submenu table"""
    menu_items = [
        ("1.", "🏆", "[gold1]Show longest streak of all habits[/gold1]"),
        ("2.", "🎯", "[gold1]Show longest streak for specific habit[/gold1]"),
        ("3.", "📈", "[gold1]Show completion statistics[/gold1]"),
        ("4.", "↩️", "[dim]Back to main menu[/dim]")
    ]

    table = Table(
        show_header=False,
        show_edge=False,
        padding=(0, 1),
        box=None
    )
    table.add_column("Number", style="bold yellow", width=4, no_wrap=True)
    table.add_column("Icon", width=4, no_wrap=True)
    table.add_column("Description")

    for item in menu_items:
        table.add_row(*item)

    return table


def get_periodicity_icon(periodicity: str) -> str:
    """
    Returns an icon based on habit periodicity.

    Args:
        periodicity: 'daily' or 'weekly'

    Returns:
        Icon string
    """
    icons = {
        'daily': '🕐',
        'weekly': '📆'
    }
    return icons. get(periodicity. lower(), '❓')