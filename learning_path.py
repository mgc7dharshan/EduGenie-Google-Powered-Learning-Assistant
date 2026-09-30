from gemini_service import (
    generate_text,
    GeminiNotConfiguredError
)


SYSTEM_PROMPT = """
You are EduGenie's learning-path planner.

Create a personalized learning path for the
requested subject.

Organize the path from:

Beginner
    ↓
Intermediate
    ↓
Advanced

For each stage include:

- Topics
- Recommended order
- Approximate timeline
- Practice activities
- What the learner should know before moving forward

Also recommend useful resource TYPES such as:

- official documentation
- books
- courses
- videos
- tutorials
- practice projects

Do not invent specific URLs.

Keep the learning path practical and adaptable.
"""


def get_learning_recommendations(
    topic: str
) -> str:

    topic = topic.strip()

    if not topic:

        return "Please enter a topic."

    try:

        return generate_text(
            prompt=f"""
Create a beginner-to-advanced learning path
for the following topic:

{topic}
""",
            system_instruction=SYSTEM_PROMPT,
            temperature=0.5,
            max_output_tokens=1500
        )

    except GeminiNotConfiguredError as error:

        return str(error)

    except Exception as error:

        return (
            "Unable to generate a learning path.\n\n"
            f"Error: {error}"
        )