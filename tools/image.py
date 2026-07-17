import requests

PEXELS_API_KEY = "V6GJ8DqqjZyrAU1aPwIUQON4mX6yaNuM3pXS3YLRLtITqu4EsQGGbUew"
PEXELS_URL = "https://api.pexels.com/v1/search"

# Common words that indicate a person/celebrity search
# Pexels doesn't have photos of specific people, so we handle these specially
GENERIC_OBJECTS = {
    "lion", "tiger", "cat", "dog", "bird", "flower", "mountain",
    "beach", "sunset", "car", "bike", "food", "nature", "city",
    "sky", "rain", "snow", "forest", "river", "ocean", "waterfall",
    "football", "cricket", "basketball", "horse", "elephant", "wolf",
}


def is_celebrity_search(query: str) -> bool:
    """
    Detect if the query looks like a specific person/celebrity
    who likely won't be found on Pexels stock photos.
    """
    words = query.lower().split()
    # If the query has 2+ words and none match common objects → likely a person
    if len(words) >= 2:
        if not any(w in GENERIC_OBJECTS for w in words):
            return True
    return False


def execute(arguments: dict):
    query = arguments.get("query", "").strip()

    if not query:
        return "Image Error: Query not provided."

    try:
        headers = {"Authorization": PEXELS_API_KEY}

        response = requests.get(
            PEXELS_URL,
            headers=headers,
            params={
                "query": query,
                "per_page": 5,
                "orientation": "landscape",
            },
            timeout=10,
        )

        response.raise_for_status()
        data = response.json()
        photos = data.get("photos", [])

        if not photos:
            return (
                f"❌ No image found for '{query}'.\n"
                f"💡 Note: Pexels stock library may not have photos of specific "
                f"celebrities or people. Try searching for a general topic instead."
            )

        # Pick the most relevant photo by matching query words in alt text
        query_words = set(query.lower().split())
        best_photo = photos[0]
        best_score = -1

        for photo in photos:
            alt = photo.get("alt", "").lower()
            score = sum(1 for word in query_words if word in alt)
            if score > best_score:
                best_score = score
                best_photo = photo

        # If best score is 0 AND it looks like a celebrity search → warn user
        if best_score == 0 and is_celebrity_search(query):
            return (
                f"⚠️ Could not find a relevant image for '{query}'.\n\n"
                f"📌 Pexels is a stock photo library — it does not have photos of "
                f"specific celebrities, influencers, or public figures like "
                f"**'{query}'**.\n\n"
                f"✅ Try searching for general topics instead, for example:\n"
                f"   • 'lion image'\n"
                f"   • 'sunset beach'\n"
                f"   • 'cricket match'"
            )

        image_url = best_photo["src"]["large2x"]
        photographer = best_photo.get("photographer", "Unknown")
        alt_text = best_photo.get("alt", query)

        # Return special marker so app.py can display image directly
        return f"IMAGE::{image_url}::📸 {alt_text} | Photographer: {photographer}"

    except Exception as e:
        return f"Image Error: {e}"


if __name__ == "__main__":
    print(execute({"query": "lion"}))
    print(execute({"query": "elvish yadav"}))