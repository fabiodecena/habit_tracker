"""
Application configuration
"""


class Config:
    """Application configuration settings"""
    DATABASE_NAME = "main.db"
    DEFAULT_PERIODICITY_OPTIONS = ['daily', 'weekly']
    SEED_WEEKS = 4
    SEED_SUCCESS_RATE = 0.8  # 80% completion rate for seed data

    # Predefined habits for seeding
    SEED_HABITS = [
        ("Read Journal", "daily"),
        ("Skin Care", "daily"),
        ("Play Music", "daily"),
        ("Water Plants", "weekly"),
        ("Finance Check", "weekly")
    ]