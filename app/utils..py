import re


def slugify(text):
    """Turn a string into a URL-friendly slug without needing an extra package."""
    text = text.strip().lower()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_-]+", "-", text)
    return text.strip("-") or "item"
