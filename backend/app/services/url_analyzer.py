import ipaddress
import re
from urllib.parse import urlparse
from difflib import SequenceMatcher

from app.schemas.url import URLResponse
from app.utils.url_utils import extract_hostname
from app.data.brands import KNOWN_BRANDS

def check_https(url: str) -> tuple[int, list[str]]:
    risk_score = 0
    reasons: list[str] = []

    if not url.startswith("https://"):
        risk_score += 20
        reasons.append("URL does not use HTTPS.")

    return risk_score, reasons


def check_url_length(url: str) -> tuple[int, list[str]]:
    risk_score = 0
    reasons: list[str] = []

    if len(url) > 100:
        risk_score += 10
        reasons.append("URL is unusually long.")

    return risk_score, reasons


def check_ip_address(url: str) -> tuple[int, list[str]]:
    risk_score = 0
    reasons: list[str] = []

    try:
        hostname = urlparse(url).hostname

        if hostname:
            ipaddress.ip_address(hostname)
            risk_score += 25
            reasons.append("URL uses an IP address instead of a domain name.")

    except ValueError:
        pass

    return risk_score, reasons


def check_suspicious_characters(url: str) -> tuple[int, list[str]]:
    risk_score = 0
    reasons: list[str] = []

    suspicious_characters = ["@", "%", "$"]

    found_characters = [
        char for char in suspicious_characters
        if char in url
    ]

    if found_characters:
        risk_score += 10
        reasons.append(
            "URL contains suspicious special characters."
        )

    return risk_score, reasons


def analyze_url(url: str) -> URLResponse:
    risk_score: int = 0
    reasons: list[str] = []

    checks = [
        check_https,
        check_url_length,
        check_ip_address,
        check_suspicious_characters,
        check_suspicious_domain,
        check_brand_impersonation,
        check_typosquatting,
        check_suspicious_brand_path,
    ]

    for check in checks:
        points, found_reasons = check(url)

        risk_score += points
        reasons.extend(found_reasons)

    risk_score = min(risk_score, 100)
    safety_score = 100 - risk_score

    reason_text = " ".join(reasons).lower()

    if (
        "brand" in reason_text
        or "resembles" in reason_text
    ):
        threat_category = "phishing_or_impersonation"

    elif "ip address" in reason_text:
        threat_category = "suspicious_ip_url"

    elif risk_score > 0:
        threat_category = "general_suspicious_url"

    else:
        threat_category = "no_clear_threat_detected"

    if risk_score >= 70:
        risk_level = "high"
        recommendation = (
            "Do not visit the URL or enter personal information. "
            "Verify the website through the organisation's official website."
        )
    elif risk_score >= 35:
        risk_level = "medium"
        recommendation = (
            "Treat this URL cautiously. Avoid entering sensitive information "
            "until the website's authenticity is verified."
        )
    elif threat_category == "phishing_or_impersonation":
        risk_level = "low"
        recommendation = (
            "Be cautious with this URL. The address contains a brand-like "
            "name that may be associated with impersonation. Verify the "
            "website through the organisation's official website."
        )
    else:
        risk_level = "low"
        recommendation = (
            "No strong malicious URL indicators were detected, but verify "
            "the website before entering sensitive information."
        )

    if not reasons:
        reasons.append(
            "No common malicious URL indicators were detected "
            "by the baseline rules."
        )

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

def check_suspicious_domain(url: str) -> tuple[int, list[str]]:
    risk_score = 0
    reasons: list[str] = []

    hostname = extract_hostname(url)

    if hostname is None:
        risk_score += 20
        reasons.append("URL does not contain a valid hostname.")
        return risk_score, reasons

    parts = hostname.split(".")

    if len(parts) > 4:
        risk_score += 10
        reasons.append(
            "URL contains an unusually complex domain structure."
        )

    return risk_score, reasons

def check_brand_impersonation(url: str) -> tuple[int, list[str]]:
    risk_score = 0
    reasons: list[str] = []

    hostname = extract_hostname(url)

    if hostname is None:
        return risk_score, reasons

    hostname = hostname.lower()

    for brand, legitimate_domains in KNOWN_BRANDS.items():
        if brand in hostname:
            if hostname not in legitimate_domains:
                risk_score += 25
                reasons.append(
                    f"Domain may be impersonating the brand '{brand}'."
                )

            break

    return risk_score, reasons

def check_typosquatting(url: str) -> tuple[int, list[str]]:
    risk_score = 0
    reasons: list[str] = []

    hostname = extract_hostname(url)

    if hostname is None:
        return risk_score, reasons

    domain_parts = hostname.lower().split(".")

    for part in domain_parts:
        words = re.split(r"[-_]", part)

        for word in words:
            for brand in KNOWN_BRANDS:
                if word == brand:
                    continue

                similarity = SequenceMatcher(
                    None,
                    word,
                    brand,
                ).ratio()

                if similarity >= 0.80:
                    risk_score += 30
                    reasons.append(
                        f"Domain contains a name closely resembling "
                        f"the brand '{brand}'."
                    )
                    return risk_score, reasons

    return risk_score, reasons

def check_suspicious_brand_path(url: str) -> tuple[int, list[str]]:
    risk_score = 0
    reasons: list[str] = []

    parsed_url = urlparse(url)

    path_parts = re.split(r"[/\-_]", parsed_url.path.lower())

    for part in path_parts:
        if not part:
            continue

        for brand in KNOWN_BRANDS:
            similarity = SequenceMatcher(
                None,
                part,
                brand,
            ).ratio()

            if similarity >= 0.80:
                risk_score += 20
                reasons.append(
                    f"URL path contains a name closely resembling "
                    f"the brand '{brand}'."
                )
                return risk_score, reasons

    return risk_score, reasons