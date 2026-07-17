import re


def clean_image_query(text: str) -> str:
    """
    Remove trigger/filler words from image query.
    Uses word-boundary regex to avoid partial word removal.
    """
    # Words to strip from the query
    remove_words = [
        "please", "can you", "could you",
        "show me", "give me", "send me",
        "download", "display", "find", "get",
        "an image of", "a picture of", "a photo of",
        "image of", "picture of", "photo of",
        "image", "picture", "photo",
        r"\bshow\b", r"\bme\b", r"\bthe\b",
        r"\ba\b", r"\ban\b",
    ]

    for word in remove_words:
        text = re.sub(word, "", text, flags=re.IGNORECASE)

    # Clean up extra spaces
    text = " ".join(text.split())
    return text.strip()


def detect_tool(user_input):
    text = user_input.lower()

    # Image
    if any(kw in text for kw in ["image", "picture", "photo", "show me", "display image"]):
        query = clean_image_query(text)
        return "image", {"query": query if query else user_input}

    # Calculator
    if re.search(r"\d+\s*[\+\-\*/]\s*\d+", text):
        return "calculator", {"expression": user_input}

    # Time
    if "time" in text or "date" in text:
        return "time", {}

    # Weather
    if "weather" in text or "temperature" in text:
        city = text.replace("weather", "").replace("in", "").strip()
        return "weather", {"city": city}

    # News
    if "news" in text:
        # Pass full text — clean_topic() in news.py handles all stripping
        return "news", {"topic": text}

    # Dictionary
    if "meaning of" in text:
        word = text.replace("meaning of", "").strip()
        return "dictionary", {"word": word}

    return None, None