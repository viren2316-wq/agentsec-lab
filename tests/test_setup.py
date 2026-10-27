
import unittest
from src.agent import SecurityAgent


class TestSecurityAgent(unittest.TestCase):

    def setUp(self):
        self.agent = SecurityAgent()

    def test_hello(self):
        response = self.agent.process_message("hello")
        self.assertIn("Hello", response)

    def test_status(self):
        response = self.agent.process_message("status")
        self.assertEqual(
            response,
            "AgentSec is running successfully."
        )

    def test_unknown_command(self):
        response = self.agent.process_message("invalid")
        self.assertIn("Unknown command", response)


if __name__ == "__main__":
    unittest.main()
