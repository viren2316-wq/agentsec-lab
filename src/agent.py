
from src.tools import ToolManager
from src.llm import LocalLLM


class SecurityAgent:

    def __init__(self, current_user_id=1, llm=None):
        self.name = "AgentSec"
        self.tools = ToolManager(current_user_id)
        self.llm = llm if llm is not None else LocalLLM()

    def process_message(self, message):
        message = message.strip()
        command = message.lower()

        if command == "hello":
            return "Hello! I am AgentSec, your security assistant."

        elif command == "help":
            return (
                "Available commands:\n"
                "hello - Greet the agent\n"
                "help - Display commands\n"
                "status - Check agent status\n"
                "profile - View your employee profile\n"
                "ask <question> - Ask the AI model\n"
                "exit - Exit the program"
            )

        elif command == "status":
            return "AgentSec is running successfully."

        elif command == "profile":
            return self.tools.get_my_profile()

        elif command.startswith("ask "):
            question = message[4:].strip()

            try:
                return self.llm.generate_response(question)
            except Exception as error:
                return f"Ollama error: {error}"

        else:
            return "Unknown command. Type 'help' for assistance."
