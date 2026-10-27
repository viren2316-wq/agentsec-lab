
import unittest

from src.database import initialize_database
from src.tools import ToolManager


class TestToolManager(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        initialize_database()

    def test_own_profile(self):
        tools = ToolManager(current_user_id=1)
        profile = tools.get_my_profile()

        self.assertEqual(profile["id"], 1)
        self.assertEqual(profile["name"], "Alice Johnson")

    def test_sensitive_salary_not_exposed(self):
        tools = ToolManager(current_user_id=1)
        profile = tools.get_my_profile()

        self.assertNotIn("salary", profile)

    def test_user_two_profile(self):
        tools = ToolManager(current_user_id=2)
        profile = tools.get_my_profile()

        self.assertEqual(profile["id"], 2)

    def test_unknown_user(self):
        tools = ToolManager(current_user_id=999)
        result = tools.get_my_profile()

        self.assertEqual(result, "Employee not found.")


if __name__ == "__main__":
    unittest.main()
