from urllib.parse import urlparse


def extract_hostname(url: str) -> str | None:
    parsed_url = urlparse(url)
    return parsed_url.hostname