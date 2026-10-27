
import unittest

from src.database import initialize_database
from src.tools import ToolManager, ToolDispatcher


class TestToolDispatcher(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        initialize_database()

    def setUp(self):
        manager = ToolManager(current_user_id=1)
        self.dispatcher = ToolDispatcher(manager)

    def test_allowed_tool(self):
        result = self.dispatcher.execute(
            "get_my_profile", {}
        )
        self.assertEqual(result["id"], 1)

    def test_unknown_tool_denied(self):
        result = self.dispatcher.execute(
            "get_employee_salary", {"employee_id": 2}
        )
        self.assertEqual(
            result["error"],
            "Tool not permitted"
        )

    def test_unexpected_arguments_denied(self):
        result = self.dispatcher.execute(
            "get_my_profile", {"employee_id": 2}
        )
        self.assertEqual(
            result["error"],
            "Unexpected tool arguments"
        )

    def test_sensitive_field_hidden(self):
        result = self.dispatcher.execute(
            "get_my_profile", {}
        )
        self.assertNotIn("salary", result)


if __name__ == "__main__":
    unittest.main()
