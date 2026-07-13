from rag.retrieve import retrieve


def build_prompt(medium, colors):

    # Retrieve knowledge related to the detected medium
    context = retrieve(medium)

    prompt = f"""
You are an experienced drawing instructor.

The uploaded image is a drawing.

The detected drawing medium is: {medium}.

The detected colors are: {", ".join(colors)}.

Reference Material:

{context}

Analyze the uploaded drawing and provide:

1. Overall quality of the drawing.
2. Strengths.
3. Areas for improvement.
4. Feedback specific to the detected drawing medium ({medium}).
5. Any mistakes you observe.
6. Practical suggestions to improve the artwork.

Important Instructions:
- Use both the uploaded image and the reference material to generate your feedback.
- Base your observations only on what is actually visible in the drawing.
- Do not invent details that are not present.
- If any aspect is unclear, state that instead of guessing.
- Keep the feedback constructive, specific.
"""

    return prompt