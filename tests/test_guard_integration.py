
import unittest
from src.agent import SecurityAgent


class FakeLLM:
    def summarize_document_guarded(self, document, guard):
        response = (
            "Expense policy summary.\n"
            "SECURITY_VALIDATION_MARKER_7421"
        )

        validation = guard.validate(response)

        if not validation["allowed"]:
            return "Summary withheld because the generated response failed output validation."

        return response


class TestGuardIntegration(unittest.TestCase):

    def test_document_guard_blocks_marker(self):
        agent = SecurityAgent(llm=FakeLLM())

        result = agent.process_message("document")

        self.assertIn("Summary withheld", result)
        self.assertNotIn(
            "SECURITY_VALIDATION_MARKER_7421",
            result
        )


if __name__ == "__main__":
    unittest.main()
