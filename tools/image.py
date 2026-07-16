import os
import requests
import streamlit as st

PEXELS_API_KEY =["V6GJ8DqqjZyrAU1aPwIUQON4mX6yaNuM3pXS3YLRLtITqu4EsQGGbUew"]
PEXELS_URL = "https://api.pexels.com/v1/search"

SAVE_DIR = "data/images"


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

        os.makedirs(SAVE_DIR, exist_ok=True)

        safe_name = "_".join(query.lower().split())
        file_path = os.path.join(SAVE_DIR, f"{safe_name}.jpg")

        img_response = requests.get(image_url, timeout=15)
        img_response.raise_for_status()

        with open(file_path, "wb") as f:
            f.write(img_response.content)

        return (
            f"🖼️ Image for '{query}' downloaded successfully!\n"
            f"📸 Photographer: {photographer}\n"
            f"📁 Saved at: {file_path}\n"
            f"🔗 URL: {image_url}"
        )

    except Exception as e:
        return f"Image Error: {e}"


if __name__ == "__main__":
    print(execute({"query": "angry cat"}))