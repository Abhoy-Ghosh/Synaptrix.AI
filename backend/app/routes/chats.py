from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
import asyncio
import json

from app.storage.db import (
    get_chat,
    delete_chat,
    add_message,
    get_messages
)
from app.ai_engine.pipeline import run_pipeline
from app.agents.followup import is_followup, generate_followup_response

router = APIRouter(prefix="/api/chats", tags=["chats"])


class MessageCreate(BaseModel):
    content: str
    mode: Optional[str] = None


@router.get("/{chat_id}")
def get_chat_detail(chat_id: str):
    chat = get_chat(chat_id)
    if not chat:
        raise HTTPException(status_code=404, detail="Chat session not found")
    messages = get_messages(chat_id)
    return {
        "chat": chat,
        "messages": messages
    }


@router.delete("/{chat_id}")
def remove_chat(chat_id: str):
    chat = get_chat(chat_id)
    if not chat:
        raise HTTPException(status_code=404, detail="Chat session not found")
    delete_chat(chat_id)
    return {"message": "Chat session deleted"}


@router.post("/{chat_id}/messages")
async def send_chat_message(chat_id: str, data: MessageCreate):
    chat = get_chat(chat_id)
    if not chat:
        raise HTTPException(status_code=404, detail="Chat session not found")

    user_content = data.content.strip()
    if not user_content:
        raise HTTPException(status_code=400, detail="Message content cannot be empty")

    # 1. Save user message
    user_msg = add_message(chat_id, "user", user_content)

    # 2. Build context-aware prompt using prior history
    history = get_messages(chat_id)
    prior_messages = history[:-1]  # Exclude the message just added

    # 3. Check if this is a follow-up question
    if is_followup(user_content, prior_messages):
        # Find the last assistant message with research_data
        prior_research = None
        for msg in reversed(prior_messages):
            if msg["role"] == "assistant" and msg.get("research_data"):
                try:
                    prior_research = json.loads(msg["research_data"]) if isinstance(msg["research_data"], str) else msg["research_data"]
                except Exception:
                    pass
                break

        if prior_research:
            followup_text = generate_followup_response(user_content, prior_research)
            followup_result = {"followup": True, "content": followup_text}
            assistant_msg = add_message(chat_id, "assistant", followup_text, research_data=followup_result)
            return {
                "user_message": user_msg,
                "assistant_message": assistant_msg,
                "research": followup_result
            }

    # 4. Build context prompt for full pipeline
    context_prompt = user_content
    if prior_messages:
        # Build concise conversation history context
        history_summary = []
        for msg in prior_messages[-4:]:  # Include last 4 turns for context window efficiency
            role_label = "User" if msg["role"] == "user" else "Assistant"
            text_snippet = msg["content"][:200]
            history_summary.append(f"{role_label}: {text_snippet}")

        context_str = "\n".join(history_summary)
        context_prompt = f"Context from previous turns:\n{context_str}\n\nCurrent User Request:\n{user_content}"

    # 5. Run research pipeline
    effective_mode = data.mode or chat.get("mode") or "fast"
    try:
        pipeline_result = await asyncio.wait_for(
            run_pipeline(context_prompt, effective_mode),
            timeout=120
        )
    except asyncio.TimeoutError:
        pipeline_result = {"error": "Research execution timed out"}
    except Exception as e:
        pipeline_result = {"error": f"Pipeline failed: {str(e)}"}

    # 6. Extract assistant reply summary
    if "error" in pipeline_result:
        assistant_text = f"Unable to complete research request: {pipeline_result['error']}"
    else:
        assistant_text = (
            pipeline_result.get("synthesis") or 
            pipeline_result.get("summary") or 
            "Research intelligence generated."
        )

    # 7. Save assistant message with full research payload
    assistant_msg = add_message(chat_id, "assistant", assistant_text, research_data=pipeline_result)

    return {
        "user_message": user_msg,
        "assistant_message": assistant_msg,
        "research": pipeline_result
    }
