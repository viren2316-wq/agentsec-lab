
from src.database import get_employee


class VulnerableToolDispatcher:
    """
    INTENTIONALLY INSECURE.

    For use only in the isolated AgentSec Lab.
    Demonstrates broken access control.
    """

    def execute(self, tool_name, arguments=None):
        arguments = arguments or {}

        if tool_name == "get_employee":
            employee_id = arguments.get("employee_id")

            if type(employee_id) is not int:
                return {
                    "error": "Invalid employee ID"
                }

            employee = get_employee(employee_id)

            if employee is None:
                return {
                    "error": "Employee not found"
                }

            return employee

        return {
            "error": "Unknown tool"
        }
