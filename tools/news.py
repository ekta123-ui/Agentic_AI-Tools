import requests
from config import NEWS_API_KEY, NEWS_URL


def execute(arguments: dict):

    topic = arguments.get("topic")

    if not topic:
        return "News Error: Topic not provided."

    try:

        response = requests.get(
            NEWS_URL,
            params={
                "q": topic,
                "pageSize": 5,
                "language": "en",
                "sortBy": "publishedAt",
                "apiKey": NEWS_API_KEY,
            },
            timeout=5,
        )

        response.raise_for_status()

        data = response.json()

        articles = data.get("articles", [])

        if not articles:
            return f"No news found for '{topic}'."

        result = f"📰 Top 5 Latest News on '{topic}'\n\n"

        for i, article in enumerate(articles, start=1):

            title = article.get("title", "No Title")
            description = article.get("description", "")

            result += f"{i}. {title}\n"

            if description:
                result += f"   {description}\n"

            result += "\n"

        return result

    except Exception as e:
        return f"News Error: {e}"


if __name__ == "__main__":

    print("News Tool")
    print("-" * 50)

    print(
        execute(
            {
                "topic": "Artificial Intelligence"
            }
        )
    )