"""
Habit Repository - Database operations for habits
"""
from datetime import datetime
from typing import List, Optional
from models.habit import Habit
from database.connection import Database


class HabitRepository:
    """
    Handles all database operations for habits.
    No business logic - just CRUD operations.
    """

    def __init__(self, db=None):
        """
        Initialize a repository.

        Args:
            db: Database connection (optional)
        """
        self.db = db

    def save(self, habit: Habit) -> bool:
        """
        Saves a habit to the database.

        Args:
            habit: Habit object to save

        Returns:
            True if successful, False otherwise
        """
        con = self.db or Database.get_connection()
        cur = con.cursor()
        try:
            cur.execute(
                """
                INSERT INTO habits (habit_id, name, periodicity, created_at, updated_at, description, is_active)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    habit.habit_id,
                    habit.name,
                    habit.periodicity,
                    habit.created_at.isoformat(),
                    habit.updated_at.isoformat(),
                    habit.description,
                    1 if habit.is_active else 0
                )
            )
            con.commit()
            return True
        except Exception as e:
            print(f"Error saving habit: {e}")
            con.rollback()
            return False
        finally:
            if not self.db:
                con.close()

    def find_all(self, include_inactive: bool = False) -> List[Habit]:
        """
        Returns all habits from the database.
        Daily habits first, then weekly. Within each group, the newest first.

        Args:
            include_inactive: Whether to include inactive habits

        Returns:
            List of Habit objects ordered by periodicity (daily first), then by creation date (the newest first)
        """
        con = self.db or Database.get_connection()
        cur = con.cursor()

        cur.execute("""
            SELECT habit_id, name, periodicity, created_at, updated_at, description, is_active
            FROM habits
        """)

        results = cur.fetchall()
        if not self.db:
            con.close()

        # Functional approach: map, filter, sort
        habits = map(Habit.from_tuple, results)

        # Filter inactive habits if needed
        if not include_inactive:
            habits = filter(lambda h: h.is_active, habits)

        # Define sorting key function (functional approach)
        def get_sort_key(habit: Habit) -> tuple:
            """
            Returns tuple for sorting:
            - First element: periodicity priority (daily=1, weekly=2, other=3)
            - Second element: negative timestamp (for descending order)
            """
            periodicity_map = {'daily': 1, 'weekly': 2}
            periodicity_priority = periodicity_map.get(habit.periodicity, 3)
            creation_time = -habit.created_at.timestamp()  # Negative for descending

            return periodicity_priority, creation_time

        # Sort using a functional key
        return sorted(habits, key=get_sort_key)

    def find_by_id(self, habit_id: str) -> Optional[Habit]:
        """
        Find a habit by ID.

        Args:
            habit_id: Habit ID

        Returns:
            Habit object or None
        """
        con = self.db or Database.get_connection()
        cur = con.cursor()
        cur.execute(
            """
            SELECT habit_id, name, periodicity, created_at, updated_at, description, is_active
            FROM habits
            WHERE habit_id = ? 
            """,
            (habit_id,)
        )
        result = cur.fetchone()
        if not self.db:
            con.close()
        return Habit.from_tuple(result) if result else None

    def find_by_name(self, name: str) -> Optional[Habit]:
        """
        Find a habit by name.

        Args:
            name: Habit name

        Returns:
            Habit object or None
        """
        con = self.db or Database.get_connection()
        cur = con.cursor()
        cur.execute(
            """
            SELECT habit_id, name, periodicity, created_at, updated_at, description, is_active
            FROM habits
            WHERE name = ?  
            """,
            (name,)
        )
        result = cur.fetchone()
        if not self.db:
            con.close()
        return Habit.from_tuple(result) if result else None

    def find_by_periodicity(self, periodicity: str, include_inactive: bool = False) -> List[Habit]:
        """
        Returns habits filtered by periodicity.

        Args:
            periodicity: 'daily' or 'weekly'
            include_inactive: Whether to include inactive habits

        Returns:
            List of Habit objects
        """
        con = self.db or Database.get_connection()
        cur = con.cursor()

        if include_inactive:
            cur.execute(
                """
                SELECT habit_id, name, periodicity, created_at, updated_at, description, is_active
                FROM habits
                WHERE periodicity = ? 
                ORDER BY created_at DESC
                """,
                (periodicity,)
            )
        else:
            cur.execute(
                """
                SELECT habit_id, name, periodicity, created_at, updated_at, description, is_active
                FROM habits
                WHERE periodicity = ? 
                ORDER BY created_at DESC
                """,
                (periodicity,)
            )

        results = cur.fetchall()
        if not self.db:
            con.close()
        return [Habit.from_tuple(row) for row in results]

    def update(self, habit: Habit) -> bool:
        """
        Updates a habit in the database.

        Args:
            habit: Updated Habit object

        Returns:
            True if successful, False otherwise
        """
        con = self.db or Database.get_connection()
        cur = con.cursor()
        try:
            habit.update_timestamp()  # Update the updated_at timestamp

            cur.execute(
                """
                UPDATE habits
                SET name = ?, 
                    periodicity = ?, 
                    updated_at = ?, 
                    is_active = ?,
                    description = ? 
                WHERE habit_id = ?
                """,
                (
                    habit.name,
                    habit.periodicity,
                    habit.updated_at.isoformat(),
                    1 if habit.is_active else 0,
                    habit.description,
                    habit.habit_id
                )
            )
            con.commit()
            return True
        except Exception as e:
            print(f"Error updating habit: {e}")
            con.rollback()
            return False
        finally:
            if not self.db:
                con.close()

    def delete(self, habit_id: str, soft_delete: bool = True) -> bool:
        """
        Deletes a habit.

        Args:
            habit_id: Habit ID
            soft_delete: If True, mark as inactive instead of deleting

        Returns:
            True if successful, False otherwise
        """
        con = self.db or Database.get_connection()
        cur = con.cursor()
        try:
            if soft_delete:
                # Soft delete - just mark as inactive
                cur.execute(
                    "UPDATE habits SET is_active = 0, updated_at = ?  WHERE habit_id = ?",
                    (datetime.now().isoformat(), habit_id)
                )
            else:
                # Hard delete - actually remove from a database
                cur.execute("DELETE FROM tracker WHERE habit_id = ?", (habit_id,))
                cur.execute("DELETE FROM habits WHERE habit_id = ?", (habit_id,))

            con.commit()
            return True
        except Exception as e:
            print(f"Error deleting habit: {e}")
            con.rollback()
            return False
        finally:
            if not self.db:
                con.close()

    def count(self, include_inactive: bool = False) -> int:
        """
        Returns the total number of habits.

        Args:
            include_inactive: Whether to include inactive habits

        Returns:
            Number of habits
        """
        con = self.db or Database.get_connection()
        cur = con.cursor()

        if include_inactive:
            cur.execute("SELECT count(*) FROM habits")
        else:
            cur.execute("SELECT count(*) FROM habits WHERE is_active = 1")

        count = cur.fetchone()[0]
        if not self.db:
            con.close()
        return count