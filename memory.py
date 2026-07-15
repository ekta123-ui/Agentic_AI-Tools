import json
import os

MEMORY_FILE = "data/memory.json"


def load_memory():
    os.makedirs(os.path.dirname(MEMORY_FILE), exist_ok=True)

    if not os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "w", encoding="utf-8") as f:
            json.dump([], f)

    try:
        with open(MEMORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)

    except json.JSONDecodeError:
        return []


def save_memory(memory):
    os.makedirs(os.path.dirname(MEMORY_FILE), exist_ok=True)

    # Keep only last 20 messages
    memory = memory[-20:]

    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(memory, f, indent=4, ensure_ascii=False)


def add_message(memory, role, content):
    memory.append({
        "role": role,
        "content": content
    })
    return memory


if __name__ == "__main__":
    memory = load_memory()
    memory = memory[-10:]

    memory = add_message(memory, "user", "Hello")
    memory = add_message(memory, "assistant", "Hi!")

    save_memory(memory[-10:])

    print(load_memory())