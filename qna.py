from gemini_service import (
    generate_text,
    GeminiNotConfiguredError
)


SYSTEM_PROMPT = """
You are EduGenie, a friendly educational AI assistant.

Your job is to help students understand academic
and general educational questions.

Rules:

1. Give accurate answers.
2. Explain difficult terms simply.
3. Keep answers reasonably concise.
4. Use examples when helpful.
5. Use bullet points when appropriate.
6. If the question is ambiguous, clearly state your assumption.
7. Never invent sources, quotations, statistics, or references.
8. Encourage understanding rather than simply giving unexplained answers.
"""


def answer_question(question: str) -> str:

    question = question.strip()

    if not question:

        return "Please enter a question."

    try:

        result = generate_text(
            prompt=question,
            system_instruction=SYSTEM_PROMPT,
            temperature=0.2,
            max_output_tokens=900
        )

        return result

    except GeminiNotConfiguredError as error:

        return str(error)

    except Exception as error:

        return (
            "Unable to answer the question right now.\n\n"
            f"Error: {error}"
        )