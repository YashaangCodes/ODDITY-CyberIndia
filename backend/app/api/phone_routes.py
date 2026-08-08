from fastapi import APIRouter

from app.schemas.phone import (
    PhoneAnalysisRequest,
    PhoneAnalysisResponse,
)
from app.services.phone_analyzer import analyze_phone


router = APIRouter(
    prefix="/api/v1/analyze",
    tags=["Phone Analysis"],
)


@router.post(
    "/phone",
    response_model=PhoneAnalysisResponse,
)
def analyze_phone_endpoint(
    request: PhoneAnalysisRequest,
) -> PhoneAnalysisResponse:
    result = analyze_phone(request.phone_number)
    return result

