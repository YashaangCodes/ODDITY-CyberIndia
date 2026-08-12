from typing import TypedDict

from app.data.phone_reputation import PhoneReputationRecord

class CombinedReputationAssessment(TypedDict):
    score: int
    classification: str | None
    category: str | None
    confidence: str | None
    total_report_count: int
    source_count: int
    classifications_found: list[str]
    conflicting_evidence: bool
    records: list[PhoneReputationRecord]

CLASSIFICATION_SCORES = {
    "scam": 50,
    "suspicious": 30,
    "spam": 20,
}


CONFIDENCE_MULTIPLIERS = {
    "low": 0.5,
    "medium": 0.75,
    "high": 1.0,
}


def get_report_count_bonus(report_count: int) -> int:
    if report_count >= 25:
        return 20
    elif report_count >= 10:
        return 15
    elif report_count >= 5:
        return 10
    elif report_count >= 2:
        return 5
    else:
        return 0


def calculate_reputation_score(
    record: PhoneReputationRecord,
) -> int:

    base_score = CLASSIFICATION_SCORES[record["classification"]]

    confidence_multiplier = CONFIDENCE_MULTIPLIERS[
        record["confidence"]
    ]

    confidence_adjusted_score = (
        base_score * confidence_multiplier
    )

    report_bonus = get_report_count_bonus(
        record["report_count"]
    )

    reputation_score = (
        confidence_adjusted_score + report_bonus
    )

    return min(round(reputation_score), 100)

def calculate_combined_reputation(
    records: list[PhoneReputationRecord],
) -> CombinedReputationAssessment:

    if not records:
        return {
            "score": 0,
            "classification": None,
            "category": None,
            "confidence": None,
            "total_report_count": 0,
            "source_count": 0,
            "classifications_found": [],
            "conflicting_evidence": False,
            "records": [],
        }

    scored_records = [
        (
            calculate_reputation_score(record),
            record,
        )
        for record in records
    ]

    scored_records.sort(
        key=lambda item: item[0],
        reverse=True,
    )

    strongest_score, strongest_record = scored_records[0]

    classifications_found = list(
        dict.fromkeys(
            record["classification"]
            for record in records
        )
    )

    if "scam" in classifications_found:
        final_classification = "scam"
    elif "suspicious" in classifications_found:
        final_classification = "suspicious"
    else:
        final_classification = "spam"

    confidence_levels = [
        record["confidence"]
        for record in records
    ]

    if "high" in confidence_levels:
        final_confidence = "high"
    elif "medium" in confidence_levels:
        final_confidence = "medium"
    else:
        final_confidence = "low"

    total_report_count = sum(
        record["report_count"]
        for record in records
    )

    unique_sources = {
        record["source"]
        for record in records
    }

    source_count = len(unique_sources)
    
    conflicting_evidence = len(
        classifications_found
    ) > 1

    # Calculate evidence components

    classification_score = {
        "scam": 50,
        "suspicious": 30,
        "spam": 20,
    }[final_classification]

    confidence_bonus = {
        "low": 0,
        "medium": 10,
        "high": 20,
    }[final_confidence]

    report_bonus = min(
        total_report_count * 2,
        20,
    )

    source_bonus = min(
        max(source_count - 1, 0) * 5,
        15,
    )

    conflict_penalty = 5 if conflicting_evidence else 0

    combined_score = (
        classification_score
        + confidence_bonus
        + report_bonus
        + source_bonus
        - conflict_penalty
    )

    combined_score = max(
        0,
        min(combined_score, 100),
    )
    return {
        "score": combined_score,
        "classification": final_classification,
        "category": strongest_record["category"],
        "confidence": final_confidence,
        "total_report_count": total_report_count,
        "source_count": len(unique_sources),
        "classifications_found": classifications_found,
        "conflicting_evidence": conflicting_evidence,
        "records": records,
    }