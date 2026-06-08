from urllib.parse import urlparse

def normalize_url(url: str) -> str:
    parsed_url = urlparse(url)
    print("URL=" + url)
    normalized_string = (parsed_url.netloc + parsed_url.path).rstrip("/").strip().lower()
    print(normalized_string)
    return normalized_string 