from agent import Agent


def main():
    print("=" * 60)
    print("AI AGENT")
    print("=" * 60)
    print("Type 'exit' to quit.")
    print()

    agent = Agent()

    while True:
        user_input = input("You: ").strip()

        # Skip empty input
        if not user_input:
            continue

        # Exit condition
        if user_input.lower() == "exit":
            print("Goodbye!")
            break

        try:
            response = agent.run(user_input)   # ✅ Fixed
            print("Agent:", response)

        except Exception as e:
            print("Error:", e)


if __name__ == "__main__":
    main()