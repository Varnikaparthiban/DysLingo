import sqlite3
from flask import current_app, g

def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(current_app.config["DATABASE"])
        g.db.row_factory = sqlite3.Row
    return g.db

def init_db():
    from flask import Flask
    # Use a direct connection so initialization works before a request context.
    import os
    from config import Config
    os.makedirs(os.path.dirname(Config.DATABASE), exist_ok=True)
    connection = sqlite3.connect(Config.DATABASE)
    connection.execute("""
        CREATE TABLE IF NOT EXISTS sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            language TEXT NOT NULL DEFAULT 'en-US',
            target_text TEXT NOT NULL,
            spoken_text TEXT NOT NULL,
            accuracy REAL NOT NULL DEFAULT 0,
            wpm REAL NOT NULL DEFAULT 0,
            errors INTEGER NOT NULL DEFAULT 0,
            pauses INTEGER NOT NULL DEFAULT 0,
            duration_seconds REAL NOT NULL DEFAULT 0
        )
    """)
    connection.commit()
    connection.close()

def close_db(exception=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()
