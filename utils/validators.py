"""Validation utilities for the chatbot"""

import re
from typing import Optional

def validate_openai_key(api_key: str) -> bool:
    """Validate OpenAI API key format"""
    if not api_key:
        return False

    # OpenAI API key typically starts with 'sk-' and are followed by alphaneumeric characters
    pattern = r'^sk-[a-zA-Z0-9]{48}$'
    return bool(re.match(pattern, api_key))

def validate_model_name(model:str) -> bool:
    """Validate OpenAI model name."""
    valid_models = [
        "gpt-4", "gpt-4-turbo", "gpt-4-turbo-preview", "gpt-3.5-turbo", "gpt-3.5-turbo-16k"
    ]
    return model in valid_models

def validate_temperature(temperature: float) -> bool:
    """Validate temperature parameter."""
    return 0.0 <= temperature <= 2.0

def validate_max_tokens(max_tokens:int) -> bool:
    """Validate max_tokens parameter"""
    return 1 <= max_tokens <= 4096


