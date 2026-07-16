import requests
import streamlit as st
from datetime import datetime, timedelta

NEWS_API_KEY = "a2d9fe97768445908783c1ebfc9c76d4"
NEWS_URL = "https://newsapi.org/v2/everything"


def clean_topic(topic: str):
    topic = topic.lower().strip()

    remove_words = [
        "tell me",
        "show me",
        "give me",
        "latest",
        "news",
        "about",
        "the",
        "they",
        "what is",
        "what are",
        "please",
    ]

    for word in remove_words:
        topic = topic.replace(word, "")

    topic = " ".join(topic.split())

    topic_map = {
        "fifa": 'FIFA AND (football OR soccer)',
        "football": "football",
        "soccer": "soccer",
        "cricket": "cricket",
        "ipl": '"Indian Premier League" OR IPL',
        "ai": '"Artificial Intelligence" OR AI',
        "artificial intelligence": '"Artificial Intelligence" OR AI',
        "tesla": "Tesla",
        "apple": "Apple",
        "google": "Google",
        "microsoft": "Microsoft",
        "openai": "OpenAI",
        "chatgpt": "ChatGPT",
    }

    return topic_map.get(topic, topic)


def execute(arguments: dict):

    topic = arguments.get("topic")

    if not topic:
        return "News Error: Topic not provided."

    topic = clean_topic(topic)

    try:

        from_date = (
            datetime.utcnow() - timedelta(days=2)
        ).strftime("%Y-%m-%d")

        params = {
            "q": topic,
            "from": from_date,
            "language": "en",
            "pageSize": 5,
            "sortBy": "publishedAt",
            "searchIn": "title,description",
            "apiKey": NEWS_API_KEY,
        }

        response = requests.get(
            NEWS_URL,
            params=params,
            timeout=10,
        )

        response.raise_for_status()

        data = response.json()

        if data.get("status") == "error":
            return f"News Error: {data.get('message')}"

        articles = data.get("articles", [])

        if not articles:
            return f"No recent news found for '{topic}'."

        result = f"📰 Latest News on '{topic}'\n\n"

        for i, article in enumerate(articles, start=1):

            title = article.get("title", "No Title")
            description = article.get("description", "No description available.")
            source = article.get("source", {}).get("name", "Unknown")
            published = article.get("publishedAt", "")

            if published:
                try:
                    published = datetime.strptime(
                        published,
                        "%Y-%m-%dT%H:%M:%SZ"
                    ).strftime("%d-%m-%Y %I:%M %p")
                except ValueError:
                    pass

            result += f"{i}. {title}\n"
            result += f"🗞️ Source: {source}\n"
            result += f"🕒 Published: {published}\n"
            result += f"{description}\n\n"

        return result.strip()

    except requests.exceptions.RequestException as e:
        return f"News Request Error: {e}"

    except Exception as e:
        return f"News Error: {e}"


if __name__ == "__main__":
    print(execute({"topic": "latest fifa news"}))