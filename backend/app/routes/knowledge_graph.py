from fastapi import APIRouter
from app.storage.db import get_connection
import json
import hashlib

router = APIRouter()

@router.get("/api/knowledge-graph")
def get_knowledge_graph():
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT m.research_data, p.topic 
        FROM messages m
        JOIN chats c ON m.chat_id = c.id
        JOIN projects p ON c.project_id = p.id
        WHERE m.research_data IS NOT NULL
    """)
    
    rows = cursor.fetchall()
    conn.close()
    
    nodes_dict = {}
    edges = []
    topics_dict = {}
    
    for row in rows:
        topic = row['topic']
        if topic not in topics_dict:
            topic_id = hashlib.md5(topic.encode()).hexdigest()
            topics_dict[topic] = topic_id
            nodes_dict[topic_id] = {
                "id": topic_id,
                "label": topic,
                "type": "topic",
                "group": topic
            }
            
        try:
            data = json.loads(row['research_data'])
        except Exception:
            continue
            
        papers = data.get('top_papers', [])
        paper_id_map = {}
        for paper in papers:
            title = paper.get('title', 'Unknown Title')
            paper_id = hashlib.md5(title.encode()).hexdigest()
            paper_id_map[title] = paper_id
            
            if paper_id not in nodes_dict:
                nodes_dict[paper_id] = {
                    "id": paper_id,
                    "label": title,
                    "type": "paper",
                    "citations": paper.get('citations', 0),
                    "group": topic,
                    "abstract_snippet": paper.get('abstract', '')[:100]
                }
            
            edges.append({
                "source": topics_dict[topic],
                "target": paper_id,
                "weight": 1.0
            })
            
        similarities = data.get('similarities', [])
        for sim in similarities:
            p1 = sim.get('paper_1')
            p2 = sim.get('paper_2')
            score = sim.get('score', 0)
            if p1 in paper_id_map and p2 in paper_id_map:
                edges.append({
                    "source": paper_id_map[p1],
                    "target": paper_id_map[p2],
                    "weight": score
                })
                
    return {
        "nodes": list(nodes_dict.values()),
        "edges": edges
    }
