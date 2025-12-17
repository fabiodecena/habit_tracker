"""
Database connection and schema management
"""
import sqlite3
from sqlite3 import Connection
from config import Config


class Database:
    """Handles database connection and schema"""

    @staticmethod
    def get_connection(db_name: str = None) -> Connection:
        """
        Creates a connection to the sqlite database.

        Args:
            db_name: Database filename (defaults to Config.DATABASE_NAME)

        Returns:
            SQLite connection object
        """
        if db_name is None:
            db_name = Config.DATABASE_NAME

        con = sqlite3.connect(db_name)
        Database.create_tables(con)
        return con

    @staticmethod
    def create_tables(con: Connection):
        """
        Creates the necessary tables if they do not exist.

        Args:
            con: SQLite connection object
        """
        cur = con.cursor()

        # Table for storing habit definitions
        cur.execute("""
            CREATE TABLE IF NOT EXISTS habits (
                habit_id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                periodicity TEXT NOT NULL,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                description TEXT DEFAULT '',
                is_active INTEGER DEFAULT 1
            )
        """)

        # Create an index on name for faster lookups
        cur.execute("""
            CREATE INDEX IF NOT EXISTS idx_habit_name 
            ON habits(name)
        """)

        # Table for storing check-off events
        cur.execute("""
            CREATE TABLE IF NOT EXISTS tracker (
                event_id TEXT PRIMARY KEY,
                habit_id TEXT NOT NULL,
                checked_at TEXT NOT NULL,
                notes TEXT DEFAULT '',
                FOREIGN KEY (habit_id) REFERENCES habits(habit_id) ON DELETE CASCADE
            )
        """)

        # Create an index on habit_id for faster lookups
        cur.execute("""
            CREATE INDEX IF NOT EXISTS idx_tracker_habit 
            ON tracker(habit_id)
        """)

        # Create an index on checked_at for date-based queries
        cur.execute("""
            CREATE INDEX IF NOT EXISTS idx_tracker_date 
            ON tracker(checked_at)
        """)

        con.commit()