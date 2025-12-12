"""
Pure Tracker data model (DTO)
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional
import uuid


@dataclass
class TrackerEvent:
    """
    Represents a single check-off event.
    This is a pure data class with no business logic.
    """
    habit_id: str
    checked_at: datetime
    event_id: Optional[str] = None
    notes: str = ""

    def __post_init__(self):
        """Set default event_id if not provided"""
        if self.event_id is None:
            self.event_id = str(uuid.uuid4())

    def to_dict(self) -> dict:
        """Convert to dictionary for serialization"""
        return {
            'event_id': self.event_id,
            'habit_id': self. habit_id,
            'checked_at': self.checked_at.isoformat(),
            'notes': self.notes
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'TrackerEvent':
        """Create from a dictionary"""
        return cls(
            event_id=data.get('event_id'),
            habit_id=data['habit_id'],
            checked_at=datetime.fromisoformat(data['checked_at']),
            notes=data.get('notes', '')
        )

    @classmethod
    def from_tuple(cls, data: tuple) -> 'TrackerEvent':
        """
        Create from a database tuple.
        Expected format: (event_id, habit_id, checked_at, notes)
        """
        return cls(
            event_id=data[0] if len(data) > 0 else None,
            habit_id=data[1] if len(data) > 1 else "",
            checked_at=datetime. fromisoformat(data[2]) if len(data) > 2 else datetime.now(),
            notes=data[3] if len(data) > 3 else ""
        )

    def __str__(self):
        return f"Completion at {self.checked_at.strftime('%Y-%m-%d %H:%M')}"

    def __repr__(self):
        return f"TrackerEvent(id={self.event_id}, habit_id={self.habit_id}, checked_at={self.checked_at})"