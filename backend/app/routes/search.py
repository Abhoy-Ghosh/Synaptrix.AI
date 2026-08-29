from fastapi import APIRouter
from app.storage.db import get_connection
import json

router = APIRouter()

@router.get("/api/search")
def global_search(q: str):
    conn = get_connection()
    cursor = conn.cursor()
    
    query = f"%{q}%"
    
    # Search projects
    cursor.execute("""
        SELECT id, name, topic, description, created_at 
        FROM projects 
        WHERE name LIKE ? COLLATE NOCASE OR topic LIKE ? COLLATE NOCASE
    """, (query, query))
    projects = [dict(row) for row in cursor.fetchall()]
    
    # Search chats
    cursor.execute("""
        SELECT id, project_id, title, created_at 
        FROM chats 
        WHERE title LIKE ? COLLATE NOCASE
    """, (query,))
    chats = [dict(row) for row in cursor.fetchall()]
    
    # Search messages
    cursor.execute("""
        SELECT id, chat_id, role, content, created_at 
        FROM messages 
        WHERE content LIKE ? COLLATE NOCASE
        LIMIT 20
    """, (query,))
    
    messages = []
    for row in cursor.fetchall():
        msg = dict(row)
        msg['snippet'] = msg['content'][:100] + ('...' if len(msg['content']) > 100 else '')
        # Delete content to not overload response
        del msg['content']
        messages.append(msg)
        
    conn.close()
    
    return {
        "projects": projects,
        "chats": chats,
        "messages": messages
    }
