"""
Application configuration
"""

class Config:
    """Application configuration settings"""
    DATABASE_NAME = "main.db"
    DEFAULT_PERIODICITY_OPTIONS = ['daily', 'weekly']

    # Test fixture settings (4 weeks as per specification)
    SEED_WEEKS = 4

    # Predefined habits with descriptions and status (test fixtures)
    # Format: (name, periodicity, description, is_active)
    SEED_HABITS = [
        ("Read Journal", "daily", "Read a journal (20-35 minutes)", True),
        ("Skin Care", "daily", "Complete your skincare routine", False),  # INACTIVE
        ("Play Music", "daily", "Practice an instrument for at least 15–30 minutes", True),
        ("Finance Check", "weekly", "Review spending and update your budget/accounts", True),
        ("Water Plants", "weekly", "Water plants and check soil moisture/leaves", True)
    ]