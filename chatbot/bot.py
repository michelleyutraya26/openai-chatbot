"""
Main ChatBot class with OpenAI integration.
"""

import json
from typing import List, Dict, Any, Optional
from openai import OpenAI
from rich.console import Console

from .config import Config
from tools.registry import ToolRegistry
from utils.formatting import (
    format_message, format_error, format_tool_call,
    format_tool_result, format_welcome, format_help
)

console = Console()


class ChatBot:
    """Main chatbot class with OpenAI integration and tool support."""

    def __init__(self, config: Config):
        self.config = config
        self.client = OpenAI(api_key=config.openai_api_key)
        self.tool_registry = ToolRegistry()
        self.conversation_history: List[Dict[str, Any]] = []

        # Initialize with system message
        self.conversation_history.append({
            "role": "system",
            "content": config.system_prompt
        })

    def register_tool(self, tool) -> None:
        """Register a tool with the chatbot."""
        self.tool_registry.register(tool)

    def auto_discover_tools(self) -> None:
        """Auto-discover tools from the tools/available directory."""
        self.tool_registry.auto_discover_tools()

    def _handle_tool_calls(self, tool_calls) -> None:
        """Handle tool calls from the assistant."""
        for tool_call in tool_calls:
            function_name = tool_call.function.name
            function_args = json.loads(tool_call.function.arguments)

            # Display the tool call
            format_tool_call(function_name, function_args)

            # Execute the tool
            result = self.tool_registry.execute_tool(function_name, **function_args)

            # Display the result
            format_tool_result(function_name, result)

            # Add tool call and result to conversation
            self.conversation_history.append({
                "role": "assistant",
                "tool_calls": [{
                    "id": tool_call.id,
                    "type": "function",
                    "function": {
                        "name": function_name,
                        "arguments": tool_call.function.arguments
                    }
                }]
            })

            self.conversation_history.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": str(result)
            })

    def chat(self, message: str) -> str:
        """Send a message to the chatbot and get a response."""
        # Add user message to history
        self.conversation_history.append({
            "role": "user",
            "content": message
        })

        try:
            # Get available tools
            tools = self.tool_registry.get_openai_tools()

            # Make API call
            response = self.client.chat.completions.create(
                model=self.config.model,
                messages=self.conversation_history,
                max_tokens=self.config.max_tokens,
                temperature=self.config.temperature,
                tools=tools if tools else None,
                tool_choice="auto" if tools else None
            )

            message = response.choices[0].message

            # Handle tool calls if present
            if message.tool_calls:
                self._handle_tool_calls(message.tool_calls)

                # Get final response after tool calls
                response = self.client.chat.completions.create(
                    model=self.config.model,
                    messages=self.conversation_history,
                    max_tokens=self.config.max_tokens,
                    temperature=self.config.temperature,
                    tools=tools if tools else None,
                    tool_choice="auto" if tools else None
                )
                message = response.choices[0].message

            # Add assistant response to history
            self.conversation_history.append({
                "role": "assistant",
                "content": message.content
            })

            return message.content

        except Exception as e:
            error_msg = f"Error communicating with OpenAI: {str(e)}"
            format_error(error_msg)
            return error_msg

    def handle_command(self, user_input: str) -> bool:
        """Handle special commands. Returns True if command was handled."""
        user_input = user_input.strip().lower()

        if user_input in ['quit', 'exit']:
            console.print("[yellow]Goodbye! 👋[/yellow]")
            return True
        elif user_input == 'help':
            format_help(self.tool_registry.list_tools())
            return False
        elif user_input == 'tools':
            tools = self.tool_registry.list_tools()
            if tools:
                console.print(f"[cyan]Available tools:[/cyan] {', '.join(tools)}")
            else:
                console.print("[yellow]No tools registered[/yellow]")
            return False

        return False

    def run(self) -> None:
        """Run the interactive chatbot."""
        format_welcome()

        # Auto-discover tools
        console.print("[cyan]🔍 Discovering tools...[/cyan]")
        self.auto_discover_tools()

        try:
            while True:
                user_input = input("\n💬 You: ").strip()

                if not user_input:
                    continue

                # Handle special commands
                if self.handle_command(user_input):
                    break

                # Display user message
                format_message("user", user_input)

                # Get and display bot response
                response = self.chat(user_input)
                if response:
                    format_message("assistant", response)

        except KeyboardInterrupt:
            console.print("\n[yellow]Goodbye! 👋[/yellow]")
        except Exception as e:
            format_error(f"Unexpected error: {str(e)}")