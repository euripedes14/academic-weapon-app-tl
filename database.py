import sqlite3

DB_NAME = "students.db"

def create_database():
    """Connect to the SQLite database (creates the file if it doesn't exist)."""
    conn = sqlite3.connect(DB_NAME)
    return conn

def create_tables(conn):
    cur = conn.cursor()

    # USERS table
    cur.execute('''
    CREATE TABLE IF NOT EXISTS USERS (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        email TEXT NULL,
        pronouns TEXT CHECK (pronouns IN ('he/him', 'she/her', 'they/them', 'any')) NULL,
        password TEXT NOT NULL
    );
    ''')
    # STREAKS table
    cur.execute('''
    CREATE TABLE IF NOT EXISTS STREAKS (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT NULL
    );
    ''')
    # USER_STREAKS table
    cur.execute('''
    CREATE TABLE IF NOT EXISTS USER_STREAKS (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        streak_id INTEGER NOT NULL,
        FOREIGN KEY (user_id) REFERENCES USERS(id),
        FOREIGN KEY (streak_id) REFERENCES STREAKS(id)
    );     
    ''')
    # PROFILE_SETTINGS table
    cur.execute('''
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
    cur.execute('''
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
