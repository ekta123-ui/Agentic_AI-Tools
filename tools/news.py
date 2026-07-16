import requests
from datetime import datetime, timedelta
import streamlit as st

NEWS_API_KEY = "a2d9fe97768445908783c1ebfc9c76d4"
NEWS_URL = "https://newsapi.org/v2/everything"  # should be https://newsapi.org/v2/everything


def execute(arguments: dict):

    topic = arguments.get("topic")

    if not topic:
        return "News Error: Topic not provided."

    try:
        from_date = (datetime.utcnow() - timedelta(days=2)).strftime("%Y-%m-%d")

        response = requests.get(
            NEWS_URL,
            params={
                "q": topic,
                "from": from_date,
                "pageSize": 5,
                "language": "en",
                "sortBy": "publishedAt",
                "searchIn": "title,description",
                "apiKey": NEWS_API_KEY,
            },
            timeout=10,
        )

        response.raise_for_status()
        data = response.json()
        articles = data.get("articles", [])

        if not articles:
            response = requests.get(
                NEWS_URL,
                params={
                    "q": topic,
                    "pageSize": 5,
                    "language": "en",
                    "sortBy": "publishedAt",
                    "apiKey": NEWS_API_KEY,
                },
                timeout=10,
            )
            response.raise_for_status()
            data = response.json()
            articles = data.get("articles", [])

        if not articles:
            return f"No recent news found for '{topic}'."

        result = f"📰 Latest News on '{topic}'\n\n"

        for i, article in enumerate(articles, start=1):
            title = article.get("title", "No Title")
            description = article.get("description", "")
            source = article.get("source", {}).get("name", "Unknown Source")
            published = article.get("publishedAt", "")

            if published:
                try:
                    published = datetime.strptime(
                        published, "%Y-%m-%dT%H:%M:%SZ"
                    ).strftime("%d-%m-%Y %I:%M %p")
                except ValueError:
                    pass

            result += f"{i}. {title}\n"
            result += f"   🗞️ Source: {source} | 🕒 {published}\n"

            if description:
                result += f"   {description}\n"

            result += "\n"

        return result.strip()

    except Exception as e:
        return f"News Error: {e}"


if __name__ == "__main__":
    print(execute({"topic": "Artificial Intelligence"}))