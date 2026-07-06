import requests
import uuid
import os
from typing import Optional
from config import STABILITY_API_KEY

STABILITY_URL = "https://api.stability.ai/v2beta/stable-image/generate/core"
GENERATED_DIR = os.path.join(os.path.dirname(__file__), "..", "static", "generated")


def generate_image_stability(prompt: str, style_preset: Optional[str] = None) -> Optional[str]:
    """Generates an image, saves it to /static/generated, and returns a relative URL path."""
    try:
        data = {
            "prompt": prompt,
            "output_format": "png",
        }
        if style_preset:
            data["style_preset"] = style_preset

        response = requests.post(
            STABILITY_URL,
            headers={
                "Authorization": f"Bearer {STABILITY_API_KEY}",
                "Accept": "image/*",
            },
            files={"none": (None, "")},
            data=data,
        )
        response.raise_for_status()

        os.makedirs(GENERATED_DIR, exist_ok=True)

        filename = f"{uuid.uuid4().hex}.png"
        filepath = os.path.join(GENERATED_DIR, filename)

        with open(filepath, "wb") as f:
            f.write(response.content)

        return f"/static/generated/{filename}"

    except Exception as e:
        print("Stability image generation error:", e)
        return None