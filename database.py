import sqlite3
from sqlite3 import Connection


def get_connection(db_name: str = "main.db") -> Connection:
    """
    Creates a connection to the sqlite database.
    """
    con = sqlite3.connect(db_name)
    create_tables(con)
    return con


def create_tables(con: Connection):
    """
    Creates the necessary tables if they do not exist.
    """
    cur = con.cursor()

    # Table for storing habit definitions
    cur.execute("""
        CREATE TABLE IF NOT EXISTS habits (
            name TEXT PRIMARY KEY,
            periodicity TEXT,
            created_at TEXT
        )
    """)

    # Table for storing check-off events
    cur.execute("""
        CREATE TABLE IF NOT EXISTS tracker (
            habit_name TEXT,
            checked_at TEXT,
            FOREIGN KEY (habit_name) REFERENCES habits(name)
        )
    """)
    con.commit()