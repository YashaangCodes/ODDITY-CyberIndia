from fastapi import APIRouter

from app.schemas.url import (
    URLRequest,
    URLResponse,
)
from app.services.url_analyzer import analyze_url

router = APIRouter(
    prefix="/api/v1/analyze",
    tags=["URL Analysis"],
)

@router.post(
    "/url",
    response_model=URLResponse,
)
def analyze_url_endpoint(
    request: URLRequest,
) -> URLResponse:
    return analyze_url(request.url)