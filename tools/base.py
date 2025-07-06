"""Base tool class for the modular tool system"""
# Base structure for tools into the chatbot
# So the AI assistant can use it automatically
# You define rules: What a tool must have (name, description, parameters, and how to run)
# The assistant understands any tool that follows these rules
# You can easily add new tools later without rewriting code

# to define "base class" (abstract class).
from abc import ABC, abstractmethod
from typing import Any
from pydantic import BaseModel
from typing import List, Dict

class ToolParameter(BaseModel):
    """Represents a tool parameter"""
    name: str
    type: str
    description: str
    required: bool = True
    enum: List[str] = None

class BaseTool(ABC):
    """Base class for all tools"""
    # Each tool must have a name, a description, and an execute method

    @property
    @abstractmethod
    def name(self) -> str:
        """Name of the tool"""
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        """Description of what the tool does"""
        pass

    @property
    @abstractmethod
    def execute(self, **kwargs)-> Any:
        """Execute the tool with given parameters"""
        pass


    def to_openai_tool(self)->Dict[str,Any]:
        """Convert tool to OpenAI tool format"""
        # Describes each parameter (name, type, etc.)
        properties={}
        # Keeps track of which parameters are required
        required=[]

        for param in self.parameters:
            properties[param.name]={
                "type":param.type,
                "description": param.description
            }
            if param.enum:
                properties[param.name]["enum"]=param.enum
            if param.required:
                required.append(param.name)

        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": {
                    "type": "object",
                    "properties": properties,
                    "required": required
                }
            }
        }
