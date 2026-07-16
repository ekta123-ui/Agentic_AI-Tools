import re

def detect_tool(user_input):
    text = user_input.lower()

    # Image
    if "image" in text or "picture" in text or "photo" in text:
        query = text
        for word in ["image", "picture", "photo", "of", "send me", "give me", "show me", "download"]:
            query = query.replace(word, "")
        query = query.strip()
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
        topic = text.replace("news", "").replace("about", "").strip()
        return "news", {"topic": topic}

    # Dictionary
    if "meaning of" in text:
        word = text.replace("meaning of", "").strip()
        return "dictionary", {"word": word}

    return None, None