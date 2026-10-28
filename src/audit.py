
import json
from datetime import datetime, timezone
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_LOG_PATH = PROJECT_ROOT / "reports" / "audit_log.jsonl"


class SecurityAuditLogger:

    def __init__(self, log_path=None):
        self.log_path = Path(log_path or DEFAULT_LOG_PATH)
        self.log_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

    def log_tool_execution(
        self,
        user_id,
        tool_name,
        target_employee_id,
        configuration,
        allowed,
        reason
    ):
        event = {
            "timestamp": datetime.now(
                timezone.utc
            ).isoformat(),
            "event": "tool_execution",
            "user_id": user_id,
            "tool_name": tool_name,
            "target_employee_id": target_employee_id,
            "configuration": configuration,
            "decision": "allowed" if allowed else "denied",
            "reason": reason
        }

        with self.log_path.open(
            "a", encoding="utf-8"
        ) as file:
            file.write(json.dumps(event) + "\n")

        return event
