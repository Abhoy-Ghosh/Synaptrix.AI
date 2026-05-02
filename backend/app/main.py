from fastapi import FastAPI
from pydantic import BaseModel
from app.ai_engine.pipeline import run_pipeline

app = FastAPI()

class Query(BaseModel):
    topic: str

@app.post("/generate")
def generate(query: Query):
    print("🔥 NEW CODE RUNNING")
    return run_pipeline(query.topic)
