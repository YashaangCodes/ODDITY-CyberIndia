from typing import Literal

from pydantic import BaseModel, Field


class URLRequest(BaseModel):
    url: str = Field(
        ...,
        min_length=1,
        max_length=8192,
    )


class URLResponse(BaseModel):
    input_type: Literal["url"]
    analysis_method: Literal["rule_based_baseline"]

    safety_score: int = Field(
        ...,
        ge=0,
        le=100,
    )

    risk_score: int = Field(
        ...,
        ge=0,
        le=100,
    )

    risk_level: Literal["low", "medium", "high"]

    threat_category: str
    reasons: list[str]
    recommendation: str