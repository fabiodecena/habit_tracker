from datetime import datetime
from database import get_connection


class Habit:
    """
    Object-Oriented representation of a Habit.
    """

    def __init__(self, name: str, periodicity: str):
        """
        Initialize a habit.
        :param name: Name of the habit
        :param periodicity: 'daily' or 'weekly'
        """
        self.name = name
        self.periodicity = periodicity
        self.created_at = datetime.now().isoformat()

    def store(self, db=None):
        """
        Saves the habit definition to the database.
        """
        con = db or get_connection()
        cur = con.cursor()
        try:
            cur.execute("INSERT OR IGNORE INTO habits VALUES (?, ?, ?)",
                        (self.name, self.periodicity, self.created_at))
            con.commit()
        finally:
            if not db:
                con.close()

    def check_off(self, date_time: datetime = None, db=None):
        """
        Marks the habit as completed for a specific time.
        """
        if date_time is None:
            date_time = datetime.now()

        con = db or get_connection()
        cur = con.cursor()
        try:
            # We store dates as ISO format strings for SQLite
            cur.execute("INSERT INTO tracker VALUES (?, ?)",
                        (self.name, date_time.isoformat()))
            con.commit()
        finally:
            if not db:
                con.close()

    def delete(self, db=None):
        """
        Deletes the habit and its history.
        """
        con = db or get_connection()
        cur = con.cursor()
        try:
            cur.execute("DELETE FROM tracker WHERE habit_name=?", (self.name,))
            cur.execute("DELETE FROM habits WHERE name=?", (self.name,))
            con.commit()
        finally:
            if not db:
                con.close()

    def __str__(self):
        return f"{self.name} ({self.periodicity})"