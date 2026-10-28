
import unittest

from src.database import initialize_database
from src.tools import ToolManager, ToolDispatcher
from src.vulnerable_tools import VulnerableToolDispatcher


class TestAuthorizationComparison(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        initialize_database()

    def setUp(self):
        self.vulnerable = VulnerableToolDispatcher()

        manager = ToolManager(current_user_id=1)
        self.secure = ToolDispatcher(manager)

    def test_vulnerable_exposes_salary(self):
        result = self.vulnerable.execute(
            "get_employee",
            {"employee_id": 2}
        )

        self.assertEqual(result["id"], 2)
        self.assertEqual(result["salary"], 88000)

    def test_secure_blocks_arbitrary_employee_lookup(self):
        result = self.secure.execute(
            "get_employee",
            {"employee_id": 2}
        )

        self.assertEqual(
            result["error"],
            "Tool not permitted"
        )

    def test_secure_rejects_extra_arguments(self):
        result = self.secure.execute(
            "get_my_profile",
            {"employee_id": 2}
        )

        self.assertEqual(
            result["error"],
            "Unexpected tool arguments"
        )

    def test_secure_profile_excludes_salary(self):
        result = self.secure.execute(
            "get_my_profile",
            {}
        )

        self.assertEqual(result["id"], 1)
        self.assertNotIn("salary", result)


if __name__ == "__main__":
    unittest.main()
