import re
from urllib.parse import urlparse

def is_valid_email(email: str) -> bool:
    """Simple email validation using regex."""
    pattern = r"^[\w\.-]+@[\w\.-]+\.[a-zA-Z]{2,}$"
    return re.match(pattern, email) is not None

def is_valid_phone(phone: str) -> bool:
    """Validate phone number (digits, optional +, spaces, dashes)."""
    pattern = r"^\+?[0-9\s\-]{7,15}$"
    return re.match(pattern, phone) is not None

def is_valid_url(url: str) -> bool:
    """Check that the string looks like a URL with scheme and netloc."""
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except Exception:
        return False
