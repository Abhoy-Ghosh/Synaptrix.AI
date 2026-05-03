from fastapi import FastAPI
from pydantic import BaseModel

from app.ai_engine.pipeline import run_pipeline
from app.feedback.feedback_store import add_feedback
from app.feedback.paper_feedback import add_paper_feedback  # ✅ NEW

app = FastAPI()


# -----------------------------
# REQUEST MODELS
# -----------------------------
class Query(BaseModel):
    topic: str


class Feedback(BaseModel):
    topic: str
    feedback: str  # "good" or "bad"


class PaperFeedback(BaseModel):   # ✅ NEW
    title: str
    score: int  # +1 or -1


# -----------------------------
# ROOT CHECK
# -----------------------------
@app.get("/")
def root():
    return {"status": "running"}


# -----------------------------
# MAIN PIPELINE
# -----------------------------
@app.post("/generate")
def generate(query: Query):
    print("🔥 PIPELINE RUNNING")
    return run_pipeline(query.topic)


# -----------------------------
# TOPIC FEEDBACK
# -----------------------------
@app.post("/feedback")
def submit_feedback(data: Feedback):
    if data.feedback not in ["good", "bad"]:
        return {"error": "feedback must be 'good' or 'bad'"}

    add_feedback(data.topic, data.feedback)

    return {
        "message": "Feedback saved",
        "topic": data.topic,
        "feedback": data.feedback
    }


# -----------------------------
# PAPER-LEVEL FEEDBACK (🔥 IMPORTANT)
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