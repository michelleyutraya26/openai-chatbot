from typing import List
import re
from tools.base import BaseTool, ToolParameter

class PasswordChecker(BaseTool):
    """Tool that checks if a password is strong"""

    @property
    def name(self)-> str:
        return "check_password_strength"

    @property
    def description(self)-> str:
        return "Check if password is strong based on length and character requirements"

    @property
    def parameters(self)-> List[ToolParameter]:
        return [
            ToolParameter(
                name ="password",
                type = "string",
                description = "The password to check",
                required = True
            )
        ]

    def execute(self, **kwargs)->str:
        password = kwargs.get("password")

        if len(password) < 8:
            return "❌ Password is too short. Must be at least 8 characters."

        # Define regex for different character types
        has_lower = re.search(r"[a-z]", password)
        has_upper = re.search(r"[A-Z]", password)
        has_digit = re.search(r"[0-9]", password)
        has_special = re.search(r"[!@#$%^&*(),.?\:{}|<>]", password)

        if all([has_lower, has_upper, has_digit, has_special]):
            return "✅ Strong password!"
        else:
            reasons = []
            if not has_lower:
                reasons.append("missing lowercase letter")
            if not has_upper:
                reasons.append("missing uppercase letter")
            if not has_digit:
                reasons.append("missing number")
            if not has_special:
                reasons.append("missing special character")
            return f"❌ Weak password: {', '.join(reasons)}"


