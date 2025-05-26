import sqlite3

def view_table(table_name):
    """Fetch and display all rows from the specified table."""
    conn = sqlite3.connect("academic_weapon.db")
    cursor = conn.cursor()

    try:
        # Query the specified table
        cursor.execute(f"SELECT * FROM {table_name}")
        rows = cursor.fetchall()

        # Print the rows
        print(f"\nContents of table '{table_name}':")
        for row in rows:
            print(row)
    except sqlite3.OperationalError as e:
        print(f"Error: {e}")
    finally:
        conn.close()

def view_all_tables():
    """Fetch and display all rows from all tables."""
    tables = [
        "courses",
        "categories",
        "transactions",
        "future_spendings",
        "repeating_spendings",
        "pomodoro_sessions",
        "streaks"
    ]
    for table in tables:
        view_table(table)

if __name__ == "__main__":
    # View all tables
    view_all_tables()