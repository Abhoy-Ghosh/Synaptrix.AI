from fastapi import FastAPI
from pydantic import BaseModel
from app.ai_engine.pipeline import run_pipeline

app = FastAPI()

class Query(BaseModel):
    topic: str

@app.get("/")
def root():
    return {"status": "running"}

@app.post("/generate")
def generate(query: Query):
    print("🔥 PIPELINE RUNNING")
    return run_pipeline(query.topic)