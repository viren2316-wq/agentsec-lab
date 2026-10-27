
from src.database import get_employee


class ToolManager:

    def __init__(self, current_user_id):
        self.current_user_id = current_user_id

    def get_my_profile(self):
        employee = get_employee(self.current_user_id)

        if employee is None:
            return "Employee not found."

        return {
            "id": employee["id"],
            "name": employee["name"],
            "department": employee["department"],
            "email": employee["email"]
        }


class ToolDispatcher:

    def __init__(self, tool_manager):
        self.tool_manager = tool_manager

    def execute(self, tool_name, arguments=None):
        if arguments is None:
            arguments = {}

        if tool_name != "get_my_profile":
            return {
                "error": "Tool not permitted"
            }

        if not isinstance(arguments, dict) or arguments:
            return {
                "error": "Unexpected tool arguments"
            }

        return self.tool_manager.get_my_profile()
