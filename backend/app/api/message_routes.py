from fastapi import APIRouter

from app.schemas.message import (
    MessageAnalysisRequest,
    MessageAnalysisResponse,
)
from app.services.message_analyzer import analyze_message_text


router = APIRouter(
    prefix="/api/v1/analyze",
    tags=["Message Analysis"],
)


@router.post(
    "/message",
    response_model=MessageAnalysisResponse,
)
def analyze_message(
    request: MessageAnalysisRequest,
) -> MessageAnalysisResponse:
    result = analyze_message_text(request.text)
    return MessageAnalysisResponse(**result)