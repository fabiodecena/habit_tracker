"""
Pure Habit data model (DTO - Data Transfer Object)
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional
import uuid


@dataclass
class Habit:
    """
    Represents a habit entity.
    This is a pure data class with no business logic.
    """
    name: str
    periodicity: str
    habit_id: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    comments: str = ""
    is_active: bool = True

    def __post_init__(self):
        """Set default values if not provided"""
        if self.habit_id is None:
            self.habit_id = str(uuid.uuid4())

        if self.created_at is None:
            self.created_at = datetime.now()

        if self.updated_at is None:
            self.updated_at = datetime.now()

    def to_dict(self) -> dict:
        """Convert to dictionary for serialization"""
        return {
            'habit_id': self.habit_id,
            'name': self.name,
            'periodicity': self.periodicity,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'comments': self.comments,
            'is_active': self.is_active
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Habit':
        """Create from a dictionary"""
        return cls(
            habit_id=data.get('habit_id'),
            name=data['name'],
            periodicity=data['periodicity'],
            created_at=datetime.fromisoformat(data['created_at']) if data.get('created_at') else None,
            updated_at=datetime.fromisoformat(data['updated_at']) if data.get('updated_at') else None,
            comments=data.get('comments', ''),
            is_active=data.get('is_active', True)
        )

    @classmethod
    def from_tuple(cls, data: tuple) -> 'Habit':
        """
        Create from a database tuple.
        Expected format: (habit_id, name, periodicity, created_at, updated_at, comments, is_active)
        """
        return cls(
            habit_id=data[0] if len(data) > 0 else None,
            name=data[1] if len(data) > 1 else "",
            periodicity=data[2] if len(data) > 2 else "daily",
            created_at=datetime.fromisoformat(data[3]) if len(data) > 3 and data[3] else None,
            updated_at=datetime.fromisoformat(data[4]) if len(data) > 4 and data[4] else None,
            comments=data[5] if len(data) > 5 else "",
            is_active=bool(data[6]) if len(data) > 6 else True
        )

    def update_timestamp(self):
        """Update the updated_at timestamp"""
        self.updated_at = datetime.now()

    def __str__(self):
        status = "Active" if self.is_active else "Inactive"
        return f"{self.name} ({self.periodicity}) - {status}"

    def __repr__(self):
        return f"Habit(id={self.habit_id}, name={self.name}, periodicity={self.periodicity})"