import re
from collections import defaultdict
from dataclasses import dataclass
from typing import Any


# ============================================================
# Evidence model
# ============================================================

@dataclass(frozen=True)
class Evidence:
    signal: str
    category: str
    weight: int
    reason: str


# ============================================================
# Pattern definitions
# ============================================================

CATEGORY_PATTERNS: dict[str, list[tuple[str, int, str]]] = {
    "banking_or_kyc_scam": [
        (
            r"\b(?:kyc|e-?kyc)\b",
            20,
            "The message contains KYC-related language commonly used in scams.",
        ),
        (
            r"\b(?:bank|banking|upi|netbanking|net banking|credit card|debit card)\b",
            8,
            "The message refers to banking or payment services.",
        ),
        (
            r"\b(?:account)\b.{0,60}\b(?:blocked|suspended|deactivated|closed|frozen|restricted|locked)\b",
            25,
            "The message threatens account suspension, blocking, or restriction.",
        ),
    ],

    "credential_theft": [
        (
            r"\b(?:share|send|provide|give|submit|enter|reveal|tell|forward|reply\s+with|type)\b"
            r".{0,60}"
            r"\b(?:otp|pin|password|cvv|passcode|verification\s+code|security\s+code)\b",
            35,
            "The message asks the user to provide sensitive authentication information.",
        ),
        (
            r"\b(?:otp|pin|password|cvv|passcode|verification\s+code|security\s+code)\b"
            r".{0,60}"
            r"\b(?:share|send|provide|give|submit|enter|reveal|tell|forward|reply\s+with|type)\b",
            35,
            "The message asks the user to provide sensitive authentication information.",
        ),
        (
            r"\b(?:aadhaar|aadhar|pan\s+card|pan\s+number|account\s+number)\b",
            15,
            "The message refers to sensitive personal or financial information.",
        ),
    ],

    "lottery_or_reward_scam": [
        (
            r"\b(?:won|winner|lottery|prize|reward|cashback|cash\s+prize|jackpot)\b",
            20,
            "The message uses a reward, prize, or winning claim to persuade the user.",
        ),
        (
            r"\b(?:free\s+money|claim\s+(?:now|your|the)|congratulations)\b",
            15,
            "The message uses reward-based persuasion.",
        ),
    ],

    "fake_job_scam": [
        (
            r"\b(?:part[-\s]?time\s+job|work\s+from\s+home|job\s+offer|online\s+job|"
            r"work\s+from\s+home\s+job)\b",
            20,
            "The message contains an unsolicited or potentially suspicious job opportunity.",
        ),
        (
            r"\b(?:earn|make)\b.{0,40}\b(?:daily|per\s+day|weekly|per\s+week|monthly)\b",
            20,
            "The message promises unusually quick or easy earnings.",
        ),
    ],

    "shopping_or_delivery_scam": [
        (
            r"\b(?:parcel|courier|delivery|package|shipment)\b",
            10,
            "The message refers to a parcel or delivery.",
        ),
        (
            r"\b(?:delivery\s+fee|customs\s+fee|redelivery\s+fee|shipping\s+fee)\b",
            25,
            "The message requests an unexpected delivery-related payment.",
        ),
        (
            r"\b(?:discount|sale|offer)\b.{0,40}\b\d{2,3}\s*%\b",
            15,
            "The message advertises an unusually large discount.",
        ),
    ],

    "malicious_download": [
        (
            r"\b(?:apk|crack|mod\s+apk|torrent|keygen|patched\s+app)\b",
            30,
            "The message promotes an unofficial or potentially unsafe download.",
        ),
        (
            r"\.(?:apk|exe|msi|scr|bat|cmd|zip|rar)\b",
            25,
            "The message contains a potentially dangerous file extension.",
        ),
    ],
}


GENERAL_PATTERNS: list[tuple[str, int, str]] = [
    (
        r"\b(?:urgent|urgently|immediately|asap|right\s+away|act\s+now|quickly|"
        r"today\s+only|within\s+\d+\s+(?:minutes?|hours?))\b",
        15,
        "The message creates urgency and pressures the user to take an immediate action.",
    ),
    (
        r"\b(?:click\s+here|tap\s+here|open\s+the\s+link|visit\s+the\s+link|"
        r"click\s+the\s+link|tap\s+the\s+link)\b",
        12,
        "The message encourages the user to open a link.",
    ),
    (
        r"https?://\S+|www\.\S+",
        10,
        "The message contains a website link.",
    ),
    (
        r"\b(?:pay|payment|transfer|send\s+money|registration\s+fee|processing\s+fee|"
        r"deposit|fee|charge)\b",
        12,
        "The message requests or refers to a payment or money transfer.",
    ),
    (
        r"\b(?:verify|update|confirm|validate)\b.{0,60}"
        r"\b(?:account|details|identity|information|kyc|profile)\b",
        15,
        "The message asks the user to verify or update sensitive details.",
    ),
]


# ============================================================
# Utility functions
# ============================================================

def _add_reason(reasons: list[str], reason: str) -> None:
    if reason not in reasons:
        reasons.append(reason)


def normalize_message(text: str) -> str:
    """
    Normalize common formatting variations without destroying
    useful information such as URLs or file extensions.
    """

    normalized = text.lower()

    # Treat separators commonly used to disguise phrases as spaces.
    normalized = re.sub(r"[_\-/\\|]+", " ", normalized)

    # Normalize repeated whitespace.
    normalized = re.sub(r"\s+", " ", normalized)

    return normalized.strip()


# ============================================================
# Protective / warning context
# ============================================================

PROTECTIVE_PATTERNS = [
    r"\bnever\s+(?:share|send|give|provide|disclose|enter|reveal|tell)\b",
    r"\bdo\s+not\s+(?:share|send|give|provide|disclose|enter|reveal|tell)\b",
    r"\bdon['’]?t\s+(?:share|send|give|provide|disclose|enter|reveal|tell)\b",
    r"\bnever\s+click\b",
    r"\bdo\s+not\s+click\b",
    r"\bdon['’]?t\s+click\b",
    r"\bwill\s+never\s+ask\b",
    r"\bnever\s+ask\s+for\b",
    r"\bshould\s+never\s+ask\b",
    r"\bbeware\s+of\b",
    r"\bwarning\b",
    r"\bscam\s+alert\b",
    r"\bfraud\s+alert\b",
    r"\bsecurity\s+advisory\b",
]


def detect_protective_context(text: str) -> bool:
    return any(
        re.search(pattern, text, flags=re.IGNORECASE)
        for pattern in PROTECTIVE_PATTERNS
    )


def is_protective_credential_context(text: str) -> bool:
    credential_pattern = (
        r"\b(?:otp|pin|password|cvv|passcode|verification\s+code|security\s+code)\b"
    )

    if not re.search(credential_pattern, text, flags=re.IGNORECASE):
        return False

    protective_patterns = [
        r"\bnever\b.{0,60}\b(?:share|send|give|provide|disclose|enter|reveal|tell)\b",
        r"\bdo\s+not\b.{0,60}\b(?:share|send|give|provide|disclose|enter|reveal|tell)\b",
        r"\bdon['’]?t\b.{0,60}\b(?:share|send|give|provide|disclose|enter|reveal|tell)\b",
        r"\b(?:bank|banking)\b.{0,60}\bwill\s+never\s+ask\b",
        r"\bnever\s+ask\s+for\b.{0,60}" + credential_pattern,
    ]

    return any(
        re.search(pattern, text, flags=re.IGNORECASE)
        for pattern in protective_patterns
    )


# ============================================================
# Evidence detectors
# ============================================================

def detect_credential_request(text: str) -> list[Evidence]:
    """
    Detect an actual request for credentials.

    Merely mentioning OTP/PIN/password is NOT enough.
    """

    if is_protective_credential_context(text):
        return []

    credential_pattern = (
        r"\b(?:otp|pin|password|cvv|passcode|verification\s+code|security\s+code)\b"
    )

    request_pattern = (
        r"\b(?:share|send|provide|give|submit|enter|reveal|tell|forward|"
        r"reply\s+with|type|confirm)\b"
    )

    if (
        re.search(credential_pattern, text, flags=re.IGNORECASE)
        and re.search(request_pattern, text, flags=re.IGNORECASE)
    ):
        return [
            Evidence(
                signal="credential_request",
                category="credential_theft",
                weight=35,
                reason=(
                    "The message asks the user to provide sensitive "
                    "authentication information."
                ),
            )
        ]

    return []


def detect_urgency(text: str) -> list[Evidence]:
    urgency_pattern = (
        r"\b(?:urgent|urgently|immediately|asap|right\s+away|act\s+now|quickly|"
        r"today\s+only|within\s+\d+\s+(?:minutes?|hours?)|"
        r"before\s+(?:it|your|the)\s+(?:expires?|deadline))\b"
    )

    action_pattern = (
        r"\b(?:click|tap|open|visit|send|share|pay|transfer|submit|verify|"
        r"confirm|update|claim|reply|provide|enter)\b"
    )

    if (
        re.search(urgency_pattern, text, flags=re.IGNORECASE)
        and re.search(action_pattern, text, flags=re.IGNORECASE)
    ):
        return [
            Evidence(
                signal="urgent_action",
                category="social_engineering",
                weight=15,
                reason=(
                    "The message creates urgency and pressures the user "
                    "to take an immediate action."
                ),
            )
        ]

    return []


def detect_reward_lure(text: str) -> list[Evidence]:
    reward_pattern = (
        r"\b(?:won|winner|lottery|prize|reward|cashback|cash\s+prize|"
        r"jackpot|congratulations)\b"
    )

    if re.search(reward_pattern, text, flags=re.IGNORECASE):
        return [
            Evidence(
                signal="reward_lure",
                category="lottery_or_reward_scam",
                weight=10,
                reason=(
                    "The message uses a reward, prize, or winning claim "
                    "to persuade the user."
                ),
            )
        ]

    return []


def detect_account_compromise(text: str) -> list[Evidence]:
    account_problem_pattern = (
        r"\b(?:account|bank\s+account|profile)\b.{0,60}"
        r"\b(?:hacked|compromised|blocked|suspended|locked|deactivated|"
        r"frozen|restricted)\b"
    )

    reverse_pattern = (
        r"\b(?:hacked|compromised)\b.{0,60}"
        r"\b(?:account|bank\s+account|profile)\b"
    )

    if (
        re.search(account_problem_pattern, text, flags=re.IGNORECASE)
        or re.search(reverse_pattern, text, flags=re.IGNORECASE)
    ):
        return [
            Evidence(
                signal="account_compromise",
                category="credential_theft",
                weight=20,
                reason=(
                    "The message claims there is an account security "
                    "problem."
                ),
            )
        ]

    return []


# ============================================================
# Contextual combinations
# ============================================================

def detect_compound_indicators(
    text: str,
) -> list[Evidence]:
    evidence: list[Evidence] = []

    if is_protective_credential_context(text):
        return evidence

    account_compromised = bool(
        detect_account_compromise(text)
    )

    credential_requested = bool(
        detect_credential_request(text)
    )

    urgency_detected = bool(
        detect_urgency(text)
    )

    # Account problem + credential request is a very strong signal.
    if account_compromised and credential_requested:
        evidence.append(
            Evidence(
                signal="account_compromise_credential_request",
                category="credential_theft",
                weight=30,
                reason=(
                    "The message claims there is an account security "
                    "problem and then asks for authentication information."
                ),
            )
        )

    # Account problem + urgency is also suspicious.
    elif account_compromised and urgency_detected:
        evidence.append(
            Evidence(
                signal="account_compromise_urgency",
                category="credential_theft",
                weight=15,
                reason=(
                    "The message combines an account security claim "
                    "with pressure to act quickly."
                ),
            )
        )

    return evidence


# ============================================================
# Pattern evidence
# ============================================================

def detect_pattern_evidence(
    text: str,
) -> list[Evidence]:
    evidence: list[Evidence] = []

    protective = detect_protective_context(text)

    for pattern, weight, reason in GENERAL_PATTERNS:
        if re.search(pattern, text, flags=re.IGNORECASE):
            # A protective message mentioning a link is still allowed,
            # but credential/payment warnings should not be treated as
            # direct requests.
            if protective and (
                "payment" in reason.lower()
                or "sensitive details" in reason.lower()
            ):
                continue

            evidence.append(
                Evidence(
                    signal="general_pattern",
                    category="general_suspicious_message",
                    weight=weight,
                    reason=reason,
                )
            )

    for category, patterns in CATEGORY_PATTERNS.items():
        for pattern, weight, reason in patterns:
            if not re.search(pattern, text, flags=re.IGNORECASE):
                continue

            # Sensitive credentials alone are not evidence of theft.
            if category == "credential_theft":
                if "authentication" in reason.lower():
                    if not detect_credential_request(text):
                        continue

                if "sensitive personal" in reason.lower():
                    # Keep this evidence, but at a lower weight unless
                    # there is an actual request.
                    weight = 8

            evidence.append(
                Evidence(
                    signal="category_pattern",
                    category=category,
                    weight=weight,
                    reason=reason,
                )
            )

    return evidence


# ============================================================
# Scoring
# ============================================================

def calculate_risk_score(
    evidence: list[Evidence],
) -> tuple[int, dict[str, int]]:
    """
    Calculate one final score while preventing multiple detectors
    from endlessly stacking the same underlying signal.
    """

    category_scores: defaultdict[str, int] = defaultdict(int)

    # Each signal should normally contribute once.
    seen_signals: set[str] = set()

    for item in evidence:
        if item.signal in seen_signals:
            continue

        seen_signals.add(item.signal)
        category_scores[item.category] += item.weight

    if not category_scores:
        return 0, {}

    # General suspicious evidence is supporting evidence, not a
    # standalone reason to make a message high-risk.
    general_score = category_scores.get(
        "general_suspicious_message",
        0,
    )

    category_scores.pop(
        "general_suspicious_message",
        None,
    )

    category_total = sum(category_scores.values())

    # General indicators can contribute, but with diminishing weight.
    adjusted_general = min(general_score, 25)

    total_score = category_total + adjusted_general

    return min(total_score, 100), dict(category_scores)


# ============================================================
# Classification
# ============================================================

def determine_threat_category(
    risk_score: int,
    category_scores: dict[str, int],
) -> str:

    if not category_scores:
        if risk_score >= 35:
            return "general_suspicious_message"

        return "no_clear_threat_detected"

    strongest_category = max(
        category_scores,
        key=category_scores.get,
    )

    strongest_score = category_scores[strongest_category]

    # Do not label something as a specific scam merely because
    # one weak keyword happened to match.
    if strongest_score < 15:
        if risk_score >= 35:
            return "general_suspicious_message"

        return "no_clear_threat_detected"

    return strongest_category


def determine_risk_level(
    risk_score: int,
) -> str:

    if risk_score >= 70:
        return "high"

    if risk_score >= 35:
        return "medium"

    return "low"


def get_recommendation(
    risk_level: str,
    threat_category: str,
) -> str:

    if risk_level == "high":
        return (
            "Do not click links, make payments, download files, or share "
            "personal information. Verify the message through the "
            "organisation's official website or another trusted channel."
        )

    if risk_level == "medium":
        return (
            "Treat this message cautiously. Verify the sender independently "
            "and avoid clicking links, sharing sensitive information, or "
            "making payments until the message is confirmed."
        )

    if threat_category == "no_clear_threat_detected":
        return (
            "No strong scam indicators were detected. Still verify the "
            "sender before sharing sensitive information or making payments."
        )

    return (
        "Some suspicious indicators were detected. Verify the sender "
        "independently before taking action or sharing sensitive information."
    )


# ============================================================
# Main analyzer
# ============================================================

def analyze_message_text(
    text: str,
) -> dict[str, Any]:

    normalized_text = normalize_message(text)

    # Empty input is handled defensively here as well as by the API schema.
    if not normalized_text:
        return {
            "input_type": "message",
            "analysis_method": "rule_based_baseline",
            "safety_score": 100,
            "risk_score": 0,
            "risk_level": "low",
            "threat_category": "no_clear_threat_detected",
            "reasons": [
                "No message content was provided for analysis."
            ],
            "recommendation": (
                "Please enter a message to analyze."
            ),
        }

    evidence: list[Evidence] = []

    # --------------------------------------------------------
    # 1. Context-sensitive detectors
    # --------------------------------------------------------

    evidence.extend(
        detect_credential_request(normalized_text)
    )

    evidence.extend(
        detect_urgency(normalized_text)
    )

    evidence.extend(
        detect_reward_lure(normalized_text)
    )

    evidence.extend(
        detect_account_compromise(normalized_text)
    )

    # --------------------------------------------------------
    # 2. Compound indicators
    # --------------------------------------------------------

    evidence.extend(
        detect_compound_indicators(normalized_text)
    )

    # --------------------------------------------------------
    # 3. General/category patterns
    # --------------------------------------------------------

    evidence.extend(
        detect_pattern_evidence(normalized_text)
    )

    # --------------------------------------------------------
    # 4. Score
    # --------------------------------------------------------

    risk_score, category_scores = calculate_risk_score(
        evidence
    )

    risk_score = max(
        0,
        min(risk_score, 100),
    )

    safety_score = 100 - risk_score

    # --------------------------------------------------------
    # 5. Classification
    # --------------------------------------------------------

    threat_category = determine_threat_category(
        risk_score,
        category_scores,
    )

    risk_level = determine_risk_level(
        risk_score
    )

    # --------------------------------------------------------
    # 6. Reasons
    # --------------------------------------------------------

    reasons: list[str] = []

    for item in evidence:
        _add_reason(
            reasons,
            item.reason,
        )

    # A protective message containing sensitive terms should not
    # be presented as a scam merely because it mentions them.
    if (
        detect_protective_context(normalized_text)
        and not evidence
    ):
        reasons.append(
            "The message contains warning or protective language "
            "rather than directly requesting sensitive information."
        )

    if not reasons:
        reasons.append(
            "No common scam indicators were detected by the "
            "baseline rules."
        )

    # --------------------------------------------------------
    # 7. Recommendation
    # --------------------------------------------------------

    recommendation = get_recommendation(
        risk_level,
        threat_category,
    )

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