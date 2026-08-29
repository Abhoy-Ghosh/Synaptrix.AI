from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from app.storage.db import (
    create_project,
    get_projects,
    get_project,
    delete_project,
    create_chat,
    get_chats
)

router = APIRouter(prefix="/api/projects", tags=["projects"])


class ProjectCreate(BaseModel):
    name: str
    topic: str
    description: Optional[str] = ""


class ChatCreate(BaseModel):
    title: str
    mode: Optional[str] = "fast"


@router.get("")
def list_projects():
    return get_projects()


@router.post("")
def add_project(data: ProjectCreate):
    if not data.name.strip():
        raise HTTPException(status_code=400, detail="Project name is required")
    return create_project(data.name.strip(), data.topic.strip(), data.description or "")


@router.get("/{project_id}")
def get_project_detail(project_id: str):
    project = get_project(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


@router.delete("/{project_id}")
def remove_project(project_id: str):
    project = get_project(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    delete_project(project_id)
    return {"message": "Project deleted successfully"}


@router.get("/{project_id}/chats")
def list_project_chats(project_id: str):
    project = get_project(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return get_chats(project_id)


@router.post("/{project_id}/chats")
def add_chat(project_id: str, data: ChatCreate):
    project = get_project(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    if not data.title.strip():
        raise HTTPException(status_code=400, detail="Chat title is required")
    return create_chat(project_id, data.title.strip(), data.mode or "fast")
