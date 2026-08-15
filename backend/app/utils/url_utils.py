from __future__ import annotations

import ipaddress
import re
from urllib.parse import ParseResult, unquote, urlparse


# ============================================================
# Constants
# ============================================================

SUPPORTED_SCHEMES = {"http", "https"}

HOSTNAME_LABEL_PATTERN = re.compile(
    r"^[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?$"
)

LOCAL_HOSTNAMES = {
    "localhost",
}


# ============================================================
# URL normalization
# ============================================================

def normalize_url(url: str) -> tuple[str, bool]:
    """
    Normalize common user-entered URL variations.

    Returns:
        (normalized_url, scheme_was_added)
    """

    value = url.strip()

    value = re.sub(
        r"^(https?)\\://",
        r"\1://",
        value,
        flags=re.IGNORECASE,
    )

    if re.match(
        r"^https?://",
        value,
        flags=re.IGNORECASE,
    ):
        return value, False

    if re.match(
        r"^[a-zA-Z][a-zA-Z0-9+.-]*://",
        value,
    ):
        return value, False

    return f"https://{value}", True


# ============================================================
# Parsing
# ============================================================

def parse_url(url: str) -> ParseResult:
    """
    Safely parse a URL.
    """

    return urlparse(url)


# ============================================================
# Hostname extraction
# ============================================================

def extract_hostname(url: str) -> str | None:
    """
    Extract the hostname from a URL.
    """

    try:
        parsed_url = urlparse(url)
        return parsed_url.hostname
    except ValueError:
        return None


# ============================================================
# IP address helpers
# ============================================================

def is_ip_address(hostname: str | None) -> bool:
    """
    Return True when the hostname is a valid IPv4 or IPv6 address.
    """

    if not hostname:
        return False

    try:
        ipaddress.ip_address(hostname)
        return True
    except ValueError:
        return False


def is_private_ip(hostname: str | None) -> bool:
    """
    Return True when the hostname is a private/local IP address.
    """

    if not hostname:
        return False

    try:
        return ipaddress.ip_address(hostname).is_private
    except ValueError:
        return False


# ============================================================
# URL decoding
# ============================================================

def decode_url_component(
    value: str,
    max_rounds: int = 3,
) -> str:
    """
    Repeatedly URL-decode a component.
    """

    decoded = value

    for _ in range(max_rounds):
        new_value = unquote(decoded)

        if new_value == decoded:
            break

        decoded = new_value

    return decoded


# ============================================================
# Domain matching
# ============================================================

def hostname_matches_domain(
    hostname: str | None,
    legitimate_domain: str,
) -> bool:
    """
    Determine whether a hostname is the legitimate domain itself
    or a legitimate subdomain of it.
    """

    if not hostname:
        return False

    hostname = hostname.lower().rstrip(".")
    legitimate_domain = legitimate_domain.lower().rstrip(".")

    return (
        hostname == legitimate_domain
        or hostname.endswith(f".{legitimate_domain}")
    )


# ============================================================
# Hostname validation
# ============================================================

def _is_valid_domain_hostname(hostname: str) -> bool:
    """
    Validate a normal DNS-style hostname.
    """

    if not hostname:
        return False

    hostname = hostname.lower().rstrip(".")

    if not hostname:
        return False

    if any(char.isspace() for char in hostname):
        return False

    if any(
        char in hostname
        for char in "/?#@"
    ):
        return False

    if ".." in hostname:
        return False

    labels = hostname.split(".")

    if len(labels) < 2:
        return hostname in LOCAL_HOSTNAMES

    for label in labels:
        if not HOSTNAME_LABEL_PATTERN.fullmatch(label):
            return False

    if len(hostname) > 253:
        return False

    return True


def has_valid_hostname(parsed_url: ParseResult) -> bool:
    """
    Check whether the parsed URL contains a usable hostname.
    """

    try:
        hostname = parsed_url.hostname
    except ValueError:
        return False

    if not hostname:
        return False

    hostname = hostname.strip()

    if not hostname:
        return False

    if is_ip_address(hostname):
        return True

    if hostname.lower() in LOCAL_HOSTNAMES:
        return True

    return _is_valid_domain_hostname(hostname)


# ============================================================
# Scheme validation
# ============================================================

def has_valid_scheme(parsed_url: ParseResult) -> bool:
    """
    Check whether the URL uses a supported network scheme.
    """

    return parsed_url.scheme.lower() in SUPPORTED_SCHEMES