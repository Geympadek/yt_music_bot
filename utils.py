def is_url(text: str) -> bool:
    text = text.strip()

    if ' ' in text:
        return False

    return text.startswith("https://") or text.startswith("http://")

def is_url_playlist(url: str):
    return url.count("?list") > 0 or url.count("&list") > 0