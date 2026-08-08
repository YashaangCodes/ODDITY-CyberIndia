from app.schemas.phone import PhoneAnalysisResponse

from app.utils.phone_utils import (
    normalize_phone_number,
    is_valid_phone_number,
    get_phone_country,
    get_phone_number_type,
    is_indian_service_number,
)

def analyze_phone(phone_number: str) -> PhoneAnalysisResponse:
    risk_score: int = 0
    reasons: list[str] = []

    # Handle Indian emergency/service numbers first
    if is_indian_service_number(phone_number):
        return PhoneAnalysisResponse(
            input_type="phone",
            analysis_method="rule_based_baseline",
            country="IN",
            number_type="indian_service_number",
            safety_score=100,
            risk_score=0,
            risk_level="low",
            threat_category="service_number",
            reasons=[
                "The number is recognized as an Indian emergency or service number."
            ],
            recommendation=(
                "This is a recognized service number. Verify the purpose of the "
                "call before sharing any personal or financial information."
            ),
        )

    try:
        parsed_number = normalize_phone_number(phone_number)
    except ValueError:
        return PhoneAnalysisResponse(
            input_type="phone",
            analysis_method="rule_based_baseline",
            country=None,
            number_type=None,
            safety_score=None,
            risk_score=None,
            risk_level="not_applicable",
            threat_category="invalid_phone_number",
            reasons=[
                "The provided input could not be interpreted as a valid phone number."
            ],
            recommendation=(
                "The input does not appear to be a valid phone number. "
                "Please check the number and try again."
            ),
        )

    if not is_valid_phone_number(parsed_number):
        risk_score += 40
        reasons.append(
            "The phone number does not appear to be a valid number for its region."
        )

    country = get_phone_country(parsed_number)
    number_type = get_phone_number_type(parsed_number)

    if not reasons:
        reasons.append(
            "No suspicious indicators were detected by the baseline phone-number rules."
        )

    risk_score = min(risk_score, 100)
    safety_score = 100 - risk_score

    if risk_score >= 70:
        risk_level = "high"
    elif risk_score >= 35:
        risk_level = "medium"
    else:
        risk_level = "low"

    if risk_score >= 70:
        threat_category = "suspicious_phone_number"
        recommendation = (
            "Avoid sharing OTPs, PINs, passwords, banking information, or "
            "making payments until the number is independently verified."
        )
    elif risk_score >= 35:
        threat_category = "potentially_invalid_phone_number"
        recommendation = (
            "Treat this number cautiously and verify it through an independent "
            "source before sharing sensitive information."
        )
    else:
        threat_category = "no_clear_threat_detected"
        recommendation = (
            "No strong suspicious indicators were detected, but do not share "
            "sensitive information unless you trust the caller."
        )

    return PhoneAnalysisResponse(
        input_type="phone",
        analysis_method="rule_based_baseline",
        country=country,
        number_type=number_type,
        safety_score=safety_score,
        risk_score=risk_score,
        risk_level=risk_level,
        threat_category=threat_category,
        reasons=reasons,
        recommendation=recommendation,
    )