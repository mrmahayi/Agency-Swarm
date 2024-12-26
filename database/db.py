import sqlite3
from pathlib import Path

class DatabaseManager:
    def __init__(self):
        self.db_path = Path("data/agency.db")
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()
    
    def _init_db(self):
        """Initialize database tables"""
        with self.get_connection() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY,
                    description TEXT,
                    status TEXT,
                    agent TEXT,
                    priority INTEGER,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS messages (
                    id INTEGER PRIMARY KEY,
                    content TEXT,
                    from_agent TEXT,
                    to_agent TEXT,
                    thread_id TEXT,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
    
    def get_connection(self):
        """Get a database connection"""
        return sqlite3.connect(self.db_path)

db = DatabaseManager() 