"""
CLI entry point using Click
"""
import click
from datetime import datetime
from database.connection import get_connection
from models.habit import Habit
from models.tracker import Tracker
from utils.seed_data import seed_predefined_data
from controllers.menu_controller import MenuController
from views.console_view import ConsoleView


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

    habit = Habit(name, periodicity)
    habit.create(db)
    view.show_habit_created(name)


@cli.command()
@click.argument('name')
@click.pass_context
def delete(ctx, name):
    """🗑️ Delete a habit"""
    db = ctx.obj['db']
    view = ConsoleView()

    habit = Habit(name, "daily")
    habit.delete(db)
    view.show_habit_deleted(name)


@cli.command()
@click.argument('name')
@click.pass_context
def checkoff(ctx, name):
    """✅ Check-off a habit (mark as complete)"""
    db = ctx.obj['db']
    view = ConsoleView()

    Tracker.check_off(name, datetime.now(), db)
    view.show_habit_checked_off(name)


@cli.command()
@click.argument('old_name')
@click.option('--new-name', help='New name for the habit')
@click.option('--periodicity', type=click.Choice(['daily', 'weekly']), help='New periodicity')
@click.pass_context
def edit(ctx, old_name, new_name, periodicity):
    """✏️ Edit a habit's name or periodicity"""
    db = ctx.obj['db']
    view = ConsoleView()

    target_habit = Habit.find_by_name(old_name, db)

    if not target_habit:
        view.show_habit_not_found(old_name)
        return

    final_name = new_name if new_name else old_name
    final_periodicity = periodicity if periodicity else target_habit[1]

    if Habit.update(old_name, final_name, final_periodicity, db):
        view.show_habit_updated(old_name, final_name, final_periodicity)
    else:
        view.show_error("Error updating habit.")


@cli.command()
@click.pass_context
def list(ctx):
    """📋 List all habits"""
    db = ctx.obj['db']
    view = ConsoleView()

    habits = Habit.get_all(db)
    view.show_habits_list(habits)


@cli.command()
@click.argument('periodicity', type=click.Choice(['daily', 'weekly']))
@click.pass_context
def filter(ctx, periodicity):
    """🔍 List habits by periodicity"""
    db = ctx.obj['db']
    view = ConsoleView()

    habits = Habit.get_by_periodicity(periodicity, db)
    view.show_filtered_habits(periodicity, habits)


@cli.command()
@click.pass_context
def champion(ctx):
    """🏆 Show the habit with the longest streak"""
    db = ctx.obj['db']
    view = ConsoleView()

    habit_name, streak = Tracker.get_longest_streak_all(db)
    view.show_longest_streak_all(habit_name, streak)


@cli.command()
@click.argument('name')
@click.pass_context
def streak(ctx, name):
    """🎯 Show the longest streak for a specific habit"""
    db = ctx.obj['db']
    view = ConsoleView()

    target = Habit.find_by_name(name, db)

    if target:
        streak_count = Tracker.calculate_longest_streak(target[0], target[1], db)
        view.show_longest_streak_specific(name, streak_count)
    else:
        view.show_habit_not_found(name)


if __name__ == '__main__':
    cli(obj={})