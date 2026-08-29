import sys
import os
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from fastapi import FastAPI
from pydantic import BaseModel
from typing import Literal
from contextlib import asynccontextmanager
import asyncio

from app.ai_engine.pipeline import run_pipeline
from app.services.model_loader import warmup_model
from app.feedback.feedback_store import add_feedback
from app.feedback.paper_feedback import add_paper_feedback

from fastapi.middleware.cors import CORSMiddleware

from app.routes.pdf import router as pdf_router

from app.storage.db import init_db
from app.routes.projects import router as projects_router
from app.routes.chats import router as chats_router
from app.routes.search import router as search_router
from app.routes.dashboard import router as dashboard_router
from app.routes.knowledge_graph import router as kg_router

# -----------------------------
# STARTUP
# -----------------------------


@asynccontextmanager
async def lifespan(app: FastAPI):

    print("[*] Starting Synaptrix AI...")

    init_db()
    print("[+] Database initialized")

    warmup_model()

    print("[+] Warmup complete")

    yield

    print("[-] Shutting down...")


app = FastAPI(lifespan=lifespan)

# CORS — allow Vercel production frontend, previews, localhost, and all headers/methods
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://synaptrix-ai.vercel.app",
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:8001",
        "http://127.0.0.1:8001",
    ],
    allow_origin_regex=r"https?://.*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

# -----------------------------
# ROUTES
# -----------------------------
app.include_router(pdf_router)
app.include_router(projects_router)
app.include_router(chats_router)
app.include_router(search_router)
app.include_router(dashboard_router)
app.include_router(kg_router)

# -----------------------------
# REQUEST MODELS
# -----------------------------
class Query(BaseModel):
    topic: str
    mode: Literal["fast", "parallel", "research"] | None = None


class Feedback(BaseModel):
    topic: str
    feedback: Literal["good", "bad"]


class PaperFeedback(BaseModel):
    title: str
    score: int


# -----------------------------
# ROOT
# -----------------------------
@app.get("/")
def root():
    return {"status": "running"}


# -----------------------------
# MAIN PIPELINE
# -----------------------------
@app.post("/generate")
async def generate(query: Query):
    print("🔥 PIPELINE RUNNING")

    if not query.topic or len(query.topic.strip()) < 3:
        return {"error": "Invalid topic"}

    try:
        result = await asyncio.wait_for(
            run_pipeline(query.topic, query.mode),
            timeout=60
        )
        return result

    except asyncio.TimeoutError:
        return {"error": "Request timed out"}

    except Exception as e:
        print("❌ Pipeline error:", str(e))
        return {"error": "Pipeline failed"}


# -----------------------------
# TOPIC FEEDBACK
# -----------------------------
@app.post("/feedback")
def submit_feedback(data: Feedback):
    add_feedback(data.topic, data.feedback)

    return {
        "message": "Feedback saved",
        "topic": data.topic,
        "feedback": data.feedback
    }


# -----------------------------
# PAPER FEEDBACK
# -----------------------------
@app.post("/paper-feedback")
def submit_paper_feedback(data: PaperFeedback):
    if data.score not in [1, -1]:
        return {"error": "score must be +1 or -1"}

    add_paper_feedback(data.title, data.score)

    return {
        "message": "Paper feedback stored",
        "title": data.title,
        "score": data.score
    }