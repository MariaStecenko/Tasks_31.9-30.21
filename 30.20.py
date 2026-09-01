import sqlite3

def init_db(db_name="accounts.db"):
    with sqlite3.connect(db_name) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS accounts (
                name TEXT PRIMARY KEY,
                url TEXT,
                login TEXT,
                password TEXT
            )
        """)
        conn.commit()

def add_account(name, url, login, password, db_name="accounts.db"):
    with sqlite3.connect(db_name) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT OR REPLACE INTO accounts VALUES (?, ?, ?, ?)",
            (name, url, login, password)
        )
        conn.commit()

def get_account(name, db_name="accounts.db"):
    with sqlite3.connect(db_name) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT url, login, password FROM accounts WHERE name = ?", (name,))
        return cursor.fetchone()
