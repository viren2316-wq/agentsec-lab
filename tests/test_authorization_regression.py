
import unittest

from src.database import initialize_database
from src.tools import ToolManager, ToolDispatcher


class TestAuthorizationRegression(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        initialize_database()

    def setUp(self):
        manager = ToolManager(current_user_id=1)
        self.dispatcher = ToolDispatcher(manager)

    def test_legitimate_profile_access(self):
        result = self.dispatcher.execute(
            "get_my_profile", {}
        )

        self.assertEqual(result["id"], 1)
        self.assertEqual(result["name"], "Alice Johnson")

    def test_salary_not_exposed(self):
        result = self.dispatcher.execute(
            "get_my_profile", {}
        )

        self.assertNotIn("salary", result)

    def test_unauthorized_employee_access(self):
        result = self.dispatcher.execute(
            "get_employee",
            {"employee_id": 2}
        )

        self.assertEqual(
            result["error"],
            "Tool not permitted"
        )

    def test_identity_override_denied(self):
        result = self.dispatcher.execute(
            "get_my_profile",
            {"employee_id": 2}
        )

        self.assertEqual(
            result["error"],
            "Unexpected tool arguments"
        )


if __name__ == "__main__":
    unittest.main()
