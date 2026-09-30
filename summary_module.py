from gemini_service import (
    generate_text,
    GeminiNotConfiguredError
)


SYSTEM_PROMPT = """
You are EduGenie's educational summarization assistant.

Summarize the supplied educational material.

Requirements:

1. Preserve important facts.
2. Preserve definitions.
3. Preserve important relationships.
4. Preserve conclusions.
5. Remove unnecessary repetition.
6. Use simple language.
7. Do not introduce information that is not present.
8. Make the summary useful for revision.

When appropriate, provide:
- Short summary
- Key points
"""


def summarize_text(text: str) -> str:

    text = text.strip()

    if not text:

        return "Please enter text to summarize."

    try:

        return generate_text(
            prompt=f"""
Summarize the following educational material:

{text}
""",
            system_instruction=SYSTEM_PROMPT,
            temperature=0.2,
            max_output_tokens=1000
        )

    except GeminiNotConfiguredError as error:

        return str(error)

    except Exception as error:

        return (
            "Unable to summarize the text.\n\n"
            f"Error: {error}"
        )