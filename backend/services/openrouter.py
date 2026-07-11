import base64
import requests
from config import OPENROUTER_API_KEY, OPENROUTER_BASE_URL, MODEL


def encode_image(image_path):
    """Convert image to base64 string."""
    with open(image_path, "rb") as img:
        return base64.b64encode(img.read()).decode("utf-8")


def call_llm(
    prompt: str,
    image_path: str = None,
    system: str = "You are an experienced drawing instructor."
) -> str:

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost:3000",
        "X-Title": "AI Drawing Assistant"
    }

    # If an image is provided, send both prompt and image
    if image_path:
        image_base64 = encode_image(image_path)

        user_content = [
            {
                "type": "text",
                "text": prompt
            },
            {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{image_base64}"
                }
            }
        ]

    else:
        # Text-only request
        user_content = prompt

    body = {
        "model": MODEL,
        "messages": [
            {
                "role": "system",
                "content": system
            },
            {
                "role": "user",
                "content": user_content
            }
        ]
    }

    response = requests.post(
        OPENROUTER_BASE_URL,
        headers=headers,
        json=body
    )

    response.raise_for_status()

    data = response.json()

    print("OpenRouter Response:")
    print(data)

    return data["choices"][0]["message"]["content"]