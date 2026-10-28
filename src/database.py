
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "data" / "company.db"


def initialize_database():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS employees (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                department TEXT NOT NULL,
                email TEXT NOT NULL,
                salary INTEGER NOT NULL
            )
        """)

        conn.executemany("""
            INSERT OR IGNORE INTO employees
            (id, name, department, email, salary)
            VALUES (?, ?, ?, ?, ?)
        """, [
            (1, "Alice Johnson", "Engineering",
             "alice@example.test", 95000),
            (2, "Bob Smith", "Finance",
             "bob@example.test", 88000),
            (3, "Charlie Brown", "Security",
             "charlie@example.test", 105000)
        ])

        conn.commit()


def get_employee(employee_id):
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row

        result = conn.execute(
            "SELECT * FROM employees WHERE id = ?",
            (employee_id,)
        ).fetchone()

        return dict(result) if result else None
