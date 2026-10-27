
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
