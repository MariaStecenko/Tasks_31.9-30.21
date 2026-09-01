import sqlite3

def init_db(db_name="glossary.db"):
    with sqlite3.connect(db_name) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS terms (
                term TEXT PRIMARY KEY,
                definition TEXT
            )
        """)
        conn.commit()

def add_term(term, definition, db_name="glossary.db"):
    with sqlite3.connect(db_name) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT OR REPLACE INTO terms VALUES (?, ?)",
            (term, definition)
        )
        conn.commit()

def get_definition(term, db_name="glossary.db"):
    with sqlite3.connect(db_name) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT definition FROM terms WHERE term = ?", (term,))
        row = cursor.fetchone()
        return row[0] if row else None
