
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
