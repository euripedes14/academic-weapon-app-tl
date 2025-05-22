import sqlite3
import openpyxl
from datetime import datetime

def create_database():
    """Creates an SQLite database and all required tables."""
    conn = sqlite3.connect("academic_weapon.db")  # Use a single database file
    cursor = conn.cursor()

    # Enable foreign key support
    cursor.execute("PRAGMA foreign_keys = ON")

# USERS table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS USERS (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        email TEXT NULL,
        pronouns TEXT CHECK (pronouns IN ('he/him', 'she/her', 'they/them', 'any')) NULL,
        password TEXT NOT NULL
    );
    ''')
    # STREAKS table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS STREAKS (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT NULL
    );
    ''')
    # USER_STREAKS table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS USER_STREAKS (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        streak_id INTEGER NOT NULL,
        FOREIGN KEY (user_id) REFERENCES USERS(id),
        FOREIGN KEY (streak_id) REFERENCES STREAKS(id)
    );     
    ''')
    # PROFILE_SETTINGS table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS PROFILE_SETTINGS (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        username TEXT NOT NULL,
        profile_picture BLOB,
        pronouns TEXT CHECK (pronouns IN ('he/him', 'she/her', 'they/them', 'any')),
        FOREIGN KEY (user_id) REFERENCES USERS(id)
    );
    ''')
    # ACCOUNT_SETTINGS table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS ACCOUNT_SETTINGS (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        email TEXT,
        password TEXT,
        location_access INTEGER CHECK (location_access IN (0, 1)),
        FOREIGN KEY (user_id) REFERENCES USERS(id)
    );
    ''')
    conn.commit()

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

    # Create the studying streaks table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS study_streaks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            streak_date TEXT NOT NULL UNIQUE,
            tasks_completed INTEGER NOT NULL
        )
    """)

   # Create the user_courses table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_courses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            course_id TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES USERS(id) ON DELETE CASCADE,
            FOREIGN KEY (course_id) REFERENCES courses(course_id) ON DELETE CASCADE,
            UNIQUE(user_id, course_id)
        )
    """) 

    conn.commit()
    conn.close()

def create_log_tables(conn):
    cur = conn.cursor()

    # Create USERS_LOG table
    cur.execute('''
    CREATE TABLE IF NOT EXISTS USERS_LOG (
        log_id INTEGER PRIMARY KEY AUTOINCREMENT,
        action TEXT NOT NULL,
        id INTEGER,
        username TEXT,
        email TEXT,
        pronouns TEXT,
        password TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    );
    ''')
    # Create STREAKS_LOG table
    cur.execute('''
    CREATE TABLE IF NOT EXISTS STREAKS_LOG (
        log_id INTEGER PRIMARY KEY AUTOINCREMENT,
        action TEXT NOT NULL,
        id INTEGER,
        title TEXT,
        description TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    );
    ''')
     # PROFILE_SETTINGS_LOG table
    cur.execute('''
    CREATE TABLE IF NOT EXISTS PROFILE_SETTINGS_LOG (
        log_id INTEGER PRIMARY KEY AUTOINCREMENT,
        action TEXT NOT NULL,
        id INTEGER,
        user_id INTEGER,
        username TEXT,
        profile_picture BLOB,
        pronouns TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    );
    ''')
    # ACCOUNT_SETTINGS_LOG table
    cur.execute('''
    CREATE TABLE IF NOT EXISTS ACCOUNT_SETTINGS_LOG (
        log_id INTEGER PRIMARY KEY AUTOINCREMENT,
        action TEXT NOT NULL,
        id INTEGER,
        user_id INTEGER,
        email TEXT,
        password TEXT,
        location_access INTEGER,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    );
    ''')
    conn.commit()

def create_triggers(conn):
    cur = conn.cursor()

    # USERS triggers
    cur.execute('''
    CREATE TRIGGER IF NOT EXISTS trg_users_insert
    AFTER INSERT ON USERS
    BEGIN
        INSERT INTO USERS_LOG (action, id, username, email, pronouns, password)
        VALUES ('INSERT', NEW.id, NEW.username, NEW.email, NEW.pronouns, NEW.password);
    END;
    ''')
    cur.execute('''
    CREATE TRIGGER IF NOT EXISTS trg_users_update
    AFTER UPDATE ON USERS
    BEGIN
        INSERT INTO USERS_LOG (action, id, username, email, pronouns, password)
        VALUES ('UPDATE', NEW.id, NEW.username, NEW.email, NEW.pronouns, NEW.password);
    END;
    ''')
    cur.execute('''
    CREATE TRIGGER IF NOT EXISTS trg_users_delete
    AFTER DELETE ON USERS
    BEGIN
        INSERT INTO USERS_LOG (action, id, username, email, pronouns, password)
        VALUES ('DELETE', OLD.id, OLD.username, OLD.email, OLD.pronouns, OLD.password);
    END;
    ''')

    # STREAKS triggers
    cur.execute('''
    CREATE TRIGGER IF NOT EXISTS trg_streaks_insert
    AFTER INSERT ON STREAKS
    BEGIN
        INSERT INTO STREAKS_LOG (action, id, title, description)
        VALUES ('INSERT', NEW.id, NEW.title, NEW.description);
    END;
    ''')
    cur.execute('''
    CREATE TRIGGER IF NOT EXISTS trg_streaks_update
    AFTER UPDATE ON STREAKS
    BEGIN
        INSERT INTO STREAKS_LOG (action, id, title, description)
        VALUES ('UPDATE', NEW.id, NEW.title, NEW.description);
    END;
    ''')
    cur.execute('''
    CREATE TRIGGER IF NOT EXISTS trg_streaks_delete
    AFTER DELETE ON STREAKS
    BEGIN
        INSERT INTO STREAKS_LOG (action, id, title, description)
        VALUES ('DELETE', OLD.id, OLD.title, OLD.description);
    END;
    ''')
     # Trigger: When PROFILE_SETTINGS is updated, update USERS table
    cur.execute('''
    CREATE TRIGGER IF NOT EXISTS trg_profile_settings_update
    AFTER UPDATE ON PROFILE_SETTINGS
    BEGIN
        UPDATE USERS
        SET username = NEW.username,
            pronouns = NEW.pronouns
        WHERE id = NEW.user_id;
    END;
    ''')

    # Trigger: When ACCOUNT_SETTINGS is updated, update USERS table
    cur.execute('''
    CREATE TRIGGER IF NOT EXISTS trg_account_settings_update
    AFTER UPDATE ON ACCOUNT_SETTINGS
    BEGIN
        UPDATE USERS
        SET email = NEW.email,
            password = NEW.password
        WHERE id = NEW.user_id;
    END;
    ''')
    # PROFILE_SETTINGS triggers
    cur.execute('''
    CREATE TRIGGER IF NOT EXISTS trg_profile_settings_insert
    AFTER INSERT ON PROFILE_SETTINGS
    BEGIN
        INSERT INTO PROFILE_SETTINGS_LOG (action, id, user_id, username, profile_picture, pronouns)
        VALUES ('INSERT', NEW.id, NEW.user_id, NEW.username, NEW.profile_picture, NEW.pronouns);
    END;
    ''')
    cur.execute('''
    CREATE TRIGGER IF NOT EXISTS trg_profile_settings_update
    AFTER UPDATE ON PROFILE_SETTINGS
    BEGIN
        INSERT INTO PROFILE_SETTINGS_LOG (action, id, user_id, username, profile_picture, pronouns)
        VALUES ('UPDATE', NEW.id, NEW.user_id, NEW.username, NEW.profile_picture, NEW.pronouns);
        UPDATE USERS
        SET username = NEW.username,
            pronouns = NEW.pronouns
        WHERE id = NEW.user_id;
    END;
    ''')
    cur.execute('''
    CREATE TRIGGER IF NOT EXISTS trg_profile_settings_delete
    AFTER DELETE ON PROFILE_SETTINGS
    BEGIN
        INSERT INTO PROFILE_SETTINGS_LOG (action, id, user_id, username, profile_picture, pronouns)
        VALUES ('DELETE', OLD.id, OLD.user_id, OLD.username, OLD.profile_picture, OLD.pronouns);
    END;
    ''')

    # ACCOUNT_SETTINGS triggers
    cur.execute('''
    CREATE TRIGGER IF NOT EXISTS trg_account_settings_insert
    AFTER INSERT ON ACCOUNT_SETTINGS
    BEGIN
        INSERT INTO ACCOUNT_SETTINGS_LOG (action, id, user_id, email, password, location_access)
        VALUES ('INSERT', NEW.id, NEW.user_id, NEW.email, NEW.password, NEW.location_access);
    END;
    ''')
    cur.execute('''
    CREATE TRIGGER IF NOT EXISTS trg_account_settings_update
    AFTER UPDATE ON ACCOUNT_SETTINGS
    BEGIN
        INSERT INTO ACCOUNT_SETTINGS_LOG (action, id, user_id, email, password, location_access)
        VALUES ('UPDATE', NEW.id, NEW.user_id, NEW.email, NEW.password, NEW.location_access);
        UPDATE USERS
        SET email = NEW.email,
            password = NEW.password
        WHERE id = NEW.user_id;
    END;
    ''')
    cur.execute('''
    CREATE TRIGGER IF NOT EXISTS trg_account_settings_delete
    AFTER DELETE ON ACCOUNT_SETTINGS
    BEGIN
        INSERT INTO ACCOUNT_SETTINGS_LOG (action, id, user_id, email, password, location_access)
        VALUES ('DELETE', OLD.id, OLD.user_id, OLD.email, OLD.password, OLD.location_access);
    END;
    ''')
    conn.commit()

def insert_user(conn, username, password, email, pronouns=None):
    """Insert a user into the USERS table."""
    cur = conn.cursor()
    cur.execute('''
    INSERT INTO USERS (username, password, email, pronouns)
    VALUES (?, ?, ?, ?)
    ''', (username, password, email, pronouns))
    conn.commit()

def check_user_credentials(conn, username, password):
    """Check if a user with the given username and password exists."""
    cur = conn.cursor()
    cur.execute('''
    SELECT * FROM USERS WHERE username = ? AND password = ?
    ''', (username, password))
    return cur.fetchone() is not None

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