from app.services.llm_service import call_llm
import json


def is_followup(content: str, history: list) -> bool:
    """
    Detect if a message is a PURE clarification/explanation request 
    vs a research query that needs the full pipeline.
    
    Only returns True for simple clarifications like:
    - "explain that again"
    - "summarize the above" 
    - "clarify the third point"
    
    Returns False for anything that could benefit from new paper retrieval:
    - "compare transformers vs mamba" → needs new research
    - "what about quantum computing?" → needs new research
    - "how does attention work?" → needs new research
    - "tell me more about CNNs" → needs new research
    """
    if len(history) == 0:
        return False
    
    content_lower = content.lower().strip()
    words = content_lower.split()
    
    # Too long = probably a real research query
    if len(words) > 12:
        return False
    
    # Only these VERY specific patterns are true follow-ups
    # (pure clarification, not asking for new information)
    clarification_only = [
        "explain that again",
        "summarize again", 
        "summarize the above",
        "clarify",
        "what do you mean",
        "rephrase that",
        "say that again",
        "repeat that",
        "in simpler terms",
        "in simple words",
        "eli5",
        "too long didn't read",
        "tldr",
        "break it down",
    ]
    
    # Research-extending signals → should NOT be follow-ups
    research_signals = [
        "compare", "versus", "vs", "difference between",
        "what about", "how does", "how do", "how is", "how are",
        "why does", "why do", "why is",
        "tell me more", "more about", "expand on",
        "what is", "what are", "which", "who",
        "find", "search", "look up", "retrieve",
        "papers on", "research on", "studies on",
        "latest", "recent", "new", "current",
    ]
    
    # If it contains research signals → NOT a follow-up, run full pipeline
    if any(signal in content_lower for signal in research_signals):
        return False
    
    # Only match pure clarification patterns
    return any(signal in content_lower for signal in clarification_only)


def generate_followup_response(question: str, prior_research_data: dict) -> str:
    """Generate a conversational follow-up using prior research context"""
    
    summary = prior_research_data.get("summary", "")
    analysis = prior_research_data.get("analysis", "")
    gaps = prior_research_data.get("gaps", "")
    synthesis = prior_research_data.get("synthesis", "")
    
    papers_context = ""
    papers = prior_research_data.get("top_papers", [])
    if papers:
        papers_context = "\n".join([f"{p.get('title', '')}: {p.get('abstract', '')[:300]}" for p in papers])
    
    context = f"""
Summary: {summary}
Analysis: {analysis}
Gaps: {gaps}
Synthesis: {synthesis}

Papers:
{papers_context}
"""
    
    context = context[:3000]
    
    prompt = f"""Based on the following research context, answer the user's clarification request.
Keep the answer focused and use the existing research data — do not invent new papers or facts.

Research Context:
{context}

User Request: {question}

Provide a clear, focused answer in markdown format."""

    try:
        result = call_llm(prompt)
        return result.strip() if result else "I'm sorry, I couldn't generate a response based on the context."
    except Exception as e:
        print("⚠️ Follow-up error:", str(e))
        return "Sorry, there was an error generating a response."
