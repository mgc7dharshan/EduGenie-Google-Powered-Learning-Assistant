import json
import os
from typing import Any

from dotenv import load_dotenv
from google import genai
from google.genai import types


# Load environment variables
load_dotenv()


# ---------------------------------------------------------
# Configuration
# ---------------------------------------------------------

GEMINI_API_KEY = os.getenv(
    "GEMINI_API_KEY"
)

GEMINI_MODEL = os.getenv(
    "GEMINI_MODEL",
    "gemini-3.8-flash"
)


# ---------------------------------------------------------
# Gemini Client
# ---------------------------------------------------------

_client = None

if GEMINI_API_KEY:

    _client = genai.Client(
        api_key=GEMINI_API_KEY
    )


# ---------------------------------------------------------
# Custom Exception
# ---------------------------------------------------------

class GeminiNotConfiguredError(RuntimeError):

    pass


# ---------------------------------------------------------
# Get Client
# ---------------------------------------------------------

def get_client():

    if _client is None:

        raise GeminiNotConfiguredError(
            "GEMINI_API_KEY is not configured. "
            "Create a .env file and add your Gemini API key."
        )

    return _client


# ---------------------------------------------------------
# Generate Text
# ---------------------------------------------------------

def generate_text(
    prompt: str,
    system_instruction: str | None = None,
    temperature: float = 0.4,
    max_output_tokens: int = 1200
) -> str:

    client = get_client()

    config = types.GenerateContentConfig(
        temperature=temperature,
        max_output_tokens=max_output_tokens,
        system_instruction=system_instruction
    )

    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=prompt,
        config=config
    )

    text = getattr(
        response,
        "text",
        None
    )

    if not text:

        raise RuntimeError(
            "Gemini returned an empty response."
        )

    return text.strip()


# ---------------------------------------------------------
# Generate Structured JSON
# ---------------------------------------------------------

def generate_json(
    prompt: str,
    response_schema: Any,
    system_instruction: str | None = None,
    temperature: float = 0.3,
    max_output_tokens: int = 1800
):

    client = get_client()

    config = types.GenerateContentConfig(
        temperature=temperature,
        max_output_tokens=max_output_tokens,
        system_instruction=system_instruction,
        response_mime_type="application/json",
        response_schema=response_schema
    )

    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=prompt,
        config=config
    )

    parsed = getattr(
        response,
        "parsed",
        None
    )

    if parsed is not None:

        return parsed

    text = getattr(
        response,
        "text",
        None
    )

    if not text:

        raise RuntimeError(
            "Gemini returned no JSON response."
        )

    return json.loads(text)