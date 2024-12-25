import sqlite3
import json
from datetime import datetime
import os
import shutil
import threading
from typing import List, Dict, Optional

class DatabaseManager:
    """
    Manages SQLite database operations for tasks and messages with enhanced features.
    """
    
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls, db_path="agency_data.db"):
        """Implement singleton pattern for connection pooling."""
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super(DatabaseManager, cls).__new__(cls)
        return cls._instance
    
    def __init__(self, db_path="agency_data.db"):
        """Initialize database connection and create tables if they don't exist."""
        if not hasattr(self, 'initialized'):
            self.db_path = db_path
            self.connection_pool = {}
            self._create_tables()
            self.initialized = True
    
    def _get_connection(self):
        """Get a thread-specific database connection."""
        thread_id = threading.get_ident()
        if thread_id not in self.connection_pool:
            self.connection_pool[thread_id] = sqlite3.connect(self.db_path)
            # Enable foreign keys
            self.connection_pool[thread_id].execute("PRAGMA foreign_keys = ON")
        return self.connection_pool[thread_id]
    
    def _create_tables(self):
        """Create necessary tables if they don't exist."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            # Create tasks table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS tasks (
                    id TEXT PRIMARY KEY,
                    title TEXT NOT NULL,
                    description TEXT,
                    priority INTEGER NOT NULL,
                    agent TEXT NOT NULL,
                    status TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL,
                    dependencies TEXT,
                    parent_task_id TEXT,
                    FOREIGN KEY(parent_task_id) REFERENCES tasks(id)
                )
            """)
            
            # Create task_history table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS task_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    task_id TEXT NOT NULL,
                    field_name TEXT NOT NULL,
                    old_value TEXT,
                    new_value TEXT,
                    changed_at TEXT NOT NULL,
                    changed_by TEXT NOT NULL,
                    FOREIGN KEY(task_id) REFERENCES tasks(id)
                )
            """)
            
            # Create messages table with threading support
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS messages (
                    id TEXT PRIMARY KEY,
                    from_agent TEXT NOT NULL,
                    to_agent TEXT NOT NULL,
                    content TEXT NOT NULL,
                    priority TEXT NOT NULL,
                    type TEXT NOT NULL,
                    status TEXT NOT NULL,
                    timestamp TEXT NOT NULL,
                    thread_id TEXT,
                    reply_to_id TEXT,
                    FOREIGN KEY(reply_to_id) REFERENCES messages(id)
                )
            """)
            
            # Create task_stats table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS task_stats (
                    agent TEXT PRIMARY KEY,
                    tasks_completed INTEGER DEFAULT 0,
                    tasks_pending INTEGER DEFAULT 0,
                    avg_completion_time REAL DEFAULT 0,
                    last_updated TEXT NOT NULL
                )
            """)
            
            conn.commit()
    
    def backup_database(self, backup_dir="backups"):
        """Create a backup of the database."""
        try:
            os.makedirs(backup_dir, exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_path = os.path.join(backup_dir, f"agency_data_backup_{timestamp}.db")
            
            # Create a new backup
            shutil.copy2(self.db_path, backup_path)
            
            # Keep only the last 5 backups
            backups = sorted([f for f in os.listdir(backup_dir) if f.endswith('.db')])
            for old_backup in backups[:-5]:
                os.remove(os.path.join(backup_dir, old_backup))
            
            return f"Backup created successfully at {backup_path}"
        except Exception as e:
            return f"Backup failed: {str(e)}"
    
    def restore_database(self, backup_path):
        """Restore the database from a backup."""
        try:
            if not os.path.exists(backup_path):
                return "Backup file not found"
            
            # Close all connections
            for conn in self.connection_pool.values():
                conn.close()
            self.connection_pool.clear()
            
            # Restore the backup
            shutil.copy2(backup_path, self.db_path)
            return "Database restored successfully"
        except Exception as e:
            return f"Restore failed: {str(e)}"
    
    def add_task(self, task_data):
        """Add a new task to the database with history tracking."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            try:
                # Insert task
                cursor.execute("""
                    INSERT INTO tasks (id, title, description, priority, agent, status, created_at, updated_at, dependencies, parent_task_id)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    task_data["id"],
                    task_data["title"],
                    task_data["description"],
                    task_data["priority"],
                    task_data["agent"],
                    task_data["status"],
                    task_data["created_at"],
                    task_data["updated_at"],
                    json.dumps(task_data.get("dependencies", [])),
                    task_data.get("parent_task_id")
                ))
                
                # Update task stats
                cursor.execute("""
                    INSERT OR REPLACE INTO task_stats (agent, tasks_pending, last_updated)
                    VALUES (?, 
                        COALESCE((SELECT tasks_pending + 1 FROM task_stats WHERE agent = ?), 1),
                        ?)
                """, (task_data["agent"], task_data["agent"], datetime.now().isoformat()))
                
                conn.commit()
                return task_data
            except Exception as e:
                conn.rollback()
                raise e
    
    def update_task(self, task_id, updates, changed_by="system"):
        """Update an existing task with history tracking."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            try:
                # Get current task data
                cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
                task = cursor.fetchone()
                if not task:
                    return None
                
                # Track changes in history
                current_time = datetime.now().isoformat()
                for key, new_value in updates.items():
                    if key in ["title", "description", "priority", "agent", "status", "dependencies"]:
                        old_value = task[{
                            "title": 1,
                            "description": 2,
                            "priority": 3,
                            "agent": 4,
                            "status": 5,
                            "dependencies": 8
                        }[key]]
                        
                        if key == "dependencies":
                            old_value = old_value if old_value else "[]"
                            new_value = json.dumps(new_value)
                        
                        if str(old_value) != str(new_value):
                            cursor.execute("""
                                INSERT INTO task_history (task_id, field_name, old_value, new_value, changed_at, changed_by)
                                VALUES (?, ?, ?, ?, ?, ?)
                            """, (task_id, key, str(old_value), str(new_value), current_time, changed_by))
                
                # Prepare update query
                update_fields = []
                update_values = []
                for key, value in updates.items():
                    if key in ["title", "description", "priority", "agent", "status", "dependencies"]:
                        update_fields.append(f"{key} = ?")
                        update_values.append(value if key != "dependencies" else json.dumps(value))
                
                # Add updated_at timestamp
                update_fields.append("updated_at = ?")
                update_values.append(current_time)
                
                # Add task_id for WHERE clause
                update_values.append(task_id)
                
                # Execute update
                query = f"UPDATE tasks SET {', '.join(update_fields)} WHERE id = ?"
                cursor.execute(query, update_values)
                
                # Update task stats if status changed
                if "status" in updates and updates["status"] == "completed":
                    # Get the agent for this task
                    agent = task[4]  # agent is at index 4 in the tasks table
                    
                    # Update task stats
                    cursor.execute("""
                        INSERT OR REPLACE INTO task_stats 
                        (agent, tasks_completed, tasks_pending, avg_completion_time, last_updated)
                        VALUES (
                            ?,
                            COALESCE((SELECT tasks_completed + 1 FROM task_stats WHERE agent = ?), 1),
                            COALESCE((SELECT tasks_pending - 1 FROM task_stats WHERE agent = ?), 0),
                            COALESCE(
                                (
                                    SELECT AVG(
                                        CAST(
                                            (JULIANDAY(th.changed_at) - JULIANDAY(t.created_at)) * 24 * 60 
                                            AS REAL
                                        )
                                    )
                                    FROM tasks t
                                    JOIN task_history th ON t.id = th.task_id
                                    WHERE t.agent = ?
                                    AND th.field_name = 'status'
                                    AND th.new_value = 'completed'
                                ),
                                0
                            ),
                            ?
                        )
                    """, (agent, agent, agent, agent, current_time))
                
                conn.commit()
                
                # Return updated task
                cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
                updated = cursor.fetchone()
                return {
                    "id": updated[0],
                    "title": updated[1],
                    "description": updated[2],
                    "priority": updated[3],
                    "agent": updated[4],
                    "status": updated[5],
                    "created_at": updated[6],
                    "updated_at": updated[7],
                    "dependencies": json.loads(updated[8]),
                    "parent_task_id": updated[9]
                }
            except Exception as e:
                conn.rollback()
                raise e
    
    def get_task_history(self, task_id) -> List[Dict]:
        """Get the history of changes for a task."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT field_name, old_value, new_value, changed_at, changed_by
                FROM task_history
                WHERE task_id = ?
                ORDER BY changed_at DESC
            """, (task_id,))
            
            history = []
            for row in cursor.fetchall():
                history.append({
                    "field": row[0],
                    "old_value": row[1],
                    "new_value": row[2],
                    "changed_at": row[3],
                    "changed_by": row[4]
                })
            
            return history
    
    def get_agent_stats(self, agent) -> Optional[Dict]:
        """Get task statistics for an agent."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT tasks_completed, tasks_pending, avg_completion_time, last_updated
                FROM task_stats
                WHERE agent = ?
            """, (agent,))
            
            row = cursor.fetchone()
            if row:
                return {
                    "tasks_completed": row[0],
                    "tasks_pending": row[1],
                    "avg_completion_time": row[2],  # in minutes
                    "last_updated": row[3]
                }
            return None
    
    def add_message(self, message_data):
        """Add a new message to the database with threading support."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO messages (
                    id, from_agent, to_agent, content, priority, type, status, timestamp,
                    thread_id, reply_to_id
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                message_data["id"],
                message_data["from_agent"],
                message_data["to_agent"],
                message_data["content"],
                message_data["priority"],
                message_data["type"],
                message_data["status"],
                message_data["timestamp"],
                message_data.get("thread_id", message_data["id"]),  # Use message ID as thread ID if not provided
                message_data.get("reply_to_id")
            ))
            conn.commit()
        return message_data
    
    def get_message_thread(self, thread_id) -> List[Dict]:
        """Get all messages in a thread."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                WITH RECURSIVE thread_messages AS (
                    SELECT id, from_agent, to_agent, content, priority, type, status, timestamp, thread_id, reply_to_id, 0 as depth
                    FROM messages
                    WHERE thread_id = ?
                    UNION ALL
                    SELECT m.id, m.from_agent, m.to_agent, m.content, m.priority, m.type, m.status, m.timestamp, m.thread_id, m.reply_to_id, tm.depth + 1
                    FROM messages m
                    JOIN thread_messages tm ON m.reply_to_id = tm.id
                )
                SELECT * FROM thread_messages
                ORDER BY timestamp ASC
            """, (thread_id,))
            
            messages = []
            for row in cursor.fetchall():
                messages.append({
                    "id": row[0],
                    "from_agent": row[1],
                    "to_agent": row[2],
                    "content": row[3],
                    "priority": row[4],
                    "type": row[5],
                    "status": row[6],
                    "timestamp": row[7],
                    "thread_id": row[8],
                    "reply_to_id": row[9],
                    "depth": row[10]
                })
            
            return messages
    
    def cleanup(self):
        """Clean up database connections."""
        for conn in self.connection_pool.values():
            conn.close()
        self.connection_pool.clear()

if __name__ == "__main__":
    # Test the enhanced database manager
    db = DatabaseManager("test_agency.db")
    
    try:
        # Test task management with history
        task = {
            "id": "task_1",
            "title": "Test Task",
            "description": "This is a test task",
            "priority": 1,
            "agent": "TestAgent",
            "status": "pending",
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            "dependencies": []
        }
        print("\nAdding task:", db.add_task(task))
        
        # Update task and check history
        print("\nUpdating task:", db.update_task("task_1", {"status": "completed"}, "test_user"))
        print("\nTask history:", db.get_task_history("task_1"))
        
        # Check agent stats
        print("\nAgent stats:", db.get_agent_stats("TestAgent"))
        
        # Test message threading
        message1 = {
            "id": "msg_1",
            "from_agent": "AgentA",
            "to_agent": "AgentB",
            "content": "Initial message",
            "priority": "high",
            "type": "task",
            "status": "sent",
            "timestamp": datetime.now().isoformat()
        }
        print("\nAdding message:", db.add_message(message1))
        
        # Add reply
        message2 = {
            "id": "msg_2",
            "from_agent": "AgentB",
            "to_agent": "AgentA",
            "content": "Reply to initial message",
            "priority": "high",
            "type": "task",
            "status": "sent",
            "timestamp": datetime.now().isoformat(),
            "thread_id": "msg_1",
            "reply_to_id": "msg_1"
        }
        print("\nAdding reply:", db.add_message(message2))
        
        # Get message thread
        print("\nMessage thread:", db.get_message_thread("msg_1"))
        
        # Test backup and restore
        print("\nCreating backup:", db.backup_database())
        
    finally:
        # Clean up
        db.cleanup()
        os.remove("test_agency.db") 