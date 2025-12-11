import sys
import os
from datetime import datetime, timedelta

# Add the parent directory to a path so we can import modules if running directly
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from habit import Habit
import analytics
from database import get_connection


def seed_predefined_data(db):
    """
    Populates the database with 5 habits and 4 weeks of sample data.
    """
    cur = db.cursor()
    cur.execute("SELECT count(*) FROM habits")
    if cur.fetchone()[0] > 0:
        return  # Data already exists, don't overwrite

    print("Seeding database with 5 predefined habits and 4 weeks of data...")

    # Define Habits
    habits_data = [
        ("Drink Water", "daily"),
        ("Read Book", "daily"),
        ("Exercise", "daily"),
        ("Clean House", "weekly"),
        ("Body Weight Check", "weekly")
    ]

    end_date = datetime.now()
    start_date = end_date - timedelta(weeks=4)

    for name, periodicity in habits_data:
        h = Habit(name, periodicity)
        h.store(db)

        # Generate tracking data
        current = start_date
        while current <= end_date:
            if periodicity == 'daily':
                # Skip some days to make it realistic (80% success rate)
                if int(current.timestamp()) % 5 != 0:
                    h.check_off(current, db)
                current += timedelta(days=1)
            elif periodicity == 'weekly':
                # Check off once per week
                h.check_off(current, db)
                current += timedelta(weeks=1)

    print("Database seeded successfully.")


def print_menu():
    print("\n--- HABIT TRACKER CLI ---")
    print("1. Create a new habit")
    print("2. Delete a habit")
    print("3. Check-off a habit (Complete task)")
    print("4. Analyze: List all habits")
    print("5. Analyze: List habits by periodicity")
    print("6. Analyze: Longest streak of all habits")
    print("7. Analyze: Longest streak for a specific habit")
    print("8. Exit")


def main():
    db = get_connection()
    seed_predefined_data(db)

    while True:
        print_menu()
        choice = input("Enter your choice (1-8): ")

        if choice == '1':
            name = input("Enter habit name: ")
            period = input("Enter periodicity (daily/weekly): ").lower()
            if period in ['daily', 'weekly']:
                h = Habit(name, period)
                h.store(db)
                print(f"Habit '{name}' created!")
            else:
                print("Invalid periodicity. Use 'daily' or 'weekly'.")

        elif choice == '2':
            name = input("Enter habit name to delete: ")
            h = Habit(name, "daily")  # Periodicity doesn't matter for deletion
            h.delete(db)
            print(f"Habit '{name}' deleted (if it existed).")

        elif choice == '3':
            name = input("Enter habit name to check-off: ")
            # We need to find the periodicity to instantiate strictly,
            # but for check-off logic specifically in this simple DB model,
            # we just need the name.
            h = Habit(name, "daily")
            h.check_off(datetime.now(), db)
            print(f"Marked '{name}' as done for today!")

        elif choice == '4':
            habits = analytics.get_all_habits(db)
            print("\nCurrently tracked habits:")
            for h in habits:
                print(f"- {h[0]} ({h[1]})")

        elif choice == '5':
            p = input("Which periodicity? (daily/weekly): ")
            habits = analytics.get_habits_by_periodicity(p, db)
            print(f"\n{p.capitalize()} habits:")
            for h in habits:
                print(f"- {h[0]}")

        elif choice == '6':
            best = analytics.get_longest_streak_all_habits(db)
            print(f"\nThe champion is '{best[0]}' with a streak of {best[1]}!")

        elif choice == '7':
            name = input("Enter habit name: ")
            # Need to fetch periodicity first to calculate correctly
            habits = analytics.get_all_habits(db)
            target = next((h for h in habits if h[0] == name), None)
            if target:
                streak = analytics.calculate_longest_streak(target[0], target[1], db)
                print(f"\nLongest streak for '{name}': {streak}")
            else:
                print("Habit not found.")

        elif choice == '8':
            print("Goodbye!")
            break
        else:
            print("Invalid choice, please try again.")


if __name__ == '__main__':
    main()