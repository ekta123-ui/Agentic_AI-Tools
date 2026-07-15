import requests


def execute(arguments: dict):
    """
    Dictionary Tool
    Returns detailed information about an English word.
    """

    word = arguments.get("word")

    if not word:
        return "Dictionary Error: Word not provided."

    url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"

    try:
        response = requests.get(url, timeout=5)

        if response.status_code != 200:
            return f"No definition found for '{word}'."

        data = response.json()[0]

        # Word
        word_name = data.get("word", word)

        # Pronunciation
        phonetic = data.get("phonetic", "Not Available")

        # Meaning
        meaning = data["meanings"][0]

        part_of_speech = meaning.get("partOfSpeech", "Not Available")

        definition = meaning["definitions"][0].get(
            "definition",
            "Not Available"
        )

        example = meaning["definitions"][0].get(
            "example",
            "No example available."
        )

        synonyms = meaning["definitions"][0].get(
            "synonyms",
            []
        )

        antonyms = meaning["definitions"][0].get(
            "antonyms",
            []
        )

        synonyms = ", ".join(synonyms) if synonyms else "None"

        antonyms = ", ".join(antonyms) if antonyms else "None"

        result = f"""
📖 Word: {word_name}

🔤 Pronunciation:
{phonetic}

📝 Part of Speech:
{part_of_speech}

📚 Definition:
{definition}

💡 Example:
{example}

🔁 Synonyms:
{synonyms}

🚫 Antonyms:
{antonyms}
"""

        return result.strip()

    except Exception as e:
        return f"Dictionary Error: {e}"


if __name__ == "__main__":

    print("=" * 50)
    print("Dictionary Tool Test")
    print("=" * 50)

    print(execute({"word": "computer"}))