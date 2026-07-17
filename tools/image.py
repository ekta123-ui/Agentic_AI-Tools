import requests

PEXELS_API_KEY = "V6GJ8DqqjZyrAU1aPwIUQON4mX6yaNuM3pXS3YLRLtITqu4EsQGGbUew"
PEXELS_URL = "https://api.pexels.com/v1/search"


def execute(arguments: dict):
    query = arguments.get("query")

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
            return f"No image found for '{query}'."

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

        image_url = best_photo["src"]["large2x"]
        photographer = best_photo.get("photographer", "Unknown")
        alt_text = best_photo.get("alt", query)

        # Return special marker so app.py can display image directly
        return f"IMAGE::{image_url}::📸 {alt_text} | Photographer: {photographer}"

    except Exception as e:
        return f"Image Error: {e}"


if __name__ == "__main__":
    print(execute({"query": "Lionel Messi"}))