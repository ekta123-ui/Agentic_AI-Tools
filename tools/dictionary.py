import requests


def execute(arguments: dict):
    word = arguments.get("word")

    if not word:
        return "Dictionary Error: Word not provided."

    url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"

    try:
        response = requests.get(url, timeout=5)

        if response.status_code != 200:
            return f"No definition found for '{word}'."

        entries = response.json()
        data = entries[0]

        word_name = data.get("word", word)
        phonetic = data.get("phonetic", "Not Available")

        result = f"📖 Word: {word_name}\n"
        result += f"🔤 Pronunciation: {phonetic}\n"

        all_synonyms = set()
        all_antonyms = set()

        for meaning in data.get("meanings", []):
            part_of_speech = meaning.get("partOfSpeech", "Not Available")
            result += f"\n📝 {part_of_speech.capitalize()}\n"

            for i, definition_entry in enumerate(
                meaning.get("definitions", [])[:3], start=1
            ):
                definition = definition_entry.get("definition", "Not Available")
                example = definition_entry.get("example")

                result += f"   {i}. {definition}\n"
                if example:
                    result += f"      e.g. \"{example}\"\n"

                all_synonyms.update(definition_entry.get("synonyms", []))
                all_antonyms.update(definition_entry.get("antonyms", []))

            all_synonyms.update(meaning.get("synonyms", []))
            all_antonyms.update(meaning.get("antonyms", []))

        result += f"\n🔁 Synonyms: {', '.join(all_synonyms) if all_synonyms else 'None'}\n"
        result += f"🚫 Antonyms: {', '.join(all_antonyms) if all_antonyms else 'None'}\n"

        return result.strip()

    except Exception as e:
        return f"Dictionary Error: {e}"


if __name__ == "__main__":
    print(execute({"word": "computer"}))