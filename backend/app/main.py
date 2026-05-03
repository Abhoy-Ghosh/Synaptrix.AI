from fastapi import FastAPI
from pydantic import BaseModel

from app.ai_engine.pipeline import run_pipeline
from app.feedback.feedback_store import add_feedback

app = FastAPI()


# -----------------------------
# REQUEST MODELS
# -----------------------------
class Query(BaseModel):
    topic: str


class Feedback(BaseModel):
    topic: str
    feedback: str  # "good" or "bad"


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
# FEEDBACK ENDPOINT
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