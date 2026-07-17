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
        # Sports
        "fifa": 'FIFA AND (football OR soccer)',
        "football": "football",
        "soccer": "soccer",
        "cricket": "cricket",
        "ipl": '"Indian Premier League" OR IPL',
        "sports": "sports",
        "basketball": "basketball",
        "tennis": "tennis",
        "olympics": "Olympics",

        # Technology
        "ai": '"Artificial Intelligence" OR AI',
        "artificial intelligence": '"Artificial Intelligence" OR AI',
        "tesla": "Tesla",
        "apple": "Apple",
        "google": "Google",
        "microsoft": "Microsoft",
        "openai": "OpenAI",
        "chatgpt": "ChatGPT",
        "technology": "technology",
        "tech": "technology",
        "cybersecurity": "cybersecurity",
        "blockchain": "blockchain",
        "crypto": "cryptocurrency",
        "cryptocurrency": "cryptocurrency",
        "bitcoin": "Bitcoin",

        # Politics
        "politics": "politics",
        "political": "politics",
        "election": "election",
        "government": "government",
        "parliament": "parliament",
        "congress": "congress",
        "president": "president",
        "prime minister": "prime minister",
        "modi": "Narendra Modi",
        "trump": "Donald Trump",
        "biden": "Joe Biden",
        "india politics": "India politics",
        "us politics": "US politics",

        # Business
        "business": "business",
        "economy": "economy",
        "stock market": "stock market",
        "stocks": "stocks",
        "finance": "finance",
        "market": "market",
        "startup": "startup",

        # Health
        "health": "health",
        "medical": "medical",
        "covid": "COVID-19",
        "coronavirus": "coronavirus",
        "vaccine": "vaccine",
        "cancer": "cancer",
        "mental health": "mental health",

        # Science
        "science": "science",
        "space": "space",
        "nasa": "NASA",
        "climate": "climate change",
        "environment": "environment",
        "research": "research",

        # Entertainment
        "entertainment": "entertainment",
        "movies": "movies",
        "bollywood": "Bollywood",
        "hollywood": "Hollywood",
        "music": "music",
        "celebrity": "celebrity",

        # World
        "world": "world",
        "international": "international",
        "war": "war",
        "ukraine": "Ukraine",
        "russia": "Russia",
        "china": "China",
        "india": "India",
        "usa": "USA",
        "us": "United States",
    }

    return topic_map.get(topic, topic)


def execute(arguments: dict):

    topic = arguments.get("topic")

    if not topic:
        return "News Error: Topic not provided."

    topic = clean_topic(topic)

    try:

        from_date = (
            datetime.utcnow() - timedelta(days=7)
        ).strftime("%Y-%m-%d")

        params = {
            "q": topic,
            "from": from_date,
            "language": "en",
            "pageSize": 10,
            "sortBy": "publishedAt",
            "searchIn": "title,description,content",
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

        total = data.get("totalResults", len(articles))
        result = f"📰 Latest News on '{topic}' ({min(10, total)} of {total} results)\n"
        result += "=" * 60 + "\n\n"

        for i, article in enumerate(articles, start=1):

            title   = article.get("title", "No Title")
            description = article.get("description") or "No description available."
            content = article.get("content") or ""
            source  = article.get("source", {}).get("name", "Unknown")
            author  = article.get("author") or "Unknown Author"
            url     = article.get("url", "")
            published = article.get("publishedAt", "")

            if published:
                try:
                    published = datetime.strptime(
                        published,
                        "%Y-%m-%dT%H:%M:%SZ"
                    ).strftime("%d-%m-%Y %I:%M %p")
                except ValueError:
                    pass

            # Clean content — remove truncation marker like "[+1234 chars]"
            if content:
                content = content.split("[+")[0].strip()

            result += f"{i}. {title}\n"
            result += f"   🗞️  Source   : {source}\n"
            result += f"   ✍️  Author   : {author}\n"
            result += f"   🕒 Published: {published}\n"
            result += f"\n   📝 Description:\n   {description}\n"
            if content and content != description:
                result += f"\n   📄 Content:\n   {content}\n"
            if url:
                result += f"\n   🔗 Read More: {url}\n"
            result += "\n" + "-" * 60 + "\n\n"

        return result.strip()

    except requests.exceptions.RequestException as e:
        return f"News Request Error: {e}"

    except Exception as e:
        return f"News Error: {e}"


if __name__ == "__main__":
    print(execute({"topic": "Lionel Messi"}))