from typing import Literal

from pydantic import BaseModel


class URLRequest(BaseModel):
    url: str


class URLResponse(BaseModel):
    input_type: Literal["url"]
    analysis_method: Literal["rule_based_baseline"]

    safety_score: int
    risk_score: int
    risk_level: Literal["low", "medium", "high"]

    threat_category: str
    reasons: list[str]
    recommendation: str