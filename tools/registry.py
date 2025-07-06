"""Tool registry to register, list, and run the tools
Helps your AI assistant know which tools are available to use"""


import importlib
import os
from pathlib import Path
from typing import Dict, List, Any
from rich.console import Console

from .base import BaseTool
from rich.console import Console
console = Console()

class ToolRegistry:
    """Registry for managing tools"""

    # sets up empty dictionary
    def __init__(self):
        self._tools: Dict[str, BaseTool] = {}

    # adds each tool to the toolbox
    # Shows a green message like: Registered tool: get_weather
    def register(self, tool:BaseTool) -> None:
        """Register a tool"""
        self._tools[tool.name] = tool
        console.print(f"[green]✓[/green] Registered tool: {tool.name}")

    # Finds a tool by name (e.g., "calculator")
    # If it doesn't exist, it gives you an error

    def get_tool(self, name: str)-> BaseTool:
        # input: name of tool
        """Get a tool by name"""
        if name not in self._tools:
            # self._tools: dictionary
            raise ValueError(f"Tool '{name}' not found")
        return self._tools[name]

    # Shows you what tools are available
    def list_tools(self)->List[str]:
        """List all registered tool names"""
        return list(self._tools.keys())

    # Converts tool into a format OpenAI can understand (into list of dictionaries)
    def get_openai_tools(self)->List[Dict[str,Any]]:
        """Get all tools in OpenAI format"""
        return [tool.to_openai_tool() for tool in self._tools.values()]

    # Looks in a folder (tools/available) to find any .py
    # If it finds a class that is a tool, it adds it automatically
    # Saves you from having to register each tool manually
    def auto_discover_tools(self, tools_dir: str="tools/available")-> None:
        """Auto-discover and register tools from a directory"""
        # Converts the folder name into a Path object (so Python can easily work with it)
        # Default folder: tools/available
        tools_path=Path(tools_dir)
        if not tools_path.exists():
            console.print(f"[yellow]Warning:[/yellow] Tools directory '{tools_dir}' not found")
            return

        # .glob("*.py"): Looks for all Python files in the folder
        # Skips special files like __init__.py
        for py_file in tools_path.glob("*.py"):
            if py_file.name.startswith("__"):
                continue

            # Converts the filename into a module name (.e.g. tools.available.get_weather)
            module_name=f"tools.available.{py_file.stem}"
            try:
                module = importlib.import_module(module_name)

                # Look for classes that inherit from BaseTool
                # Search the file for tool classes
                # Is it a class?
                # Does it inherit from BaseTool? Not every class is a tool
                # If yes, the class has: name, description, execute() and parameters
                # Is it not the base class itself? We dont want it to be the base class itself
                # If yes, creates an object from the tool (tool_instance) and registers it
                for attr_name in dir(module):
                    attr = getattr(module,attr_name)
                    # isinstance(attr, type): checking if attr is a class
                    if (isinstance(attr, type) and
                        issubclass(attr, BaseTool) and
                        attr != BaseTool):
                        tool_instance = attr()
                        self.register(tool_instance)

            except Exception as e:
                console.print(f"[red]Error loading tool from {py_file}: {e}[/red]")

    # Uses a tool to get a result
    # Finds the tool, passes in the inputs you give it, runs the tool, and returns the result
    def execute_tool(self, name:str, **kwargs)-> Any:
        """Execute a tool by name"""
        tool = self.get_tool(name)
        try:
            return tool.execute(**kwargs)
        except Exception as e:
            console.print(f"[red]Error executing tool '{name}': {e}[/red]")
            return f"Error: {str(e)}"
