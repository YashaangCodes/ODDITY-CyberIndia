import re
from collections import defaultdict
from typing import Any


CATEGORY_PATTERNS: dict[str, list[tuple[str, int, str]]] = {
    "banking_or_kyc_scam": [
        (
            r"\bkyc\b",
            25,
            "The message contains KYC-related language commonly used in scams.",
        ),
        (
            r"\baccount\b.*\b(blocked|suspended|deactivated|closed)\b",
            30,
            "The message threatens account suspension or blocking.",
        ),
        (
            r"\b(bank|upi|netbanking|credit card|debit card)\b",
            10,
            "The message refers to banking or payment services.",
        ),
    ],
    "credential_theft": [
        (
            r"\b(otp|pin|password|cvv|verification code)\b",
            35,
            "The message requests or mentions sensitive authentication information.",
        ),
        (
            r"\b(aadhaar|pan card|account number)\b",
            20,
            "The message refers to sensitive personal or financial information.",
        ),
    ],
    "lottery_or_reward_scam": [
        (
            r"\b(won|winner|lottery|prize|reward|cashback)\b",
            25,
            "The message promises an unexpected reward or prize.",
        ),
        (
            r"\b(free money|claim now|congratulations)\b",
            20,
            "The message uses reward-based persuasion.",
        ),
    ],
    "fake_job_scam": [
        (
            r"\b(part[- ]?time job|work from home|job offer)\b",
            25,
            "The message contains an unsolicited job opportunity.",
        ),
        (
            r"\bearn\b.*\b(daily|per day|weekly)\b",
            20,
            "The message promises unusually quick earnings.",
        ),
    ],
    "shopping_or_delivery_scam": [
        (
            r"\b(parcel|courier|delivery|package)\b",
            15,
            "The message refers to a parcel or delivery.",
        ),
        (
            r"\b(delivery fee|customs fee|redelivery fee)\b",
            25,
            "The message requests an unexpected delivery-related payment.",
        ),
        (
            r"\b(discount|sale|offer)\b.*\b\d{2,3}%\b",
            20,
            "The message advertises an unusually large discount.",
        ),
    ],
    "malicious_download": [
        (
            r"\b(apk|crack|mod apk|torrent|keygen)\b",
            30,
            "The message promotes an unofficial or potentially unsafe download.",
        ),
        (
            r"\.(apk|exe|msi|scr|bat|cmd|zip|rar)\b",
            25,
            "The message contains a potentially dangerous file extension.",
        ),
    ],
}


GENERAL_PATTERNS: list[tuple[str, int, str]] = [
    (
        r"\b(urgent|immediately|act now|today only|within 24 hours)\b",
        15,
        "The message creates urgency and pressures the user to act quickly.",
    ),
    (
        r"\b(click here|tap here|open the link|visit the link)\b",
        15,
        "The message encourages the user to open a link.",
    ),
    (
        r"\b(pay|payment|transfer|send money|registration fee)\b",
        15,
        "The message requests a payment or money transfer.",
    ),
    (
        r"https?://\S+|www\.\S+",
        10,
        "The message contains a website link.",
    ),
    (
        r"\b(verify|update|confirm)\b.*\b(account|details|identity)\b",
        20,
        "The message asks the user to verify or update sensitive details.",
    ),
]


def _add_reason(reasons: list[str], reason: str) -> None:
    if reason not in reasons:
        reasons.append(reason)


def analyze_message_text(text: str) -> dict[str, Any]:
    normalized_text = " ".join(text.lower().split())

    risk_score = 0
    reasons: list[str] = []
    category_scores: defaultdict[str, int] = defaultdict(int)

    for pattern, points, reason in GENERAL_PATTERNS:
        if re.search(pattern, normalized_text, flags=re.IGNORECASE):
            risk_score += points
            _add_reason(reasons, reason)

    for category, patterns in CATEGORY_PATTERNS.items():
        for pattern, points, reason in patterns:
            if re.search(pattern, normalized_text, flags=re.IGNORECASE):
                risk_score += points
                category_scores[category] += points
                _add_reason(reasons, reason)

    risk_score = min(risk_score, 100)
    safety_score = 100 - risk_score

    if risk_score >= 70:
        risk_level = "high"
        recommendation = (
            "Do not click links, make payments, download files, or share personal "
            "information. Verify the message through the organisation's official website."
        )
    elif risk_score >= 35:
        risk_level = "medium"
        recommendation = (
            "Treat this message cautiously. Verify the sender and avoid using links "
            "contained in the message until its authenticity is confirmed."
        )
    else:
        risk_level = "low"
        recommendation = (
            "No strong scam indicators were detected, but independently verify the "
            "sender before sharing sensitive information or making payments."
        )

    if category_scores:
        threat_category = max(category_scores, key=category_scores.get)
    elif risk_score > 0:
        threat_category = "general_suspicious_message"
    else:
        threat_category = "no_clear_threat_detected"

    if not reasons:
        reasons.append("No common scam indicators were detected by the baseline rules.")

    return {
        "input_type": "message",
        "analysis_method": "rule_based_baseline",
        "safety_score": safety_score,
        "risk_score": risk_score,
        "risk_level": risk_level,
        "threat_category": threat_category,
        "reasons": reasons,
        "recommendation": recommendation,
    }