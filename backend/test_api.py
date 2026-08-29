import pytest
from fastapi.testclient import TestClient
import os

from app.main import app
import app.storage.db as db_module

client = TestClient(app)


@pytest.fixture(autouse=True)
def setup_test_db(tmp_path, monkeypatch):
    test_db_dir = str(tmp_path)
    monkeypatch.setenv("DATA_DIR", test_db_dir)
    db_module.BASE_DIR = test_db_dir
    db_module.DB_PATH = os.path.join(test_db_dir, "synaptrix.db")
    db_module.init_db()


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "running"}


def test_projects_crud():
    # Create project
    res = client.post("/api/projects", json={
        "name": "Test Project",
        "topic": "Machine Learning",
        "description": "A test project"
    })
    assert res.status_code == 200
    project = res.json()
    assert project["name"] == "Test Project"
    project_id = project["id"]

    # Get project
    res = client.get(f"/api/projects/{project_id}")
    assert res.status_code == 200

    # List projects
    res = client.get("/api/projects")
    assert res.status_code == 200
    assert len(res.json()) >= 1

    # Create chat
    res = client.post(f"/api/projects/{project_id}/chats", json={
        "title": "ML Synthesis Chat",
        "mode": "fast"
    })
    assert res.status_code == 200
    chat = res.json()
    chat_id = chat["id"]

    # List chats
    res = client.get(f"/api/projects/{project_id}/chats")
    assert res.status_code == 200
    assert len(res.json()) == 1

    # Get chat detail
    res = client.get(f"/api/chats/{chat_id}")
    assert res.status_code == 200
    assert res.json()["chat"]["title"] == "ML Synthesis Chat"

    # Delete chat
    res = client.delete(f"/api/chats/{chat_id}")
    assert res.status_code == 200

    # Delete project
    res = client.delete(f"/api/projects/{project_id}")
    assert res.status_code == 200


def test_dashboard_and_search():
    res = client.get("/api/dashboard/stats")
    assert res.status_code == 200
    stats = res.json()
    assert "total_projects" in stats
    assert "total_chats" in stats

    res = client.get("/api/search?q=test")
    assert res.status_code == 200
    search_data = res.json()
    assert "projects" in search_data
    assert "chats" in search_data
    assert "messages" in search_data


def test_knowledge_graph():
    res = client.get("/api/knowledge-graph")
    assert res.status_code == 200
    kg = res.json()
    assert "nodes" in kg
    assert "edges" in kg


def test_feedback_endpoints():
    res = client.post("/feedback", json={"topic": "quantum", "feedback": "good"})
    assert res.status_code == 200

    res = client.post("/paper-feedback", json={"title": "Test Paper", "score": 1})
    assert res.status_code == 200
