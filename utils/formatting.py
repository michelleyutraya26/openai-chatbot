"""
Rich formatting utilities for the chatbot.
"""

from typing import Any
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.syntax import Syntax
from rich.text import Text
from rich.table import Table

console = Console()

def format_message(role: str, content: str)->None:
    """Format and print a chat message"""
    # Displays a chat message with styled panels
    if role == "user":
        panel = Panel(
            content,
            title="[bold blue]You[/bold blue]",
            border_style="blue",
            padding=(0,1)
        )
    elif role == "assistant":
        # Try to render as markdown
        try:
            markdown = Markdown(content)
            panel = Panel(
                markdown,
                title="[bold green]Assistant[/bold green]",
                border_style="green",
                padding=(0,1)
            )
        except:
            panel = Panel(
                content,
                title="[bold green]Assistant[/bold green]",
                border_style="green",
                padding=(0,1)
            )
    elif role == "system":
        panel = Panel(
            content,
            title="[bold yellow]System[/bold yellow]",
            border_style="yellow",
            padding=(0,1)
            )
    else:
        panel = Panel(content, title=f"[bold]{role}[/bold]", padding=(0,1))

    console.print(panel)

def format_error(error: str) -> None:
    """Format and print an error message"""
    console.print(f"[bold red]Error:[/bold red] {error}")

def format_tool_call(tool_name: str, arguments: dict) -> None:
    """Format and print a tool call"""
    # SHows when a tool is being called, with its inputs
    table = Table(title=f"Calling tool: {tool_name}")
    table.add_column("Parameter", style="cyan")
    table.add_column("Value", style="green")

    for key, value in arguments.items():
        table.add_row(key, str(value))

    console.print(table)

def format_tool_result(tool_name: str, result: Any) -> None:
    """Format and print a tool result"""
    # Displays the output/result of the tool
    panel=Panel(
        str(result),
        title=f"[bold cyan]Tool Result: {tool_name}[/bold cyan]",
        border_style="cyan",
        padding=(0,1)
    )
    console.print(panel)


def format_welcome() -> None:
    """Format and print the welcome message."""
    welcome_text = Text.from_markup(
        """[bold blue]🤖 CLI Chatbot[/bold blue]

Connected to OpenAI with tool support!
Type your message or 'quit' to exit.
Use 'help' to see available commands."""
    )

    panel = Panel(
        welcome_text,
        title="[bold green]Welcome[/bold green]",
        border_style="green",
        padding=(1, 2)
    )
    console.print(panel)


def format_help(tools: list) -> None:
    """Format and print help information."""
    help_text = """Available commands:
• quit/exit - Exit the chatbot
• help - Show this help message
• tools - List available tools

Available tools:"""

    if tools:
        for tool in tools:
            help_text += f"\n• {tool}"
    else:
        help_text += "\n• No tools registered"

    panel = Panel(
        help_text,
        title="[bold yellow]Help[/bold yellow]",
        border_style="yellow",
        padding=(0, 1)
    )
    console.print(panel)