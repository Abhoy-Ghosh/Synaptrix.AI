import sqlite3
import json
import os
import time
import uuid

BASE_DIR = os.environ.get("DATA_DIR", os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DB_PATH = os.path.join(BASE_DIR, "synaptrix.db")


def get_connection():
    os.makedirs(BASE_DIR, exist_ok=True)
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    # Projects Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS projects (
        id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        topic TEXT NOT NULL,
        description TEXT DEFAULT '',
        created_at REAL NOT NULL,
        updated_at REAL NOT NULL
    );
    """)

    # Chats Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS chats (
        id TEXT PRIMARY KEY,
        project_id TEXT NOT NULL,
        title TEXT NOT NULL,
        mode TEXT DEFAULT 'fast',
        created_at REAL NOT NULL,
        updated_at REAL NOT NULL,
        FOREIGN KEY (project_id) REFERENCES projects (id) ON DELETE CASCADE
    );
    """)

    # Messages Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS messages (
        id TEXT PRIMARY KEY,
        chat_id TEXT NOT NULL,
        role TEXT NOT NULL,
        content TEXT NOT NULL,
        research_data TEXT DEFAULT NULL,
        created_at REAL NOT NULL,
        FOREIGN KEY (chat_id) REFERENCES chats (id) ON DELETE CASCADE
    );
    """)

    conn.commit()
    conn.close()


# -----------------------------
# PROJECTS CRUD
# -----------------------------

def create_project(name: str, topic: str, description: str = ""):
    project_id = str(uuid.uuid4())
    now = time.time()
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO projects (id, name, topic, description, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?)",
        (project_id, name, topic, description, now, now)
    )
    conn.commit()
    conn.close()
    return get_project(project_id)


def get_projects():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT p.*, COUNT(c.id) as chat_count 
        FROM projects p 
        LEFT JOIN chats c ON p.id = c.project_id 
        GROUP BY p.id 
        ORDER BY p.updated_at DESC
    """)
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]


def get_project(project_id: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM projects WHERE id = ?", (project_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None


def delete_project(project_id: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM projects WHERE id = ?", (project_id,))
    conn.commit()
    conn.close()
    return True


# -----------------------------
# CHATS CRUD
# -----------------------------

def create_chat(project_id: str, title: str, mode: str = "fast"):
    chat_id = str(uuid.uuid4())
    now = time.time()
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO chats (id, project_id, title, mode, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?)",
        (chat_id, project_id, title, mode, now, now)
    )
    # Update project updated_at
    cursor.execute("UPDATE projects SET updated_at = ? WHERE id = ?", (now, project_id))
    conn.commit()
    conn.close()
    return get_chat(chat_id)


def get_chats(project_id: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM chats WHERE project_id = ? ORDER BY updated_at DESC", (project_id,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]


def get_chat(chat_id: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM chats WHERE id = ?", (chat_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None


def delete_chat(chat_id: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM chats WHERE id = ?", (chat_id,))
    conn.commit()
    conn.close()
    return True


# -----------------------------
# MESSAGES CRUD
# -----------------------------

def add_message(chat_id: str, role: str, content: str, research_data: dict = None):
    msg_id = str(uuid.uuid4())
    now = time.time()
    research_json = json.dumps(research_data) if research_data is not None else None

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO messages (id, chat_id, role, content, research_data, created_at) VALUES (?, ?, ?, ?, ?, ?)",
        (msg_id, chat_id, role, content, research_json, now)
    )
    # Touch chat and parent project updated_at timestamp
    cursor.execute("UPDATE chats SET updated_at = ? WHERE id = ?", (now, chat_id))
    cursor.execute("""
        UPDATE projects SET updated_at = ? 
        WHERE id = (SELECT project_id FROM chats WHERE id = ?)
    """, (now, chat_id))

    conn.commit()
    conn.close()

    return {
        "id": msg_id,
        "chat_id": chat_id,
        "role": role,
        "content": content,
        "research_data": research_data,
        "created_at": now
    }


def get_messages(chat_id: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM messages WHERE chat_id = ? ORDER BY created_at ASC", (chat_id,))
    rows = cursor.fetchall()
    conn.close()

    result = []
    for row in rows:
        item = dict(row)
        if item["research_data"]:
            try:
                item["research_data"] = json.loads(item["research_data"])
            except Exception:
                pass
        result.append(item)
    return result
