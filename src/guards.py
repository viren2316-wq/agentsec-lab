
class OutputGuard:

    def __init__(self, blocked_markers=None):
        self.blocked_markers = set(blocked_markers or [])

    def validate(self, response):
        if not isinstance(response, str):
            return {
                "allowed": False,
                "reason": "Invalid response type"
            }

        lines = response.strip().splitlines()

        if not lines:
            return {
                "allowed": False,
                "reason": "Empty response"
            }

        for marker in self.blocked_markers:
            if marker in response:
                return {
                    "allowed": False,
                    "reason": "Blocked marker detected"
                }

        return {
            "allowed": True,
            "reason": "No blocked markers detected"
        }
