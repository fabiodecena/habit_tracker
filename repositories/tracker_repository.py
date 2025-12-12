"""
Tracker Repository - Database operations for tracker events
"""
from typing import List, Optional
from models.tracker import TrackerEvent
from database.connection import Database


class TrackerRepository:
    """
    Handles all database operations for tracker events.
    No business logic - just CRUD operations.
    """

    def __init__(self, db=None):
        """
        Initialize a repository.

        Args:
            db: Database connection (optional)
        """
        self.db = db

    def save(self, event: TrackerEvent) -> bool:
        """
        Records a check-off event.

        Args:
            event: TrackerEvent to save

        Returns:
            True if successful, False otherwise
        """
        con = self.db or Database.get_connection()
        cur = con.cursor()
        try:
            cur.execute(
                "INSERT INTO tracker (event_id, habit_id, checked_at, notes) VALUES (?, ?, ?, ?)",
                (event.event_id, event.habit_id, event.checked_at.isoformat(), event.notes)
            )
            con.commit()
            return True
        except Exception as e:
            print(f"Error saving tracker event:  {e}")
            con.rollback()
            return False
        finally:
            if not self.db:
                con.close()

    def find_by_habit_id(self, habit_id: str) -> List[TrackerEvent]:
        """
        Returns all check-off events for a specific habit.

        Args:
            habit_id:  Habit ID

        Returns:
            List of TrackerEvent objects sorted by date
        """
        con = self.db or Database.get_connection()
        cur = con.cursor()
        cur.execute(
            """
            SELECT event_id, habit_id, checked_at, notes
            FROM tracker
            WHERE habit_id = ?
            ORDER BY checked_at
            """,
            (habit_id,)
        )
        results = cur.fetchall()
        if not self.db:
            con.close()
        return [TrackerEvent.from_tuple(row) for row in results]

    def find_by_habit_name(self, habit_name: str) -> List[TrackerEvent]:
        """
        Returns all check-off events for a specific habit by name.

        Args:
            habit_name: Habit name

        Returns:
            List of TrackerEvent objects sorted by date
        """
        con = self.db or Database.get_connection()
        cur = con.cursor()
        cur.execute(
            """
            SELECT t.event_id, t.habit_id, t.checked_at, t.notes
            FROM tracker t
            INNER JOIN habits h ON t.habit_id = h.habit_id
            WHERE h.name = ? 
            ORDER BY t.checked_at
            """,
            (habit_name,)
        )
        results = cur.fetchall()
        if not self.db:
            con.close()
        return [TrackerEvent.from_tuple(row) for row in results]

    def find_all(self) -> List[TrackerEvent]:
        """
        Returns all tracker events.

        Returns:
            List of TrackerEvent objects
        """
        con = self.db or Database.get_connection()
        cur = con.cursor()
        cur.execute("""
            SELECT event_id, habit_id, checked_at, notes
            FROM tracker
            ORDER BY checked_at DESC
        """)
        results = cur.fetchall()
        if not self.db:
            con.close()
        return [TrackerEvent.from_tuple(row) for row in results]

    def delete_by_habit_id(self, habit_id: str) -> bool:
        """
        Deletes all tracker events for a habit.

        Args:
            habit_id: Habit ID

        Returns:
            True if successful, False otherwise
        """
        con = self.db or Database.get_connection()
        cur = con.cursor()
        try:
            cur.execute("DELETE FROM tracker WHERE habit_id = ?", (habit_id,))
            con.commit()
            return True
        except Exception as e:
            print(f"Error deleting tracker events: {e}")
            con.rollback()
            return False
        finally:
            if not self.db:
                con.close()

    def delete_by_event_id(self, event_id: str) -> bool:
        """
        Deletes a specific tracker event.

        Args:
            event_id: Event ID

        Returns:
            True if successful, False otherwise
        """
        con = self.db or Database.get_connection()
        cur = con.cursor()
        try:
            cur.execute("DELETE FROM tracker WHERE event_id = ?", (event_id,))
            con.commit()
            return True
        except Exception as e:
            print(f"Error deleting tracker event: {e}")
            con.rollback()
            return False
        finally:
            if not self.db:
                con.close()

    def update_notes(self, event_id: str, notes: str) -> bool:
        """
        Updates notes for a specific tracker event.

        Args:
            event_id: Event ID
            notes: New notes

        Returns:
            True if successful, False otherwise
        """
        con = self.db or Database.get_connection()
        cur = con.cursor()
        try:
            cur.execute(
                "UPDATE tracker SET notes = ? WHERE event_id = ?",
                (notes, event_id)
            )
            con.commit()
            return True
        except Exception as e:
            print(f"Error updating notes: {e}")
            con.rollback()
            return False
        finally:
            if not self.db:
                con.close()

    def find_by_event_id(self, event_id: str) -> Optional['TrackerEvent']:
        """
        Find a tracker event by ID.

        Args:
            event_id: Event ID

        Returns:
            TrackerEvent or None
        """
        from models.tracker import TrackerEvent

        con = self.db or Database.get_connection()
        cur = con.cursor()
        cur.execute(
            """
            SELECT event_id, habit_id, checked_at, notes
            FROM tracker
            WHERE event_id = ?
            """,
            (event_id,)
        )
        result = cur.fetchone()
        if not self.db:
            con.close()
        return TrackerEvent.from_tuple(result) if result else None