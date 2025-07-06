"""
Configuration management for the AI assistant project.
"""
import os
from dataclasses import dataclass
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv(override=True)

@dataclass
class Config:
    """Configuration for the chatbot"""
    openai_api_key: str
    model: str = "gpt-4o-mini"
    max_tokens: int=1000
    temperature: float=0.7
    system_prompt:str="You are a helpful assistant with access to tools."

    @classmethod
    def from_env(cls) -> "Config":
        """Create config from environment variables"""
        api_key=os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable is required")

        return cls(
            openai_api_key=api_key,
            max_tokens=int(os.getenv("MAX_TOKENS", "1000")),
            temperature=float(os.getenv("TEMPERATURE", "0.7")),
            system_prompt=os.getenv("SYSTEM_PROMPT", "You are a helpful assistant with access to tools.")
        )





