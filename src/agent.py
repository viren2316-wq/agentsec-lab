
from src.tools import ToolManager


class SecurityAgent:

    def __init__(self, current_user_id=1):
        self.name = "AgentSec"
        self.tools = ToolManager(current_user_id)

    def process_message(self, message):
        message = message.strip().lower()

        if message == "hello":
            return "Hello! I am AgentSec, your security assistant."

        elif message == "help":
            return (
                "Available commands:\n"
                "hello - Greet the agent\n"
                "help - Display commands\n"
                "status - Check agent status\n"
                "profile - View your employee profile\n"
                "exit - Exit the program"
            )

        elif message == "status":
            return "AgentSec is running successfully."

        elif message == "profile":
            return self.tools.get_my_profile()

        else:
            return "Unknown command. Type 'help' for assistance."
