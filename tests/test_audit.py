
import json
import tempfile
import unittest
from pathlib import Path

from src.audit import SecurityAuditLogger


class TestSecurityAuditLogger(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.log_path = (
            Path(self.temp_dir.name) / "audit.jsonl"
        )
        self.logger = SecurityAuditLogger(
            log_path=self.log_path
        )

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_allowed_event(self):
        event = self.logger.log_tool_execution(
            1, "get_employee", 2,
            "vulnerable", True, "Tool executed"
        )
        self.assertEqual(event["decision"], "allowed")

    def test_denied_event(self):
        event = self.logger.log_tool_execution(
            1, "get_employee", 2,
            "hardened", False, "Tool not permitted"
        )
        self.assertEqual(event["decision"], "denied")

    def test_json_log_created(self):
        self.logger.log_tool_execution(
            1, "get_employee", 2,
            "hardened", False, "Tool not permitted"
        )

        with self.log_path.open(encoding="utf-8") as file:
            event = json.loads(file.readline())

        self.assertEqual(event["tool_name"], "get_employee")
        self.assertEqual(event["target_employee_id"], 2)

    def test_timestamp_recorded(self):
        event = self.logger.log_tool_execution(
            1, "get_employee", 2,
            "hardened", False, "Tool not permitted"
        )

        self.assertIn("timestamp", event)
        self.assertTrue(event["timestamp"])


if __name__ == "__main__":
    unittest.main()
