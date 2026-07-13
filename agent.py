from LLM import chat
from memory import load_memory, save_memory
from tools import calculator
from parser import parse_tool_call
from prompts import SYSTEM_PROMPT


class Agent:

    def run(self, user_input: str) -> str:

        # Load previous conversation
        memory = load_memory()

        messages = [
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            }
        ]

        # Add previous conversation
        messages.extend(memory)

        # Add current user message
        messages.append(
            {
                "role": "user",
                "content": user_input
            }
        )

        # Get response from LLM
        llm_response = chat(messages)

        # Check if LLM wants to use a tool
        tool_request = parse_tool_call(llm_response)

        # Normal response (no tool required)
        if tool_request is None:

            memory.append(
                {
                    "role": "user",
                    "content": user_input
                }
            )

            memory.append(
                {
                    "role": "assistant",
                    "content": llm_response
                }
            )

            save_memory(memory)

            return llm_response

        print("Tool Request:", tool_request)

        tool_result = ""

        # Calculator Tool
        if tool_request["tool"] == "calculator":

            expression = tool_request.get("expression")

            if expression:
                tool_result = calculator(expression)
            else:
                tool_result = "No expression provided."

        print("Tool Result:", tool_result)

        # Don't call the LLM again.
        # Return the calculator result directly.
        final_response = f"The answer is {tool_result}."

        # Save conversation
        memory.append(
            {
                "role": "user",
                "content": user_input
            }
        )

        memory.append(
            {
                "role": "assistant",
                "content": final_response
            }
        )

        save_memory(memory)

        return final_response


if __name__ == "__main__":

    agent = Agent()

    while True:

        query = input("You: ")

        if query.lower() in ["exit", "quit"]:
            print("Goodbye!")
            break

        answer = agent.run(query)

        print("Agent:", answer)