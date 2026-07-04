# services/image_generator.py
import urllib.parse

def generate_image(prompt: str):
    encoded = urllib.parse.quote(prompt)
    return f"https://image.pollinations.ai/prompt/{encoded}"