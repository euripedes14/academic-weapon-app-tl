import sqlite3
import openpyxl
from datetime import datetime

def create_database():
    """Creates an SQLite database and all required tables."""
    conn = sqlite3.connect("academic_weapon.db")  # Use a single database file
    cursor = conn.cursor()

    # Enable foreign key support
    cursor.execute("PRAGMA foreign_keys = ON")

    # Drop existing tables if they exist
    cursor.execute("DROP TABLE IF EXISTS courses")
    cursor.execute("DROP TABLE IF EXISTS transactions")
    cursor.execute("DROP TABLE IF EXISTS categories")
    cursor.execute("DROP TABLE IF EXISTS future_spendings")
    cursor.execute("DROP TABLE IF EXISTS repeating_spendings")
    cursor.execute("DROP TABLE IF EXISTS tasks")
    cursor.execute("DROP TABLE IF EXISTS pomodoro_sessions")
    cursor.execute("DROP TABLE IF EXISTS streaks")


    # Create the courses table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS courses (
            course_id TEXT PRIMARY KEY NOT NULL,
            course_name TEXT NOT NULL,
            department TEXT NOT NULL,
            semester INTEGER NOT NULL,
            ects INTEGER NOT NULL,
            professor TEXT,
            study_hours INTEGER,
            day TEXT,
            start_time TEXT,
            end_time TEXT,
            UNIQUE(course_id)
        )
    """)

    # Create the categories table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL
        )
    """)

    # Create the transactions table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category_id INTEGER NOT NULL,
            amount REAL NOT NULL,
            date TEXT NOT NULL,
            FOREIGN KEY (category_id) REFERENCES categories (id) ON DELETE CASCADE
        )
    """)

    # Create the future_spendings table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS future_spendings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category_id INTEGER NOT NULL,
            amount REAL NOT NULL,
            date TEXT NOT NULL,
            FOREIGN KEY (category_id) REFERENCES categories (id) ON DELETE CASCADE
        )
    """)

    # Create the repeating_spendings table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS repeating_spendings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category_id INTEGER NOT NULL,
            amount REAL NOT NULL,
            frequency INTEGER NOT NULL,
            FOREIGN KEY (category_id) REFERENCES categories (id) ON DELETE CASCADE
        )
    """)

    # Create the tasks table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task_name TEXT NOT NULL,
            is_completed BOOLEAN NOT NULL DEFAULT 0,
            created_at TEXT NOT NULL,
            completed_at TEXT
        )
    """)

    # Create the pomodoro_sessions table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pomodoro_sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            work_duration INTEGER NOT NULL,
            break_duration INTEGER NOT NULL,
            is_completed BOOLEAN NOT NULL DEFAULT 0,
            session_date TEXT NOT NULL
        )
    """)

    # Create the streaks table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS streaks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            streak_date TEXT NOT NULL UNIQUE,
            tasks_completed INTEGER NOT NULL
        )
    """)

    conn.commit()
    conn.close()

def insert_courses_from_xlsx(file_path):
    """Reads data from an XLSX file and inserts it into the courses table."""
    conn = sqlite3.connect("academic_weapon.db")  # Use the same database
    cursor = conn.cursor()

    # Load the workbook and select the active sheet
    wb = openpyxl.load_workbook(file_path)
    sheet = wb.active

    # Iterate through the rows and insert data into the table
    for row in sheet.iter_rows(min_row=2, values_only=True):  # Skip the header row
        course_id = row[0]  
        course_name = row[1]  
        department = row[2]   
        semester = row[3]     
        ects = row[4]        
        professor = row[5]    
        study_hours = row[6]  
        day = row[7]         
        start_time = row[8]  
        end_time = row[9]    

        if course_name and department and semester and ects:  # Ensure required data is not empty
            cursor.execute("""
                INSERT INTO courses (
                    course_id, course_name, department, semester, ects, professor, study_hours, day, start_time, end_time
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (course_id, course_name, department, semester, ects, professor, study_hours, day, start_time, end_time))

    conn.commit()
    conn.close()

def insert_category(name):
    """Inserts a new category into the categories table."""
    conn = sqlite3.connect("academic_weapon.db")
    cursor = conn.cursor()
    cursor.execute("INSERT OR IGNORE INTO categories (name) VALUES (?)", (name,))
    conn.commit()
    conn.close()

def insert_transaction(category_name, amount, date):
    """Inserts a new transaction into the transactions table."""
    conn = sqlite3.connect("academic_weapon.db")
    cursor = conn.cursor()

    # Get the category ID
    cursor.execute("SELECT id FROM categories WHERE name = ?", (category_name,))
    category_id = cursor.fetchone()
    if category_id:
        category_id = category_id[0]
        cursor.execute("INSERT INTO transactions (category_id, amount, date) VALUES (?, ?, ?)",
                       (category_id, amount, date))
    conn.commit()
    conn.close()

def insert_future_spending(category_name, amount, date):
    """Inserts a new future spending into the future_spendings table."""
    conn = sqlite3.connect("academic_weapon.db")
    cursor = conn.cursor()

    # Get the category ID
    cursor.execute("SELECT id FROM categories WHERE name = ?", (category_name,))
    category_id = cursor.fetchone()
    if category_id:
        category_id = category_id[0]
        cursor.execute("INSERT INTO future_spendings (category_id, amount, date) VALUES (?, ?, ?)",
                       (category_id, amount, date))
    conn.commit()
    conn.close()

def insert_repeating_spending(category_name, amount, frequency):
    """Inserts a new repeating spending into the repeating_spendings table."""
    conn = sqlite3.connect("academic_weapon.db")
    cursor = conn.cursor()

    # Get the category ID
    cursor.execute("SELECT id FROM categories WHERE name = ?", (category_name,))
    category_id = cursor.fetchone()
    if category_id:
        category_id = category_id[0]
        cursor.execute("INSERT INTO repeating_spendings (category_id, amount, frequency) VALUES (?, ?, ?)",
                       (category_id, amount, frequency))
    conn.commit()
    conn.close()

    def insert_task(task_name):
        conn = sqlite3.connect("academic_weapon.db")
        cursor = conn.cursor()
        created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute("INSERT INTO tasks (task_name, is_completed, created_at) VALUES (?, 0, ?)", (task_name, created_at))
        conn.commit()
        conn.close()

    def complete_task(task_id):
        conn = sqlite3.connect("academic_weapon.db")
        cursor = conn.cursor()
        completed_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute("UPDATE tasks SET is_completed = 1, completed_at = ? WHERE id = ?", (completed_at, task_id))
        conn.commit()
        conn.close()

    def insert_pomodoro_session(work_duration, break_duration, is_completed):
        conn = sqlite3.connect("academic_weapon.db")
        cursor = conn.cursor()
        session_date = datetime.now().strftime("%Y-%m-%d")
        cursor.execute("""
        INSERT INTO pomodoro_sessions (work_duration, break_duration, is_completed, session_date)
        VALUES (?, ?, ?, ?)
        """, (work_duration, break_duration, is_completed, session_date))
        conn.commit()
        conn.close()

    def update_streaks(tasks_completed):
        conn = sqlite3.connect("academic_weapon.db")
        cursor = conn.cursor()
        streak_date = datetime.now().strftime("%Y-%m-%d")
        cursor.execute("""
        INSERT OR REPLACE INTO streaks (streak_date, tasks_completed)
        VALUES (?, ?)
        """, (streak_date, tasks_completed))
        conn.commit()
        conn.close()

if __name__ == "__main__":
    # Create the database and tables
    create_database()

    # Insert sample categories
    categories = ["Travel", "Supermarket", "Rent", "Bills", "Coffee", "Entertainment"]
    for category in categories:
        insert_category(category)

    # Path to the XLSX file
    xlsx_file_path = "ceid_courses.xlsx"

    # Insert data from the XLSX file into the courses table
    insert_courses_from_xlsx(xlsx_file_path)

    print("All tables have been created, and sample data has been successfully inserted into the database.")