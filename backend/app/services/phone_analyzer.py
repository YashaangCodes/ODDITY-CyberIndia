from phonenumbers import format_number, PhoneNumberFormat

from app.schemas.phone import (
    PhoneAnalysisResponse,
    PhoneReputationEvidence,
)

from app.data.phone_reputation import PHONE_REPUTATION_DATA

from app.utils.phone_utils import (
    normalize_phone_number,
    is_valid_phone_number,
    get_phone_country,
    get_phone_number_type,
    is_indian_service_number,
)

from app.services.phone_reputation_engine import (
    calculate_combined_reputation,
)


def lookup_phone_reputation(phone_number: str):
    """Find reputation records matching a normalized phone number."""
    return [
        record
        for record in PHONE_REPUTATION_DATA
        if record["number"] == phone_number
    ]


def analyze_phone(phone_number: str) -> PhoneAnalysisResponse:
    risk_score: int = 0
    reasons: list[str] = []

    # Handle Indian emergency/service numbers first.
    # These should not be passed through normal phone-number validation.
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

    # Check whether the parsed number is actually valid.
    if not is_valid_phone_number(parsed_number):
        return PhoneAnalysisResponse(
            input_type="phone",
            analysis_method="rule_based_baseline",
            country=get_phone_country(parsed_number),
            number_type=get_phone_number_type(parsed_number),
            safety_score=None,
            risk_score=None,
            risk_level="not_applicable",
            threat_category="invalid_phone_number",
            reasons=[
                "The provided input is not a valid phone number for its region."
            ],
            recommendation=(
                "Please check the phone number and enter a valid number."
            ),
        )

    country = get_phone_country(parsed_number)
    number_type = get_phone_number_type(parsed_number)

    normalized_number = format_number(
        parsed_number,
        PhoneNumberFormat.E164,
    )

    # Reputation lookup against the local sample dataset.
    reputation_records = lookup_phone_reputation(normalized_number)

    # Calculate reputation assessment.
    reputation_assessment = calculate_combined_reputation(
        reputation_records
    )

    reputation_score = reputation_assessment["score"]
    reputation_classification = reputation_assessment["classification"]
    reputation_category = reputation_assessment["category"]
    reputation_confidence = reputation_assessment["confidence"]
    total_report_count = reputation_assessment["total_report_count"]
    source_count = reputation_assessment["source_count"]
    conflicting_evidence = reputation_assessment["conflicting_evidence"]

    reputation_evidence = (
        PhoneReputationEvidence(
            classification=reputation_classification,
            category=reputation_category or "unknown",
            report_count=total_report_count,
            source_count=source_count,
            confidence=reputation_confidence or "low",
            conflicting_evidence=conflicting_evidence,
        )
        if reputation_classification
        else None
    )

    # Add reputation-based explanations.
    if reputation_classification == "scam":
        reasons.append(
            "The phone number matches a number listed in the ScamShield-India "
            "sample scam dataset."
        )

    elif reputation_classification == "suspicious":
        reasons.append(
            "The phone number matches a number listed in the ScamShield-India "
            "sample suspicious-number dataset."
        )

    elif reputation_classification == "spam":
        reasons.append(
            "The phone number matches a number listed in the ScamShield-India "
            "sample spam dataset."
        )

    if total_report_count >= 2:
        reasons.append(
            f"The sample dataset contains {total_report_count} reputation "
            f"record(s) across {source_count} source classification(s)."
        )

    if reputation_confidence == "high":
        reasons.append(
            "The sample reputation data is marked as high confidence."
        )

    if conflicting_evidence:
        reasons.append(
            "The sample dataset contains conflicting classifications for this number."
        )

    if not reasons:
        reasons.append(
            "No suspicious indicators were detected by the current "
            "phone-number baseline."
        )

    # Combine validation/rule-based risk with reputation risk.
    risk_score = max(
        risk_score,
        reputation_score,
    )

    risk_score = min(risk_score, 100)
    safety_score = 100 - risk_score

    # Determine risk level.
    if risk_score >= 70:
        risk_level = "high"
    elif risk_score >= 35:
        risk_level = "medium"
    else:
        risk_level = "low"

    # Determine threat category and recommendation.
    if reputation_classification == "scam":
        threat_category = reputation_category or "general_scam_phone"

        recommendation = (
            "This number matches a number classified as a scam in the "
            "current sample dataset. Do not share OTPs, PINs, passwords, "
            "banking information, or make payments unless the caller is "
            "independently verified."
        )

    elif reputation_classification == "spam":
        threat_category = "spam_phone_number"

        recommendation = (
            "This number matches a number classified as spam in the "
            "current sample dataset. Be cautious about responding or "
            "sharing personal information."
        )

    elif reputation_classification == "suspicious":
        threat_category = "suspicious_phone_number"

        recommendation = (
            "This number matches a number classified as suspicious in the "
            "current sample dataset. Verify the caller independently before "
            "sharing sensitive information."
        )

    else:
        threat_category = "no_clear_threat_detected"

        recommendation = (
            "No strong suspicious indicators were detected by the current "
            "baseline. This does not guarantee that the number is safe. "
            "Do not share sensitive information unless you trust the caller."
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
        reputation_evidence=reputation_evidence,
    )