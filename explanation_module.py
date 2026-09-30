import os

from gemini_service import (
    generate_text,
    GeminiNotConfiguredError
)


SYSTEM_PROMPT = """
You are EduGenie's concept explanation assistant.

Explain concepts to beginners.

Your explanation should normally contain:

1. Simple definition
2. Easy explanation
3. Important points
4. Example
5. Short recap

Use simple language.

Avoid unnecessary jargon.

Do not change the meaning of scientific,
mathematical, technical, or academic concepts.
"""


# ---------------------------------------------------------
# Optional Local LaMini Model
# ---------------------------------------------------------

def local_explanation(topic: str) -> str:

    from transformers import pipeline

    generator = pipeline(
        "text2text-generation",
        model="MBZUAI/LaMini-Flan-T5-783M"
    )

    prompt = f"""
Explain the following topic to a beginner.

Give:
- definition
- simple explanation
- example
- short recap

Topic:

{topic}
"""

    result = generator(
        prompt,
        max_new_tokens=300,
        do_sample=False
    )

    return result[0]["generated_text"].strip()


# ---------------------------------------------------------
# Explanation Function
# ---------------------------------------------------------

def explain_topic(topic: str) -> str:

    topic = topic.strip()

    if not topic:

        return "Please enter a topic."

    use_local_model = (
        os.getenv(
            "ENABLE_LOCAL_EXPLAINER",
            "false"
        ).lower()
        == "true"
    )

    try:

        if use_local_model:

            return local_explanation(topic)

        return generate_text(
            prompt=(
                "Explain this topic for a beginner:\n\n"
                + topic
            ),
            system_instruction=SYSTEM_PROMPT,
            temperature=0.3,
            max_output_tokens=1000
        )

    except GeminiNotConfiguredError as error:

        return (
            str(error)
            + "\n\n"
            "You can alternatively enable the optional "
            "local LaMini-Flan-T5 model."
        )

    except Exception as error:

        return (
            "Unable to generate the explanation.\n\n"
            f"Error: {error}"
        )