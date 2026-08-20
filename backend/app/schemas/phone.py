from typing import Literal

from pydantic import BaseModel, Field


class PhoneAnalysisRequest(BaseModel):
    phone_number: str = Field(
        min_length=3,
        max_length=25,
        description="Phone number to analyze.",
        examples=["9876543210", "+919876543210"],
    )

class PhoneReputationEvidence(BaseModel):
    classification: str
    category: str
    report_count: int
    source_count: int
    confidence: str
    conflicting_evidence: bool

class PhoneAnalysisResponse(BaseModel):
    input_type: Literal["phone"]
    analysis_method: Literal["rule_based_baseline"]

    country: str | None
    number_type: str | None

    safety_score: int | None
    risk_score: int | None
    risk_level: Literal["low", "medium", "high", "not_applicable"]

    threat_category: str
    reasons: list[str]
    recommendation: str

    reputation_evidence: PhoneReputationEvidence | None = None