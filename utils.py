def is_url(text: str) -> bool:
    text = text.strip()

    if ' ' in text:
        return False

    return text.startswith("https://") or text.startswith("http://")