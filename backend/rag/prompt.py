from rag.retrieve import retrieve

def build_prompt(medium):
    context = retrieve(f"{medium} drawing techniques")

    return f"""
You are an experienced drawing instructor.

The uploaded image is a drawing.

The detected drawing medium is: {medium}.

Reference Material:
{context}

Analyze the uploaded drawing and provide:

1. Overall quality of the drawing.
2. Strengths.
3. Areas for improvement.
4. Suggestions based on the detected medium.
5. Any mistakes you observe.
6. An encouraging conclusion.

Use the uploaded image together with the reference material.
Base your feedback on what you actually observe in the drawing.
If something is unclear, mention that instead of guessing.
"""
    