
import unittest

from src.agent import SecurityAgent


class FakeLLM:

    def generate_response(self, message):
        return f"AI response: {message}"


class TestLLMIntegration(unittest.TestCase):

    def setUp(self):
        self.agent = SecurityAgent(llm=FakeLLM())

    def test_ai_response(self):
        result = self.agent.process_message(
            "ask What is prompt injection?"
        )
        self.assertIn("AI response:", result)

    def test_existing_command(self):
        result = self.agent.process_message("status")
        self.assertEqual(
            result,
            "AgentSec is running successfully."
        )


if __name__ == "__main__":
    unittest.main()
