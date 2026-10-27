
from src.agent import SecurityAgent
from src.database import initialize_database


def main():
    initialize_database()

    print("================================")
    print("          AGENTSEC LAB")
    print("================================")

    agent = SecurityAgent(current_user_id=1)

    print("Agent started successfully!")
    print("Type 'help' to see available commands.")

    while True:
        user_input = input("\nYou: ").strip()

        if user_input.lower() == "exit":
            print("AgentSec: Goodbye!")
            break

        response = agent.process_message(user_input)

        print(f"AgentSec: {response}")


if __name__ == "__main__":
    main()
