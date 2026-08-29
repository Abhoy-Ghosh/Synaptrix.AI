from fastapi import APIRouter
from app.storage.db import get_connection
import json

router = APIRouter()

@router.get("/api/dashboard/stats")
def get_dashboard_stats():
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) as c FROM projects")
    total_projects = cursor.fetchone()['c']
    
    cursor.execute("SELECT COUNT(*) as c FROM chats")
    total_chats = cursor.fetchone()['c']
    
    cursor.execute("SELECT COUNT(*) as c FROM messages")
    total_messages = cursor.fetchone()['c']
    
    # Mode distribution
    cursor.execute("SELECT mode, COUNT(*) as c FROM chats GROUP BY mode")
    mode_distribution = {row['mode']: row['c'] for row in cursor.fetchall()}
    
    # Activity Timeline (last 30 days)
    cursor.execute("""
        SELECT date(created_at, 'unixepoch') as d, COUNT(*) as c 
        FROM messages 
        WHERE created_at >= (strftime('%s', 'now') - 30 * 24 * 60 * 60)
        GROUP BY d
        ORDER BY d
    """)
    activity_timeline = [{"date": row['d'], "count": row['c']} for row in cursor.fetchall()]
    
    # Recent activity
    cursor.execute("""
        SELECT chat_id, role, content, created_at 
        FROM messages 
        ORDER BY created_at DESC 
        LIMIT 10
    """)
    recent_activity = []
    for row in cursor.fetchall():
        r = dict(row)
        r['snippet'] = r['content'][:100]
        del r['content']
        recent_activity.append(r)
        
    # Top topics
    cursor.execute("""
        SELECT topic, COUNT(*) as c 
        FROM projects 
        GROUP BY topic 
        ORDER BY c DESC
    """)
    top_topics = {row['topic']: row['c'] for row in cursor.fetchall()}
    
    # Total unique papers
    cursor.execute("SELECT research_data FROM messages WHERE research_data IS NOT NULL")
    unique_papers = set()
    for row in cursor.fetchall():
        try:
            data = json.loads(row['research_data'])
            if 'top_papers' in data:
                for paper in data['top_papers']:
                    if 'title' in paper:
                        unique_papers.add(paper['title'])
        except Exception:
            pass
            
    total_papers = len(unique_papers)
    
    conn.close()
    
    return {
        "total_projects": total_projects,
        "total_chats": total_chats,
        "total_messages": total_messages,
        "total_papers": total_papers,
        "mode_distribution": mode_distribution,
        "activity_timeline": activity_timeline,
        "recent_activity": recent_activity,
        "top_topics": top_topics
    }
