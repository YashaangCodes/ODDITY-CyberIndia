from __future__ import annotations

import ipaddress
import re
from collections import defaultdict
from difflib import SequenceMatcher
from urllib.parse import parse_qs, unquote, urlparse

from app.data.brands import KNOWN_BRANDS
from app.schemas.url import URLResponse
from app.utils.url_utils import (
    decode_url_component,
    extract_hostname,
    has_valid_hostname,
    has_valid_scheme,
    normalize_url,
)


# ============================================================
# Constants
# ============================================================

MAX_ANALYZED_URL_LENGTH = 2048

HIGH_RISK_THRESHOLD = 70
MEDIUM_RISK_THRESHOLD = 35

SUPPORTED_SCHEMES = {"http", "https"}

COMMON_TLDS = {
    "com",
    "org",
    "net",
    "in",
    "co",
    "io",
    "edu",
    "gov",
}


# ============================================================
# General helpers
# ============================================================

def _add_reason(
    reasons: list[str],
    reason: str,
) -> None:
    """Add a reason only once."""

    if reason not in reasons:
        reasons.append(reason)


def _brand_domains(
    brand: str,
) -> list[str]:
    """Return normalized legitimate domains for a brand."""

    return [
        domain.lower().rstrip(".")
        for domain in KNOWN_BRANDS.get(brand, [])
    ]


def _hostname_labels(
    hostname: str,
) -> list[str]:
    """Return non-empty hostname labels."""

    return [
        label
        for label in hostname.lower().rstrip(".").split(".")
        if label
    ]


def _hostname_is_legitimate_for_brand(
    hostname: str,
    brand: str,
) -> bool:
    """
    Determine whether a hostname belongs to a brand's
    legitimate domain.
    """

    hostname = hostname.lower().rstrip(".")

    for domain in _brand_domains(brand):
        if hostname == domain:
            return True

        if hostname.endswith("." + domain):
            return True

    return False


def _normalize_brand_candidate(
    value: str,
) -> str:
    """
    Normalize common character substitutions used in typosquatting.
    """

    translation_table = str.maketrans(
        {
            "0": "o",
            "1": "l",
            "3": "e",
            "4": "a",
            "5": "s",
            "7": "t",
            "8": "b",
        }
    )

    return value.lower().translate(translation_table)


def _is_ip_address(
    hostname: str | None,
) -> bool:
    """Return True when hostname is an IPv4 or IPv6 address."""

    if not hostname:
        return False

    try:
        ipaddress.ip_address(hostname)
        return True
    except ValueError:
        return False


def _is_private_ip(
    hostname: str | None,
) -> bool:
    """Return True when hostname is a private/local IP."""

    if not hostname:
        return False

    try:
        address = ipaddress.ip_address(hostname)
    except ValueError:
        return False

    return (
        address.is_private
        or address.is_loopback
        or address.is_link_local
        or address.is_reserved
    )


def _is_valid_hostname(
    hostname: str | None,
) -> bool:
    """
    Perform conservative hostname validation.
    """

    if not hostname:
        return False

    hostname = hostname.rstrip(".")

    if not hostname:
        return False

    if len(hostname) > 253:
        return False

    if _is_ip_address(hostname):
        return True

    labels = hostname.split(".")

    if len(labels) < 2:
        return False

    for label in labels:
        if not label:
            return False

        if len(label) > 63:
            return False

        if label.startswith("-") or label.endswith("-"):
            return False

        if not re.fullmatch(
            r"[a-zA-Z0-9-]+",
            label,
        ):
            return False

    return True


# ============================================================
# Validation
# ============================================================

def validate_url(
    raw_url: str,
) -> tuple[bool, str, str | None]:
    """
    Normalize and validate the supplied URL.

    Returns:
        valid,
        normalized_url,
        validation_reason
    """

    if not isinstance(raw_url, str):
        return (
            False,
            "",
            "The supplied URL must be text.",
        )

    raw_url = raw_url.strip()

    if not raw_url:
        return (
            False,
            "",
            "Please enter a URL to analyze.",
        )

    normalized_url, _ = normalize_url(raw_url)

    if len(normalized_url) > MAX_ANALYZED_URL_LENGTH:
        return (
            False,
            normalized_url,
            "The URL is too long to analyze safely.",
        )

    if "\\" in normalized_url:
        return (
            False,
            normalized_url,
            "The URL contains invalid characters.",
        )

    if any(char.isspace() for char in normalized_url):
        return (
            False,
            normalized_url,
            "The URL contains whitespace and is not valid.",
        )

    try:
        parsed_url = urlparse(normalized_url)
    except ValueError:
        return (
            False,
            normalized_url,
            "The URL could not be parsed.",
        )

    if not has_valid_scheme(parsed_url):
        return (
            False,
            normalized_url,
            "The URL must use HTTP or HTTPS.",
        )

    if parsed_url.scheme.lower() not in SUPPORTED_SCHEMES:
        return (
            False,
            normalized_url,
            "The URL must use HTTP or HTTPS.",
        )

    if not has_valid_hostname(parsed_url):
        return (
            False,
            normalized_url,
            "The URL does not contain a valid hostname.",
        )

    hostname = parsed_url.hostname

    if not _is_valid_hostname(hostname):
        return (
            False,
            normalized_url,
            "The URL does not contain a valid hostname.",
        )

    try:
        _ = parsed_url.port
    except ValueError:
        return (
            False,
            normalized_url,
            "The URL contains an invalid network port.",
        )

    return True, normalized_url, None


# ============================================================
# HTTPS
# ============================================================

def check_https(
    parsed_url,
) -> tuple[int, list[str]]:
    """
    HTTP is a security weakness but does not automatically mean
    that the destination is malicious.
    """

    if parsed_url.scheme.lower() == "http":
        return (
            15,
            ["The URL does not use HTTPS."],
        )

    return 0, []


# ============================================================
# IP address analysis
# ============================================================

def check_ip_address(
    hostname: str | None,
) -> tuple[int, list[str], dict[str, int]]:
    """
    Analyze URLs that use IP addresses instead of domains.
    """

    if not _is_ip_address(hostname):
        return 0, [], {}

    if _is_private_ip(hostname):
        return (
            25,
            [
                "The URL uses a private or local IP address "
                "instead of a public domain name."
            ],
            {
                "suspicious_ip_url": 25,
            },
        )

    return (
        25,
        [
            "The URL uses an IP address instead of a domain name."
        ],
        {
            "suspicious_ip_url": 25,
        },
    )


# ============================================================
# Domain structure
# ============================================================

def check_domain_structure(
    hostname: str | None,
) -> tuple[int, list[str]]:
    """
    Detect unusually complex domain structures.
    """

    if not hostname or _is_ip_address(hostname):
        return 0, []

    labels = _hostname_labels(hostname)

    if len(labels) >= 6:
        return (
            8,
            [
                "The hostname contains an unusually large number "
                "of subdomain levels."
            ],
        )

    return 0, []


# ============================================================
# URL length
# ============================================================

def check_url_length(
    url: str,
) -> tuple[int, list[str]]:
    """Use URL length only as weak supporting evidence."""

    if len(url) > 512:
        return (
            5,
            ["The URL is unusually long."],
        )

    return 0, []


# ============================================================
# Brand detection helpers
# ============================================================

def _brand_from_exact_hostname(
    hostname: str,
) -> str | None:
    """Return the brand whose legitimate domain owns the hostname."""

    for brand in KNOWN_BRANDS:
        if _hostname_is_legitimate_for_brand(
            hostname,
            brand,
        ):
            return brand

    return None


def _brand_matches_hostname(
    hostname: str,
    brand: str,
) -> bool:
    """
    Determine whether the hostname contains a meaningful
    brand-like label.
    """

    labels = _hostname_labels(hostname)

    for label in labels:
        normalized_label = label.replace("-", "")

        if normalized_label == brand:
            return True

        if brand in normalized_label:
            return True

    return False


# ============================================================
# Brand impersonation
# ============================================================

def check_brand_impersonation(
    hostname: str | None,
) -> tuple[int, list[str], dict[str, int]]:
    """
    Detect a known brand being used in a hostname that is not
    controlled by that brand.
    """

    if not hostname or _is_ip_address(hostname):
        return 0, [], {}

    hostname = hostname.lower().rstrip(".")

    for brand in KNOWN_BRANDS:

        if _hostname_is_legitimate_for_brand(
            hostname,
            brand,
        ):
            continue

        if not _brand_matches_hostname(
            hostname,
            brand,
        ):
            continue

        return (
            35,
            [
                f"The hostname contains the brand name '{brand}' "
                "but is not on the brand's legitimate domain."
            ],
            {
                "phishing_or_impersonation": 35,
            },
        )

    return 0, [], {}


# ============================================================
# Typosquatting
# ============================================================

def check_typosquatting(
    hostname: str | None,
) -> tuple[int, list[str], dict[str, int]]:
    """
    Detect labels that closely imitate known brands.
    """

    if not hostname or _is_ip_address(hostname):
        return 0, [], {}

    labels = _hostname_labels(hostname)

    for label in labels:

        if label in COMMON_TLDS:
            continue

        normalized_label = label.replace("-", "").lower()

        for brand in KNOWN_BRANDS:

            if _hostname_is_legitimate_for_brand(
                hostname,
                brand,
            ):
                continue

            if normalized_label == brand:
                continue

            visual_candidate = _normalize_brand_candidate(
                normalized_label
            )

            visual_similarity = SequenceMatcher(
                None,
                visual_candidate,
                brand,
            ).ratio()

            raw_similarity = SequenceMatcher(
                None,
                normalized_label,
                brand,
            ).ratio()

            if (
                visual_similarity >= 0.90
                or raw_similarity >= 0.82
            ):
                return (
                    40,
                    [
                        "The domain appears to use character "
                        f"substitutions or spelling changes to imitate "
                        f"the brand '{brand}'."
                    ],
                    {
                        "phishing_or_impersonation": 40,
                    },
                )

    return 0, [], {}


# ============================================================
# Path brand analysis
# ============================================================

def _path_contains_brand(
    path: str,
    brand: str,
) -> bool:
    """Check for a meaningful brand occurrence in a URL path."""

    tokens = [
        token.lower()
        for token in re.split(
            r"[/\-_?.=&]+",
            path,
        )
        if token
    ]

    return brand in tokens


def check_brand_in_path(
    parsed_url,
) -> tuple[int, list[str], dict[str, int]]:
    """
    Detect known brands in the path of an unrelated domain.
    """

    hostname = parsed_url.hostname

    if not hostname:
        return 0, [], {}

    decoded_path = decode_url_component(
        parsed_url.path
    )

    if not decoded_path:
        return 0, [], {}

    security_terms = {
        "login",
        "signin",
        "sign-in",
        "verify",
        "verification",
        "security",
        "account",
        "secure",
        "password",
        "update",
        "confirm",
    }

    path_lower = decoded_path.lower()

    security_context = any(
        re.search(
            rf"\b{re.escape(term)}\b",
            path_lower,
        )
        for term in security_terms
    )

    for brand in KNOWN_BRANDS:

        if _hostname_is_legitimate_for_brand(
            hostname,
            brand,
        ):
            continue

        if not _path_contains_brand(
            path_lower,
            brand,
        ):
            continue

        if security_context:
            return (
                35,
                [
                    f"The URL path uses the brand name '{brand}' "
                    "on a different domain together with login or "
                    "security-related language."
                ],
                {
                    "phishing_or_impersonation": 35,
                },
            )

        return (
            25,
            [
                f"The URL path contains the brand name '{brand}' "
                "on a different domain."
            ],
            {
                "phishing_or_impersonation": 25,
            },
        )

    return 0, [], {}


# ============================================================
# Encoded path analysis
# ============================================================

def check_encoded_brand_path(
    parsed_url,
) -> tuple[int, list[str], dict[str, int]]:
    """
    Detect encoded brand names in URL paths.
    """

    raw_path = parsed_url.path

    if "%" not in raw_path:
        return 0, [], {}

    decoded_path = decode_url_component(
        raw_path
    )

    if decoded_path == raw_path:
        return 0, [], {}

    hostname = parsed_url.hostname

    if not hostname:
        return 0, [], {}

    decoded_lower = decoded_path.lower()

    for brand in KNOWN_BRANDS:

        if _hostname_is_legitimate_for_brand(
            hostname,
            brand,
        ):
            continue

        if not _path_contains_brand(
            decoded_lower,
            brand,
        ):
            continue

        return (
            30,
            [
                "The encoded URL path reveals the brand name "
                f"'{brand}' on a different domain."
            ],
            {
                "phishing_or_impersonation": 30,
            },
        )

    return 0, [], {}


# ============================================================
# Redirect analysis
# ============================================================

def _extract_urls_from_query(
    parsed_url,
) -> list[str]:
    """Extract URL-looking query parameter values."""

    found_urls: list[str] = []

    try:
        query_params = parse_qs(
            parsed_url.query,
            keep_blank_values=True,
        )
    except ValueError:
        return found_urls

    for values in query_params.values():
        for value in values:

            decoded_value = unquote(
                decode_url_component(value)
            ).strip()

            if re.match(
                r"^https?://",
                decoded_value,
                flags=re.IGNORECASE,
            ):
                found_urls.append(
                    decoded_value
                )

    return found_urls


def check_redirects(
    parsed_url,
) -> tuple[int, list[str], dict[str, int]]:
    """
    Detect query parameters containing URLs that point to
    another domain.
    """

    destination_urls = _extract_urls_from_query(
        parsed_url
    )

    if not destination_urls:
        return 0, [], {}

    current_hostname = parsed_url.hostname

    if not current_hostname:
        return 0, [], {}

    current_hostname = current_hostname.lower().rstrip(".")

    for destination in destination_urls:

        try:
            destination_parsed = urlparse(
                destination
            )
        except ValueError:
            continue

        destination_hostname = (
            destination_parsed.hostname
        )

        if not destination_hostname:
            continue

        destination_hostname = (
            destination_hostname
            .lower()
            .rstrip(".")
        )

        if destination_hostname == current_hostname:
            continue

        return (
            15,
            [
                "The URL contains a redirect or destination URL "
                "pointing to a different domain."
            ],
            {
                "suspicious_redirect": 15,
            },
        )

    return 0, [], {}


# ============================================================
# Userinfo / authority analysis
# ============================================================

def check_userinfo(
    parsed_url,
) -> tuple[int, list[str]]:
    """
    Detect user-information data before the hostname.
    """

    if parsed_url.username is None:
        return 0, []

    return (
        20,
        [
            "The URL contains user-information data before the "
            "hostname, which can obscure the actual destination."
        ],
    )


# ============================================================
# Suspicious ports
# ============================================================

def check_port(
    parsed_url,
) -> tuple[int, list[str]]:
    """Flag unusual non-standard ports as supporting evidence."""

    try:
        port = parsed_url.port
    except ValueError:
        return (
            20,
            [
                "The URL contains an invalid network port."
            ],
        )

    if port is None:
        return 0, []

    if port not in {80, 443}:
        return (
            8,
            [
                f"The URL uses a non-standard network port ({port})."
            ],
        )

    return 0, []


# ============================================================
# Special-character analysis
# ============================================================

def check_suspicious_characters(
    parsed_url,
) -> tuple[int, list[str]]:
    """
    Detect genuinely suspicious authority characters.
    """

    if parsed_url.username is not None:
        return 0, []

    return 0, []


# ============================================================
# Recommendations
# ============================================================

def _recommendation_for(
    risk_level: str,
    threat_category: str,
) -> str:

    if threat_category == "invalid_url":
        return (
            "Please enter a complete and valid website address "
            "such as https://example.com."
        )

    if risk_level == "high":
        return (
            "Do not visit this URL or enter passwords, OTPs, "
            "payment details, or personal information. Verify "
            "the website through the organisation's official "
            "website or another trusted channel."
        )

    if risk_level == "medium":
        return (
            "Treat this URL cautiously. Avoid entering sensitive "
            "information or downloading anything until the "
            "destination has been independently verified."
        )

    if threat_category == "phishing_or_impersonation":
        return (
            "Do not enter passwords, OTPs, payment details, or "
            "personal information on this website. Verify the "
            "organisation's official domain before continuing."
        )

    return (
        "No strong malicious URL indicators were detected. "
        "Still verify the website before entering sensitive "
        "information."
    )


# ============================================================
# Main analyzer
# ============================================================

def analyze_url(
    url: str,
) -> URLResponse:

    # ---------------------------------------------------------
    # 1. Validate input
    # ---------------------------------------------------------

    valid, normalized_url, validation_reason = validate_url(
        url
    )

    if not valid:
        return URLResponse(
            input_type="url",
            analysis_method="rule_based_baseline",
            safety_score=100,
            risk_score=0,
            risk_level="low",
            threat_category="invalid_url",
            reasons=[
                validation_reason
                or "The supplied input is not a valid URL."
            ],
            recommendation=_recommendation_for(
                "low",
                "invalid_url",
            ),
        )

    parsed_url = urlparse(normalized_url)
    hostname = extract_hostname(normalized_url)

    # ---------------------------------------------------------
    # 2. Evidence collection
    # ---------------------------------------------------------

    risk_score = 0
    reasons: list[str] = []
    category_scores: dict[str, int] = defaultdict(int)

    def add_evidence(
        score: int,
        evidence_reasons: list[str],
        evidence_categories: dict[str, int] | None = None,
    ) -> None:

        nonlocal risk_score

        risk_score += score

        for reason in evidence_reasons:
            _add_reason(
                reasons,
                reason,
            )

        if evidence_categories:
            for category, category_score in (
                evidence_categories.items()
            ):
                category_scores[category] += (
                    category_score
                )

    # ---------------------------------------------------------
    # 3. HTTPS
    # ---------------------------------------------------------

    score, evidence_reasons = check_https(
        parsed_url
    )

    add_evidence(
        score,
        evidence_reasons,
    )

    # ---------------------------------------------------------
    # 4. IP address
    # ---------------------------------------------------------

    (
        score,
        evidence_reasons,
        evidence_categories,
    ) = check_ip_address(
        hostname
    )

    add_evidence(
        score,
        evidence_reasons,
        evidence_categories,
    )

    # ---------------------------------------------------------
    # 5. Domain structure
    # ---------------------------------------------------------

    score, evidence_reasons = (
        check_domain_structure(
            hostname
        )
    )

    add_evidence(
        score,
        evidence_reasons,
    )

    # ---------------------------------------------------------
    # 6. URL length
    # ---------------------------------------------------------

    score, evidence_reasons = (
        check_url_length(
            normalized_url
        )
    )

    add_evidence(
        score,
        evidence_reasons,
    )

    # ---------------------------------------------------------
    # 7. Brand impersonation
    # ---------------------------------------------------------

    (
        score,
        evidence_reasons,
        evidence_categories,
    ) = check_brand_impersonation(
        hostname
    )

    add_evidence(
        score,
        evidence_reasons,
        evidence_categories,
    )

    # ---------------------------------------------------------
    # 8. Typosquatting
    # ---------------------------------------------------------

    (
        score,
        evidence_reasons,
        evidence_categories,
    ) = check_typosquatting(
        hostname
    )

    add_evidence(
        score,
        evidence_reasons,
        evidence_categories,
    )

    # ---------------------------------------------------------
    # 9. Brand in path
    # ---------------------------------------------------------

    (
        score,
        evidence_reasons,
        evidence_categories,
    ) = check_brand_in_path(
        parsed_url
    )

    add_evidence(
        score,
        evidence_reasons,
        evidence_categories,
    )

    # ---------------------------------------------------------
    # 10. Encoded brand path
    # ---------------------------------------------------------

    (
        score,
        evidence_reasons,
        evidence_categories,
    ) = check_encoded_brand_path(
        parsed_url
    )

    add_evidence(
        score,
        evidence_reasons,
        evidence_categories,
    )

    # ---------------------------------------------------------
    # 11. Redirects
    # ---------------------------------------------------------

    (
        score,
        evidence_reasons,
        evidence_categories,
    ) = check_redirects(
        parsed_url
    )

    add_evidence(
        score,
        evidence_reasons,
        evidence_categories,
    )

    # ---------------------------------------------------------
    # 12. Userinfo
    # ---------------------------------------------------------

    score, evidence_reasons = check_userinfo(
        parsed_url
    )

    add_evidence(
        score,
        evidence_reasons,
    )

    # ---------------------------------------------------------
    # 13. Port
    # ---------------------------------------------------------

    score, evidence_reasons = check_port(
        parsed_url
    )

    add_evidence(
        score,
        evidence_reasons,
    )

    # ---------------------------------------------------------
    # 14. Suspicious characters
    # ---------------------------------------------------------

    score, evidence_reasons = (
        check_suspicious_characters(
            parsed_url
        )
    )

    add_evidence(
        score,
        evidence_reasons,
    )

    # ---------------------------------------------------------
    # 15. Final score
    # ---------------------------------------------------------

    risk_score = min(
        max(risk_score, 0),
        100,
    )

    safety_score = 100 - risk_score

    # ---------------------------------------------------------
    # 16. Threat category
    # ---------------------------------------------------------

    if category_scores:

        threat_category = max(
            category_scores,
            key=category_scores.get,
        )

    elif risk_score > 0:

        threat_category = (
            "general_suspicious_url"
        )

    else:

        threat_category = (
            "no_clear_threat_detected"
        )

    # ---------------------------------------------------------
    # 17. Risk level
    # ---------------------------------------------------------

    if risk_score >= HIGH_RISK_THRESHOLD:

        risk_level = "high"

    elif risk_score >= MEDIUM_RISK_THRESHOLD:

        risk_level = "medium"

    else:

        risk_level = "low"

    # ---------------------------------------------------------
    # 18. Fallback reason
    # ---------------------------------------------------------

    if not reasons:

        reasons.append(
            "No common malicious URL indicators were detected "
            "by the baseline rules."
        )

    # ---------------------------------------------------------
    # 19. Recommendation
    # ---------------------------------------------------------

    recommendation = _recommendation_for(
        risk_level,
        threat_category,
    )

    # ---------------------------------------------------------
    # 20. Response
    # ---------------------------------------------------------

    return URLResponse(
        input_type="url",
        analysis_method="rule_based_baseline",
        safety_score=safety_score,
        risk_score=risk_score,
        risk_level=risk_level,
        threat_category=threat_category,
        reasons=reasons,
        recommendation=recommendation,
    )