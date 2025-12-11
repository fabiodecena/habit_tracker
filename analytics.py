from datetime import datetime, timedelta
from typing import List, Tuple
from database import get_connection


# Functional Programming Module

def get_all_habits(db=None) -> List[Tuple]:
    """
    Returns a list of all currently tracked habits.
    """
    con = db or get_connection()
    cur = con.cursor()
    cur.execute("SELECT name, periodicity FROM habits")
    results = cur.fetchall()
    if not db:
        con.close()
    return results


def get_habits_by_periodicity(periodicity: str, db=None) -> List[Tuple]:
    """
    Returns a list of habits filtered by periodicity.
    Filter is applied using a list comprehension (functional style).
    """
    all_habits = get_all_habits(db)
    # Functional approach: filter
    return list(filter(lambda h: h[1] == periodicity, all_habits))


def get_habit_history(habit_name: str, db=None) -> List[datetime]:
    """
    Returns a sorted list of completion dates for a specific habit.
    """
    con = db or get_connection()
    cur = con.cursor()
    cur.execute("SELECT checked_at FROM tracker WHERE habit_name=?", (habit_name,))
    data = cur.fetchall()
    if not db:
        con.close()
    # Convert strings back to datetime objects and sort
    return sorted([datetime.fromisoformat(row[0]) for row in data])


def calculate_longest_streak(habit_name: str, periodicity: str, db=None) -> int:
    """
    Calculates the longest streak for a given habit.
    """
    history = get_habit_history(habit_name, db)

    if not history:
        return 0

    # Normalize dates based on periodicity to ensure uniform comparison logic.
    # For 'daily', use the date. For 'weekly', use the Monday of that week.
    if periodicity == 'daily':
        normalized_dates = sorted({d.date() for d in history})
        step = timedelta(days=1)
    else:
        # Normalize to the start (Monday) of the ISO week
        normalized_dates = sorted({
            datetime.fromisocalendar(d.isocalendar()[0], d.isocalendar()[1], 1).date()
            for d in history
        })
        step = timedelta(weeks=1)

    if len(normalized_dates) < 2:
        return len(normalized_dates)

    longest_streak = 0
    current_streak = 1

    for i in range(1, len(normalized_dates)):
        prev = normalized_dates[i - 1]
        curr = normalized_dates[i]

        if curr - prev == step:
            current_streak += 1
        else:
            longest_streak = max(longest_streak, current_streak)
            current_streak = 1

    return max(longest_streak, current_streak)


def get_longest_streak_all_habits(db=None) -> Tuple[str, int]:
    """
    Returns the longest streak among all defined habits.
    """
    habits = get_all_habits(db)
    if not habits:
        return "None", 0

    # Map every habit to its max streak
    streaks = map(lambda h: (h[0], calculate_longest_streak(h[0], h[1], db)), habits)

    # Reduce/Max to find the best one
    return max(streaks, key=lambda x: x[1])