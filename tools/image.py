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
            params={"query": query, "per_page": 1},
            timeout=10,
        )

        response.raise_for_status()
        data = response.json()
        photos = data.get("photos", [])

        if not photos:
            return f"No image found for '{query}'."

        photo = photos[0]
        image_url = photo["src"]["large"]
        photographer = photo.get("photographer", "Unknown")

        # Return special marker so app.py can display image directly
        return f"IMAGE::{image_url}::📸 Photographer: {photographer}"

    except Exception as e:
        return f"Image Error: {e}"


if __name__ == "__main__":
    print(execute({"query": "angry cat"}))