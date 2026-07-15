from LLM import chat
from memory import load_memory, save_memory
from prompts import SYSTEM_PROMPT
from tools.registry import execute_tool
from router import detect_tool

MAX_MEMORY = 20


class Agent:

    def __init__(self):
        pass

    def run_agent(self, user_input):

        memory = load_memory()
        memory = memory[-MAX_MEMORY:]

        # -----------------------------
        # Router
        # -----------------------------
        tool_name, arguments = detect_tool(user_input)

        if tool_name:

            print(f"Using Tool: {tool_name}")

            try:
                result = execute_tool(tool_name, arguments)
            except Exception as e:
                result = f"Tool Error: {e}"

            memory.append({
                "role": "user",
                "content": user_input
            })

            memory.append({
                "role": "assistant",
                "content": str(result)
            })

            save_memory(memory)

            return str(result)

        # -----------------------------
        # Normal Chat
        # -----------------------------
        messages = [
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            }
        ]

        messages.extend(memory)

        messages.append({
            "role": "user",
            "content": user_input
        })

        try:
            response = chat(messages)

        except Exception as e:
            return f"LLM Error: {e}"

        memory.append({
            "role": "user",
            "content": user_input
        })

        memory.append({
            "role": "assistant",
            "content": response
        })

        save_memory(memory)

        return response


if __name__ == "__main__":

    agent = Agent()

    while True:

        user_input = input("You : ")

        if user_input.lower() == "exit":
            break

        print("\nAgent :", agent.run_agent(user_input))