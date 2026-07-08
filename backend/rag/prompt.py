from rag.retrieve import retrieve

def build_prompt(medium):

    context = retrieve(f"{medium} drawing techniques")

    prompt = f"""
You are an experienced drawing instructor.

The drawing medium used is: {medium}.

Reference Material:
{context}

Using only the reference material above, provide:

1. General feedback about this drawing medium.
2. Practical improvement tips.
3. Best practices for beginners.
4. Common mistakes to avoid.
5. Keep the response encouraging and concise.

Do not assume or analyze the uploaded drawing.
"""

    return prompt