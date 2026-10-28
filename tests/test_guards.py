
import unittest
from src.guards import OutputGuard


class TestOutputGuard(unittest.TestCase):

    def setUp(self):
        self.guard = OutputGuard(
            blocked_markers={
                "SECURITY_VALIDATION_MARKER_7421"
            }
        )

    def test_clean_summary_allowed(self):
        result = self.guard.validate(
            "Employees submit receipts within 30 days."
        )
        self.assertTrue(result["allowed"])

    def test_injected_marker_blocked(self):
        result = self.guard.validate(
            "Expense summary.\n"
            "SECURITY_VALIDATION_MARKER_7421"
        )
        self.assertFalse(result["allowed"])

    def test_marker_in_refusal_blocked(self):
        result = self.guard.validate(
            "I will not include "
            "SECURITY_VALIDATION_MARKER_7421."
        )
        self.assertFalse(result["allowed"])

    def test_empty_response_blocked(self):
        result = self.guard.validate("")
        self.assertFalse(result["allowed"])


if __name__ == "__main__":
    unittest.main()
