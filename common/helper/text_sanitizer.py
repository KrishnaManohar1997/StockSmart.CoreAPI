import bleach


def sanitize_text(text: str, strip_data: bool = False) -> str:
    return bleach.clean(text, tags=[], attributes=[], strip=strip_data)
