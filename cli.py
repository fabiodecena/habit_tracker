"""
CLI entry point using Click
"""
from datetime import datetime
import click
from controllers.menu_controller import MenuController
from database.connection import Database
from services.analytics_service import AnalyticsService
from services.habit_service import HabitService
from services.tracker_service import TrackerService
from utils.seed_data import seed_predefined_data
from views.console_view import ConsoleView


@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx):
    """✨ Habit Tracker CLI - Build better habits!  ✨"""
    # Initialize database and seed data
    db = Database. get_connection()
    seed_predefined_data(db)

    # Store db in context for other commands
    ctx.ensure_object(dict)
    ctx.obj['db'] = db

    # If no subcommand is provided, launch the interactive menu
    if ctx.invoked_subcommand is None:
        controller = MenuController(db)
        controller.run()


# ============ Menu Command ============

@cli.command()
@click.pass_context
def menu(ctx):
    """🎯 Launch interactive menu"""
    db = ctx.obj['db']
    controller = MenuController(db)
    controller.run()


# ============ Direct CLI Commands (Quick Actions) ============

@cli.command()
@click.argument('name')
@click.argument('periodicity', type=click.Choice(['daily', 'weekly']))
@click.option('--description', default='', help='Description for the habit')
@click.pass_context
def create(ctx, name, periodicity, description):
    """✨ Create a new habit"""
    db = ctx.obj['db']
    view = ConsoleView()
    service = HabitService(db)

    success, message = service.create_habit(name, periodicity, description)

    if success:
        view.show_habit_created(name)
        if description:
            view.console.print(f"   💬 Description: [italic]{description}[/italic]", style="dim cyan")
    else:
        view.show_error(message)


@cli.command()
@click.argument('name')
@click.option('--hard', is_flag=True, help='Permanently delete (default is soft delete)')
@click.pass_context
def delete(ctx, name, hard):
    """❌ Delete a habit"""
    db = ctx.obj['db']
    view = ConsoleView()
    service = HabitService(db)

    soft_delete = not hard

    if hard:
        confirm = view.get_confirmation(
            f"⚠️  PERMANENTLY delete '{name}' and all its data?  This cannot be undone!  (y/n): "
        )
    else:
        confirm = view. get_confirmation(
            f"⚠️  Archive '{name}'? (You can restore it later) (y/n): "
        )

    if confirm. lower() != 'y':
        view. console.print("❌ Deletion cancelled.", style="yellow")
        return

    success, message = service.delete_habit(name, soft_delete=soft_delete)

    if success:
        if soft_delete:
            view. show_habit_archived(name)
        else:
            view.show_habit_deleted(name)
    else:
        view.show_error(message)


@cli.command()
@click.argument('name')
@click.option('--notes', default='', help='Optional notes about completion')
@click.pass_context
def checkoff(ctx, name, notes):
    """✅ Check off a habit"""
    db = ctx.obj['db']
    view = ConsoleView()
    service = TrackerService(db)

    success, message = service.check_off_habit(name, datetime.now(), notes)

    if success:
        view. show_habit_checked_off(name)
        if notes:
            view.console.print(f"   📝 Notes: [italic]{notes}[/italic]", style="dim cyan")
    else:
        view.show_error(message)


@cli.command()
@click.option('--all', 'show_all', is_flag=True, help='Show all habits including inactive')
@click.pass_context
def habit_list(ctx, show_all):
    """📋 List all habits"""
    db = ctx.obj['db']
    view = ConsoleView()
    service = HabitService(db)

    habits = service.get_all_habits(include_inactive=show_all)
    habit_tuples = [(h.name, h.periodicity, h.description, h.is_active) for h in habits]

    if show_all:
        view.show_all_habits_list(habit_tuples)
    else:
        view.show_active_habits_list(habit_tuples)


@cli.command()
@click.argument('name')
@click.option('--new-name', default=None, help='New habit name')
@click.option('--periodicity', type=click.Choice(['daily', 'weekly']), default=None, help='New periodicity')
@click.option('--description', default=None, help='New description')
@click.option('--activate', 'status', flag_value=True, help='Set habit as active')
@click.option('--deactivate', 'status', flag_value=False, help='Set habit as inactive')
@click.pass_context
def edit(ctx, name, new_name, periodicity, description, status):
    """📝 Edit a habit"""
    db = ctx.obj['db']
    view = ConsoleView()
    service = HabitService(db)

    # Get current habit
    habit = service.get_habit_by_name(name)
    if not habit:
        view. show_error(f"Habit '{name}' not found")
        return

    # Use current values if not specified
    final_name = new_name if new_name else habit.name
    final_periodicity = periodicity if periodicity else habit.periodicity
    final_description = description if description is not None else habit.description
    final_status = status if status is not None else habit.is_active

    success, message = service.update_habit(
        name,
        final_name,
        final_periodicity,
        final_description,
        final_status
    )

    if success:
        view. show_habit_updated(name, final_name, final_periodicity, final_status)
    else:
        view.show_error(message)


@cli.command()
@click.pass_context
def champion(ctx):
    """🏆 Show the habit with the longest streak"""
    db = ctx. obj['db']
    view = ConsoleView()
    service = AnalyticsService(db)

    habit_name, habit_streak = service.get_longest_streak_all_habits()

    if habit_name:
        view.console.print()
        view.console.print(f"🏆 [bold gold1]Champion Habit:[/bold gold1] [cyan]{habit_name}[/cyan]")
        view.console. print(f"   [yellow]Longest streak:[/yellow] [green bold]{habit_streak}[/green bold] days")
        view.console.print()
    else:
        view.show_error("No habits found")


@cli.command()
@click.argument('name')
@click.pass_context
def streak(ctx, name):
    """🎯 Show the longest streak for a specific habit"""
    db = ctx. obj['db']
    view = ConsoleView()
    service = AnalyticsService(db)

    longest_streak = service.calculate_longest_streak(name)

    if longest_streak is not None:
        view.console. print()
        view.console. print(f"🎯 [bold cyan]Habit:[/bold cyan] {name}")
        view.console. print(f"   [yellow]Longest streak:[/yellow] [green bold]{longest_streak}[/green bold] days")
        view.console.print()
    else:
        view.show_error(f"Habit '{name}' not found")


if __name__ == '__main__':
    cli(obj={})