from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from io import BytesIO

from app.services.pdf_service import build_pdf

router = APIRouter()


@router.post("/generate-pdf")
def generate_pdf(payload: dict):

    pdf_bytes = build_pdf(payload)

    return StreamingResponse(
        BytesIO(pdf_bytes),
        media_type="application/pdf",
        headers={
            "Content-Disposition": "attachment; filename=research_report.pdf"
        }
    )