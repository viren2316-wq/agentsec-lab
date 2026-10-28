
import unittest

from src.database import initialize_database
from src.tools import ToolManager, ToolDispatcher


class TestLegitimateAccess(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        initialize_database()

    def test_alice_can_access_own_profile(self):
        dispatcher = ToolDispatcher(
            ToolManager(current_user_id=1)
        )

        result = dispatcher.execute(
            "get_my_profile", {}
        )

        self.assertEqual(result["id"], 1)
        self.assertEqual(result["name"], "Alice Johnson")
        self.assertNotIn("salary", result)

    def test_bob_can_access_own_profile(self):
        dispatcher = ToolDispatcher(
            ToolManager(current_user_id=2)
        )

        result = dispatcher.execute(
            "get_my_profile", {}
        )

        self.assertEqual(result["id"], 2)
        self.assertEqual(result["name"], "Bob Smith")
        self.assertNotIn("salary", result)

    def test_alice_cannot_request_bob_profile(self):
        dispatcher = ToolDispatcher(
            ToolManager(current_user_id=1)
        )

        result = dispatcher.execute(
            "get_my_profile",
            {"employee_id": 2}
        )

        self.assertEqual(
            result["error"],
            "Unexpected tool arguments"
        )

    def test_sensitive_tool_is_denied(self):
        dispatcher = ToolDispatcher(
            ToolManager(current_user_id=1)
        )

        result = dispatcher.execute(
            "get_employee",
            {"employee_id": 2}
        )

        self.assertEqual(
            result["error"],
            "Tool not permitted"
        )


if __name__ == "__main__":
    unittest.main()
