import sqlite3

def create_database():
    """Creates an SQLite database and all required tables."""
    conn = sqlite3.connect("academic_weapon.db")  # Use a single database file
    cursor = conn.cursor()

# Drop existing tables if they exist
    cursor.execute("DROP TABLE IF EXISTS courses")
    cursor.execute("DROP TABLE IF EXISTS transactions")
    cursor.execute("DROP TABLE IF EXISTS categories")
    cursor.execute("DROP TABLE IF EXISTS future_spendings")
    cursor.execute("DROP TABLE IF EXISTS repeating_spendings")
    cursor.execute("DROP TABLE IF EXISTS tasks")
    cursor.execute("DROP TABLE IF EXISTS pomodoro_sessions")
    cursor.execute("DROP TABLE IF EXISTS study_streaks")
    cursor.execute("DROP TABLE IF EXISTS user_courses")
    cursor.execute("DROP TABLE IF EXISTS USERS")
    cursor.execute("DROP TABLE IF EXISTS STREAKS")
    cursor.execute("DROP TABLE IF EXISTS USER_STREAKS")
    cursor.execute("DROP TABLE IF EXISTS PROFILE_SETTINGS")
    cursor.execute("DROP TABLE IF EXISTS ACCOUNT_SETTINGS")
    cursor.execute("DROP TABLE IF EXISTS USERS_LOG")
    cursor.execute("DROP TABLE IF EXISTS STREAKS_LOG")
    cursor.execute("DROP TABLE IF EXISTS PROFILE_SETTINGS_LOG")
    cursor.execute("DROP TABLE IF EXISTS ACCOUNT_SETTINGS_LOG")

    conn.commit()
    conn.close()