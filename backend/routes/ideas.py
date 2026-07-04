import re
import requests

from flask import Blueprint, request, jsonify
from services.openrouter import call_llm
from utils.prompt_parser import parse_llm_output

ideas_bp = Blueprint("ideas", __name__)



import urllib.parse

def generate_image(prompt: str):
    try:
        encoded_prompt = urllib.parse.quote(prompt)
        url = f"https://image.pollinations.ai/prompt/{encoded_prompt}"
        return url  # returns direct image URL

    except Exception as e:
        print("Image generation error:", e)
        return None

# ==============================
# MAIN ROUTE
# ==============================
@ideas_bp.route("/api/ideas", methods=["POST"])
def get_ideas():
    data = request.json
    user_input = data.get("prompt", "house")

    # ==============================
    # LLM PROMPT
    # ==============================
    prompt = f"""
You are an expert drawing tutor and AI image prompt engineer.

User wants to draw: "{user_input}"

Generate EXACTLY 3 AI image prompts.

FORMAT:
EASY: ...
MEDIUM: ...
HARD: ...

Rules:
- Same subject
- Increasing difficulty
- Only return the 3 lines
"""

    # ==============================
    # CALL LLM
    # ==============================
    response = call_llm(prompt)

    print("LLM RESPONSE:", response)

      #    ✅ FIX: response is already text
    text_output = response
    # ==============================
    # PARSE PROMPTS
    # ==============================
    prompts = parse_llm_output(text_output)

    # ==============================
    # GENERATE IMAGES
    # ==============================
    easy_img = generate_image(prompts["easy"])
    medium_img = generate_image(prompts["medium"])
    hard_img = generate_image(prompts["hard"])

    # ==============================
    # RESPONSE
    # ==============================
    return jsonify({
        "easy": {
            "prompt": prompts["easy"],
            "image": easy_img
        },
        "medium": {
            "prompt": prompts["medium"],
            "image": medium_img
        },
        "hard": {
            "prompt": prompts["hard"],
            "image": hard_img
        }
    })
