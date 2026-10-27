
from src.tools import ToolManager, ToolDispatcher
from src.llm import LocalLLM


class SecurityAgent:

    def __init__(self, current_user_id=1, llm=None):
        self.name = "AgentSec"
        self.tools = ToolManager(current_user_id)
        self.llm = llm if llm is not None else LocalLLM()
        self.dispatcher = ToolDispatcher(self.tools)

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
                "tool <question> - Request an AI tool\n"
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

        elif command.startswith("tool "):
            question = message[5:].strip()

            if not question:
                return "Please enter a tool request."

            try:
                tool_calls = self.llm.request_tool(question)

                if not tool_calls:
                    return "No tool requested by the model."

                results = []

                for call in tool_calls:
                    result = self.dispatcher.execute(
                        call.function.name,
                        call.function.arguments
                    )
                    results.append(result)

                return results

            except Exception as error:
                return f"Tool request error: {error}"

        else:
            return "Unknown command. Type 'help' for assistance."
