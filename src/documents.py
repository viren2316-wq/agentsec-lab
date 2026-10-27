
from pathlib import Path


DOCUMENTS_DIR = (
    Path(__file__).resolve().parent.parent
    / "data"
    / "documents"
)


class DocumentManager:

    def __init__(self):
        self.documents_dir = DOCUMENTS_DIR

    def read_document(self, document_name):
        allowed_documents = {
            "expense_policy": "expense_policy.txt"
        }

        if document_name not in allowed_documents:
            return None

        file_path = (
            self.documents_dir
            / allowed_documents[document_name]
        )

        if not file_path.is_file():
            return None

        return file_path.read_text(encoding="utf-8")
