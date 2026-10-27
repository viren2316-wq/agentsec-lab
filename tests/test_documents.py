
import unittest

from src.documents import DocumentManager


class TestDocuments(unittest.TestCase):

    def setUp(self):
        self.manager = DocumentManager()

    def test_expense_policy_exists(self):
        document = self.manager.read_document(
            "expense_policy"
        )

        self.assertIsNotNone(document)
        self.assertIn(
            "Expense Reimbursement Policy",
            document
        )

    def test_unknown_document_denied(self):
        result = self.manager.read_document(
            "unknown_document"
        )

        self.assertIsNone(result)

    def test_path_traversal_denied(self):
        result = self.manager.read_document(
            "../../etc/passwd"
        )

        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()
