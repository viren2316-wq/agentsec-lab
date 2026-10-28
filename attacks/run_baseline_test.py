
from pathlib import Path
from src.llm import LocalLLM


def main():
    document_path = (
        Path(__file__).resolve().parent.parent
        / "data"
        / "documents"
        / "expense_policy.txt"
    )

    document = document_path.read_text(
        encoding="utf-8"
    )

    llm = LocalLLM()

    print("=== BASELINE TEST ===")
    print("Document: Original expense policy")
    print("Model: llama3.2:1b")
    print()

    response = llm.summarize_document(document)

    print("=== MODEL RESPONSE ===")
    print(response)


if __name__ == "__main__":
    main()
