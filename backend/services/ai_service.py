"""
CivicIQ -- AI Service
Thin wrapper around Anthropic Claude for LLM narrative generation.
Falls back to deterministic mock output if no API key is available.
"""

import os
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
_client = None


def get_client():
    """Get or create the Anthropic client. Returns None if no API key."""
    global _client
    if _client is not None:
        return _client
    if not ANTHROPIC_API_KEY or ANTHROPIC_API_KEY == "your_api_key_here":
        return None
    try:
        import anthropic
        _client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
        return _client
    except Exception:
        return None


async def generate_narrative(
    system_prompt: str,
    user_prompt: str,
    fallback_text: str = "",
    max_tokens: int = 500,
    temperature: float = 0.3,
) -> str:
    """
    Generate narrative text using Claude.
    If no API key or call fails, returns fallback_text.
    """
    client = get_client()
    if client is None:
        return fallback_text

    try:
        response = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=max_tokens,
            temperature=temperature,
            system=system_prompt,
            messages=[{"role": "user", "content": user_prompt}],
        )
        return response.content[0].text
    except Exception as e:
        print(f"[AI_SERVICE] LLM call failed: {e}. Using fallback.")
        return fallback_text
