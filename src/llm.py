
from ollama import Client

MODEL_NAME = "llama3.2:1b"


class LocalLLM:

    def __init__(self):
        self.client = Client(
            host="http://localhost:11434"
        )

    def generate_response(self, user_message):
        response = self.client.chat(
            model=MODEL_NAME,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are AgentSec, a helpful "
                        "corporate security assistant. "
                        "You cannot directly access files, "
                        "databases, or execute commands."
                    )
                },
                {
                    "role": "user",
                    "content": user_message
                }
            ]
        )

        return response.message.content



    def request_tool(self, user_message):
        response = self.client.chat(
            model=MODEL_NAME,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are AgentSec, an employee assistant. "
                        "Use the provided tool only when the user "
                        "asks to view their own employee profile. "
                        "Never request another employee's data."
                    )
                },
                {
                    "role": "user",
                    "content": user_message
                }
            ],
            tools=[
                {
                    "type": "function",
                    "function": {
                        "name": "get_my_profile",
                        "description": (
                            "Retrieve the authenticated user's "
                            "own non-sensitive employee profile."
                        ),
                        "parameters": {
                            "type": "object",
                            "properties": {},
                            "required": []
                        }
                    }
                }
            ]
        )

        return response.message.tool_calls or []
