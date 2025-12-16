"""
Application configuration
"""

class Config:
    """Application configuration settings"""
    DATABASE_NAME = "main. db"
    DEFAULT_PERIODICITY_OPTIONS = ['daily', 'weekly']
    SEED_WEEKS = 4
    SEED_SUCCESS_RATE = 0.8  # 80% completion rate for seed data

    # Predefined habits for seeding (name, periodicity, description)
    SEED_HABITS = [
        ("Read Journal", "daily", "Read a journal (20-35 minutes)"),
        ("Skin Care", "daily", "Complete your skincare routine"),
        ("Play Music", "daily", "Practice an instrument for at least 15–30 minutes"),
        ("Finance Check", "weekly", "Review spending and update your budget/accounts"),
        ("Water Plants", "weekly", "Water plants and check soil moisture/leaves")
    ]