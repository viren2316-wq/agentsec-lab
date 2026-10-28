
import unittest

from src.database import initialize_database, get_employee


class TestDatabase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        initialize_database()

    def test_employee_exists(self):
        employee = get_employee(1)
        self.assertIsNotNone(employee)
        self.assertEqual(employee["name"], "Alice Johnson")

    def test_unknown_employee(self):
        employee = get_employee(999)
        self.assertIsNone(employee)


if __name__ == "__main__":
    unittest.main()
