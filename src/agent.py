
class SecurityAgent:

    def __init__(self):
        self.name = "AgentSec"

    def process_message(self, message):
        message = message.strip()

        if message.lower() == "hello":
            return "Hello! I am AgentSec, your AI security assistant."

        elif message.lower() == "help":
            return (
                "Available commands:\n"
                "hello - Greet the agent\n"
                "help - Show available commands\n"
                "status - Check agent status\n"
                "exit - Close the agent"
            )

        elif message.lower() == "status":
            return "AgentSec is running successfully."

        else:
           return "Unknown command. Type 'help' for assistance."
