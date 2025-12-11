import sys
import os
from datetime import datetime, timedelta
import click
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

# Add the parent directory to a path so we can import modules if running directly
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from habit import Habit
import analytics
from database import get_connection

# Initialize Rich console
console = Console()


def seed_predefined_data(db):
    """
    Populates the database with 5 habits and 4 weeks of sample data.
    """
    cur = db.cursor()
    cur.execute("SELECT count(*) FROM habits")
    if cur.fetchone()[0] > 0:
        return  # Data already exists, don't overwrite

    console.print("🌱 Seeding database with 5 predefined habits and 4 weeks of data.. .", style="cyan")

    # Define Habits
    habits_data = [
        ("Drink Water", "daily"),
        ("Read Book", "daily"),
        ("Exercise", "daily"),
        ("Clean House", "weekly"),
        ("Body Weight Check", "weekly")
    ]

    end_date = datetime.now()
    start_date = end_date - timedelta(weeks=4)

    for name, periodicity in habits_data:
        h = Habit(name, periodicity)
        h.create(db)

        # Generate tracking data
        current = start_date
        while current <= end_date:
            if periodicity == 'daily':
                # Skip some days to make it realistic (80% success rate)
                if int(current.timestamp()) % 5 != 0:
                    h.check_off(current, db)
                current += timedelta(days=1)
            elif periodicity == 'weekly':
                # Check off once per week
                h.check_off(current, db)
                current += timedelta(weeks=1)

    console.print("✅ Database seeded successfully.", style="bold green")


# Click command group
@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx):
    """✨ Habit Tracker CLI - Build better habits!  ✨"""
    db = get_connection()
    seed_predefined_data(db)

    # Store db in context for other commands
    ctx.ensure_object(dict)
    ctx.obj['db'] = db

    # If no subcommand is provided, show the interactive menu
    if ctx.invoked_subcommand is None:
        interactive_menu(db)


def show_fancy_menu():
    """Display a fancy menu with icons using Rich"""
    from rich import box
    from rich.align import Align
    from rich.console import Group
    from rich.rule import Rule

    menu_items = [
        ("1.", "➕", "[cyan]Create a new habit[/cyan]"),
        ("2.", "❌", "[red]Delete a habit[/red]"),
        ("3.", "✅", "[green]Check-off a habit (Complete task)[/green]"),
        ("4.", "📝", "[yellow]Edit a habit[/yellow]"),
        ("5.", "📋", "[blue]List all habits[/blue]"),
        ("6.", "🔍", "[blue]List habits by periodicity[/blue]"),
        ("7.", "🏆", "[gold1]Show longest streak of all habits[/gold1]"),
        ("8.", "🎯", "[gold1]Show longest streak for a specific habit[/gold1]"),
        ("9.", "👋", "[red]Exit[/red]")
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

    # Title
    title = Text("✨ HABIT TRACKER MENU ✨\n", style="bold magenta")

    # Horizontal line/rule
    horizontal_line = Rule(style="bright_blue")

    # Empty line for spacing
    spacing = Text("")

    panel = Panel(
        Group(Align.center(title), horizontal_line, spacing, table),
        box=box.HORIZONTALS,
        border_style="bright_blue",
        padding=(1, 2),
        title="[bold white]Main Menu[/bold white]",
        title_align="center",
        expand=False
    )

    console.print(panel)

def interactive_menu(db):
    """Interactive menu loop"""
    while True:
        show_fancy_menu()
        choice = console.input("[bold yellow]Enter your choice (1-9): [/bold yellow]")

        if choice == '1':
            create_habit_interactive(db)
        elif choice == '2':
            delete_habit_interactive(db)
        elif choice == '3':
            checkoff_habit_interactive(db)
        elif choice == '4':
            edit_habit_interactive(db)
        elif choice == '5':
            list_habits_interactive(db)
        elif choice == '6':
            list_by_periodicity_interactive(db)
        elif choice == '7':
            longest_streak_all_interactive(db)
        elif choice == '8':
            longest_streak_specific_interactive(db)
        elif choice == '9':
            console.print("\n👋 [bold magenta]Goodbye!  Keep building those habits![/bold magenta] ✨", style="magenta")
            break
        else:
            console.print("❌ Invalid choice, please try again.", style="red")


def create_habit_interactive(db):
    """Interactive create habit"""
    console.print("\n✨ [bold cyan]Create a new habit[/bold cyan]")
    name = console.input("Enter habit name: ")
    period = console.input("Enter periodicity (daily/weekly): ").lower()

    if period in ['daily', 'weekly']:
        h = Habit(name, period)
        h.create(db)
        console.print(f"✅ Habit '[bold green]{name}[/bold green]' created!", style="green")
    else:
        console.print("❌ Invalid periodicity. Use 'daily' or 'weekly'.", style="red")


def delete_habit_interactive(db):
    """Interactive delete habit"""
    console.print("\n🗑️  [bold red]Delete a habit[/bold red]")
    name = console.input("Enter habit name to delete: ")
    h = Habit(name, "daily")
    h.delete(db)
    console.print(f"🗑️  Habit '[bold]{name}[/bold]' deleted (if it existed).", style="yellow")


def checkoff_habit_interactive(db):
    """Interactive check-off habit"""
    console.print("\n✅ [bold green]Check-off a habit[/bold green]")
    name = console.input("Enter habit name to check-off: ")
    h = Habit(name, "daily")
    h.check_off(datetime.now(), db)
    console.print(f"✅ Marked '[bold green]{name}[/bold green]' as done for today!", style="green")


def edit_habit_interactive(db):
    """Interactive edit habit"""
    console.print("\n✏️  [bold yellow]Edit a habit[/bold yellow]")

    habits = analytics.get_all_habits(db)
    if not habits:
        console.print("❌ No habits found to edit.", style="red")
        return

    console.print("\n[bold cyan]Current habits:[/bold cyan]")
    for i, habit in enumerate(habits, 1):
        periodicity_icon = "☀️" if habit[1] == "daily" else "📆"
        console.print(f"  {i}. {periodicity_icon} [cyan]{habit[0]}[/cyan] ([yellow]{habit[1]}[/yellow])")

    old_name = console.input("\nEnter the name of the habit to edit: ")

    target_habit = next((h for h in habits if h[0] == old_name), None)
    if not target_habit:
        console.print(f"❌ Habit '{old_name}' not found.", style="red")
        return

    console.print(f"\n[bold cyan]Editing:[/bold cyan] [green]{old_name}[/green] ([yellow]{target_habit[1]}[/yellow])")
    console.print("\n[dim]Press Enter to keep current value[/dim]")

    new_name = console.input(f"New name (current: {old_name}): ").strip()
    new_periodicity = console.input(f"New periodicity (current: {target_habit[1]}): ").lower().strip()

    if not new_name:
        new_name = old_name
    if not new_periodicity:
        new_periodicity = target_habit[1]

    if new_periodicity not in ['daily', 'weekly']:
        console.print("❌ Invalid periodicity. Use 'daily' or 'weekly'.", style="red")
        return

    cur = db.cursor()
    try:
        cur.execute(
            "UPDATE habits SET name = ?, periodicity = ? WHERE name = ?",
            (new_name, new_periodicity, old_name)
        )

        if new_name != old_name:
            cur.execute(
                "UPDATE tracker SET habit_name = ? WHERE habit_name = ?",
                (new_name, old_name)
            )

        db.commit()
        console.print(f"✅ Habit updated successfully!", style="bold green")
        console.print(f"   [cyan]{old_name}[/cyan] → [green]{new_name}[/green] ([yellow]{new_periodicity}[/yellow])")
    except Exception as e:
        db.rollback()
        console.print(f"❌ Error updating habit: {e}", style="red")


def list_habits_interactive(db):
    """Interactive list of all habits"""
    console.print("\n📋 [bold blue]Currently tracked habits:[/bold blue]")
    habits = analytics.get_all_habits(db)
    if habits:
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Icon", style="cyan", width=6)
        table.add_column("Habit Name", style="cyan")
        table.add_column("Periodicity", style="yellow")

        for habit in habits:
            periodicity_icon = "☀️" if habit[1] == "daily" else "📆"
            table.add_row(periodicity_icon, habit[0], habit[1])

        console.print(table)
    else:
        console.print("  No habits found.", style="dim")


def list_by_periodicity_interactive(db):
    """Interactive list habits by periodicity"""
    console.print("\n🔍 [bold blue]Filter habits by periodicity[/bold blue]")
    p = console.input("Which periodicity?  (daily/weekly): ").lower()
    habits = analytics.get_habits_by_periodicity(p, db)
    console.print(f"\n{p.capitalize()} habits:", style="bold cyan")
    if habits:
        for habit in habits:
            periodicity_icon = "☀️" if p == "daily" else "📆"
            console.print(f"  {periodicity_icon} [cyan]{habit[0]}[/cyan]")
    else:
        console.print(f"  No {p} habits found.", style="dim")


def longest_streak_all_interactive(db):
    """Interactive longest streak for all habits"""
    console.print("\n🏆 [bold gold1]Longest streak analysis[/bold gold1]")
    best = analytics.get_longest_streak_all_habits(db)
    console.print(
        f"🏆 The champion is '[bold green]{best[0]}[/bold green]' with a streak of [bold yellow]{best[1]}[/bold yellow]!",
        style="gold1")


def longest_streak_specific_interactive(db):
    """Interactive longest item_streak for a specific habit"""
    console.print("\n🎯 [bold gold1]Specific habit item_streak analysis[/bold gold1]")
    name = console.input("Enter habit name: ")
    habits = analytics.get_all_habits(db)
    target = next((h for h in habits if h[0] == name), None)
    if target:
        item_streak = analytics.calculate_longest_streak(target[0], target[1], db)
        console.print(f"🎯 Longest item_streak for '[bold green]{name}[/bold green]':  [bold yellow]{item_streak}[/bold yellow]",
                      style="gold1")
    else:
        console.print("❌ Habit not found.", style="red")


# Click commands for direct CLI usage
@cli.command()
@click.argument('name')
@click.argument('periodicity', type=click.Choice(['daily', 'weekly']))
@click.pass_context
def create(ctx, name, periodicity):
    """✨ Create a new habit"""
    db = ctx.obj['db']
    h = Habit(name, periodicity)
    h.create(db)
    console.print(f"✅ Habit '[bold green]{name}[/bold green]' created!", style="green")


@cli.command()
@click.argument('name')
@click.pass_context
def delete(ctx, name):
    """🗑️  Delete a habit"""
    db = ctx.obj['db']
    h = Habit(name, "daily")
    h.delete(db)
    console.print(f"🗑️  Habit '[bold]{name}[/bold]' deleted.", style="yellow")


@cli.command()
@click.argument('name')
@click.pass_context
def checkoff(ctx, name):
    """✅ Check-off a habit (mark as complete)"""
    db = ctx.obj['db']
    h = Habit(name, "daily")
    h.check_off(datetime.now(), db)
    console.print(f"✅ Marked '[bold green]{name}[/bold green]' as done!", style="green")


@cli.command()
@click.argument('old_name')
@click.option('--new-name', help='New name for the habit')
@click.option('--periodicity', type=click.Choice(['daily', 'weekly']), help='New periodicity')
@click.pass_context
def edit(ctx, old_name, new_name, periodicity):
    """✏️  Edit a habit's name or periodicity"""
    db = ctx.obj['db']
    habits = analytics.get_all_habits(db)
    target_habit = next((h for h in habits if h[0] == old_name), None)

    if not target_habit:
        console.print(f"❌ Habit '{old_name}' not found.", style="red")
        return

    final_name = new_name if new_name else old_name
    final_periodicity = periodicity if periodicity else target_habit[1]

    cur = db.cursor()
    try:
        cur.execute(
            "UPDATE habits SET name = ?, periodicity = ? WHERE name = ?",
            (final_name, final_periodicity, old_name)
        )

        if final_name != old_name:
            cur.execute(
                "UPDATE tracker SET habit_name = ? WHERE habit_name = ?",
                (final_name, old_name)
            )

        db.commit()
        console.print(
            f"✅ Habit updated:  [cyan]{old_name}[/cyan] → [green]{final_name}[/green] ([yellow]{final_periodicity}[/yellow])",
            style="green")
    except Exception as e:
        db.rollback()
        console.print(f"❌ Error:  {e}", style="red")


@cli.command()
@click.pass_context
def item_list(ctx):
    """📋 List all habits"""
    db = ctx.obj['db']
    habits = analytics.get_all_habits(db)

    if habits:
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Icon", style="cyan", width=6)
        table.add_column("Habit Name", style="cyan")
        table.add_column("Periodicity", style="yellow")

        for habit in habits:
            periodicity_icon = "📅" if habit[1] == "daily" else "📆"
            table.add_row(periodicity_icon, habit[0], habit[1])

        console.print(table)
    else:
        console.print("No habits found.", style="dim")


@cli.command()
@click.argument('periodicity', type=click.Choice(['daily', 'weekly']))
@click.pass_context
def item_filter(ctx, periodicity):
    """🔍 List habits by periodicity"""
    db = ctx.obj['db']
    habits = analytics.get_habits_by_periodicity(periodicity, db)

    console.print(f"\n{periodicity.capitalize()} habits:", style="bold cyan")
    if habits:
        for habit in habits:
            periodicity_icon = "📅" if periodicity == "daily" else "📆"
            console.print(f"  {periodicity_icon} [cyan]{habit[0]}[/cyan]")
    else:
        console.print(f"  No {periodicity} habits found.", style="dim")


@cli.command()
@click.pass_context
def champion(ctx):
    """🏆 Show the habit with the longest streak"""
    db = ctx.obj['db']
    best = analytics.get_longest_streak_all_habits(db)
    console.print(
        f"🏆 Champion: '[bold green]{best[0]}[/bold green]' with streak of [bold yellow]{best[1]}[/bold yellow]!",
        style="gold1")


@cli.command()
@click.argument('name')
@click.pass_context
def streak(ctx, name):
    """🎯 Show the longest streak for a specific habit"""
    db = ctx.obj['db']
    habits = analytics.get_all_habits(db)
    target = next((h for h in habits if h[0] == name), None)

    if target:
        streak_count = analytics.calculate_longest_streak(target[0], target[1], db)
        console.print(f"🎯 Streak for '[bold green]{name}[/bold green]': [bold yellow]{streak_count}[/bold yellow]",
                      style="gold1")
    else:
        console.print(f"❌ Habit '{name}' not found.", style="red")


if __name__ == '__main__':
    cli(obj={})