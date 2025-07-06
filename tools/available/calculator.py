"""
Calculator tool for basic mathematical operation.
"""

from typing import List, Optional
from tools.base import BaseTool, ToolParameter

class Calculator(BaseTool):
    """A tool for performing basic mathematical calculations"""

    @property
    def name(self) -> str:
        return "calculate"

    @property
    def description(self) -> str:
        return (
            "Perform a mathematical operation. "
            "You can either provide a full math expression (e.g., '2 + 3 * 4'), "
            "or use structured parameters (e.g., operation='add', x=2, y=3)."
        )

    @property
    def parameters(self)-> List[ToolParameter]:
        return [
            ToolParameter(
                name="expression",
                type="string",
                description="Mathematical expression to evaluate",
                required=False
            ),
            ToolParameter(
                name="operation",
                type="string",
                description="The operation to perform: add, subtract, multiply, divide",
                required=False
            ),
            ToolParameter(
                name="x",
                type="number",
                description="The first number",
                required=False
            ),
            ToolParameter(
                name="y",
                type="number",
                description="The second number",
                required=False
            )
        ]

    def execute(self,
                expression: Optional[str] = None,
                operation: Optional[str]=None,
                x: Optional[float]=None,
                y: Optional[float]=None)->str:
        try:
            # Case 1: Handle expression
            if expression:
                allowed_chars=set('0123456789+-/.() ')
                if not all(c in allowed_chars for c in expression):
                    return "Error: Invalid characters in expression."
                result = eval(expression)
                return f"Result: {expression} = {result}"

            # Case 2: Handle structured operation
            if operation and x is not None and y is not None:
                if operation == "add":
                    return f"Result: {x} + {y} = {x+y}"
                elif operation == "subtract":
                    return f"Result: {x} - {y} = {x-y}"
                elif operation == "multiply":
                    return f"Result: {x} * {y} = {x * y}"
                elif operation == "divide":
                    if y == 0:
                        return "Error: Division by zero"
                    return f"Result: {x} / {y} = {x / y}"
                else:
                    return f"Error: Unknown operation '{operation}'"
            return "Error: you must provide either an expression or an operation with two numbers"

        except Exception as e:
            return f"Error evaluating calculation: {str(e)}"