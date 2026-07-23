from typing import Literal

from pydantic import BaseModel, Field


class MessageAnalysisRequest(BaseModel):
    text: str = Field(
        min_length=3,
        max_length=5000,
        description="The suspicious SMS, WhatsApp message, or email text.",
        examples=[
            "Complete your KYC immediately or your bank account will be blocked."
        ],
    )


class MessageAnalysisResponse(BaseModel):
    input_type: Literal["message"]
    analysis_method: Literal["rule_based_baseline"]

    safety_score: int
    risk_score: int
    risk_level: Literal["low", "medium", "high"]

    threat_category: str
    reasons: list[str]
    recommendation: str

