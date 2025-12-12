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
    """✨ Habit Tracker CLI - Build better habits!   ✨"""
    db = Database. get_connection()
    seed_predefined_data(db)

    # Store db in context for other commands
    ctx.ensure_object(dict)
    ctx.obj['db'] = db

    # If no subcommand is provided, show the interactive menu
    if ctx.invoked_subcommand is None:
        menu = MenuController(db)
        menu.run()


# ============ Direct CLI Commands ============

@cli.command()
@click.argument('name')
@click.argument('periodicity', type=click.Choice(['daily', 'weekly']))
@click.pass_context
def create(ctx, name, periodicity):
    """✨ Create a new habit"""
    db = ctx.obj['db']
    view = ConsoleView()
    service = HabitService(db)

    success, message = service.create_habit(name, periodicity)

    if success:
        view.show_habit_created(name)
    else:
        view.show_error(message)


@cli.command()
@click.argument('name')
@click.pass_context
def delete(ctx, name):
    """🗑️ Delete a habit"""
    db = ctx.obj['db']
    view = ConsoleView()
    service = HabitService(db)

    success, message = service.delete_habit(name)

    if success:
        view.show_habit_deleted(name)
    else:
        view.show_error(message)


@cli.command()
@click.argument('name')
@click.option('--notes', default='', help='Optional notes for this check-off')
@click.pass_context
def checkoff(ctx, name, notes):
    """✅ Check-off a habit (mark as complete)"""
    db = ctx.obj['db']
    view = ConsoleView()
    service = TrackerService(db)

    success, message = service.check_off_habit(name, datetime.now(), notes)

    if success:
        view. show_habit_checked_off(name)
    else:
        view.show_error(message)


@cli.command()
@click.argument('old_name')
@click.option('--new-name', help='New name for the habit')
@click.option('--periodicity', type=click.Choice(['daily', 'weekly']), help='New periodicity')
@click.option('--comments', help='Comments about the habit')
@click.pass_context
def edit(ctx, old_name, new_name, periodicity, comments):
    """✏️ Edit a habit's name or periodicity"""
    db = ctx.obj['db']
    view = ConsoleView()
    habit_service = HabitService(db)

    # Get existing habit
    habit = habit_service.get_habit_by_name(old_name)
    if not habit:
        view.show_habit_not_found(old_name)
        return

    # Use existing values if not provided
    final_name = new_name if new_name else old_name
    final_periodicity = periodicity if periodicity else habit.periodicity
    final_comments = comments if comments is not None else habit.comments

    # Update comments on the habit object
    if comments is not None:
        habit.comments = final_comments

    success, message = habit_service.update_habit(old_name, final_name, final_periodicity)

    if success:
        view.show_habit_updated(old_name, final_name, final_periodicity)
    else:
        view.show_error(message)


@cli.command()
@click.pass_context
def habits_list(ctx):
    """📋 List all habits"""
    db = ctx.obj['db']
    view = ConsoleView()
    service = HabitService(db)

    habits = service.get_all_habits()
    habit_tuples = [(h.name, h.periodicity) for h in habits]
    view.show_habits_list(habit_tuples)


@cli.command()
@click.argument('periodicity', type=click.Choice(['daily', 'weekly']))
@click.pass_context
def habits_filter(ctx, periodicity):
    """🔍 List habits by periodicity"""
    db = ctx.obj['db']
    view = ConsoleView()
    service = HabitService(db)

    habits = service.get_habits_by_periodicity(periodicity)
    habit_tuples = [(h. name, h.periodicity) for h in habits]
    view. show_filtered_habits(periodicity, habit_tuples)


@cli.command()
@click.pass_context
def champion(ctx):
    """🏆 Show the habit with the longest habit_streak"""
    db = ctx. obj['db']
    view = ConsoleView()
    service = AnalyticsService(db)

    habit_name, habit_streak = service.get_longest_streak_all_habits()
    view.show_longest_streak_all(habit_name, habit_streak)


@cli.command()
@click.argument('name')
@click.pass_context
def streak(ctx, name):
    """🎯 Show the longest streak for a specific habit"""
    db = ctx. obj['db']
    view = ConsoleView()
    habit_service = HabitService(db)
    analytics_service = AnalyticsService(db)

    habit = habit_service.get_habit_by_name(name)
    if habit:
        streak_count = analytics_service.calculate_longest_streak(name)
        view.show_longest_streak_specific(name, streak_count)
    else:
        view.show_habit_not_found(name)


if __name__ == '__main__':
    cli(obj={})