from flask import Blueprint, request, jsonify
from services.openrouter import call_llm
from services.stability import generate_image_stability
from utils.prompt_parser import parse_llm_output

ideas_bp = Blueprint("ideas", __name__)


def build_styled_prompt(base_prompt: str, style: str) -> str:
    return f"{base_prompt}, {style}, clean reference image, plain background"


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

Generate EXACTLY 3 short scene descriptions of the SAME subject, increasing
in complexity. Describe ONLY the subject, pose, and composition — do NOT
mention art style, lighting quality, "realistic", "detailed", "photograph",
or camera/rendering terms. Keep each description under 20 words.

Respond in EXACTLY this format, with no extra text before or after:

EASY: <subject description>
MEDIUM: <subject description>
HARD: <subject description>

Rules:
- Same subject across all three
- Do not add commentary, headers, or markdown formatting
- Do not abbreviate or truncate the word "EASY"
- Do not describe art style — that will be added separately

"""

    # ==============================
    # CALL LLM (with retry on parse failure)
    # ==============================
    prompts = {"easy": "", "medium": "", "hard": ""}
    raw_response = ""
    max_attempts = 2

    for attempt in range(max_attempts):
        try:
            raw_response = call_llm(prompt)
        except Exception as e:
            print(f"LLM call failed (attempt {attempt + 1}):", e)
            continue

        print(f"LLM RESPONSE (attempt {attempt + 1}):", raw_response)

        prompts = parse_llm_output(raw_response)

        if prompts["easy"] and prompts["medium"] and prompts["hard"]:
            break  # success, stop retrying

        print(f"PARSE FAILED (attempt {attempt + 1}) — raw output was:\n{raw_response}")

    # ==============================
    # FINAL CHECK — give up gracefully if still incomplete
    # ==============================
    if not prompts["easy"] or not prompts["medium"] or not prompts["hard"]:
        return jsonify({
            "error": "Could not generate ideas right now. Please try again."
        }), 500

    # ==============================
    # GENERATE IMAGES (Stability AI, saved to disk)
    # ==============================
    easy_img = generate_image_stability(
        build_styled_prompt(
            prompts["easy"],
            "hand-drawn pencil sketch, graphite lines, sketchbook drawing, not a photo, no color"
        ),
        style_preset="line-art"
    )
    medium_img = generate_image_stability(
        build_styled_prompt(
            prompts["medium"],
            "colored pencil illustration, hand-drawn shading strokes, sketchbook art, not a photo"
        ),
        style_preset="comic-book"
    )
    hard_img = generate_image_stability(
        build_styled_prompt(
            prompts["hard"],
            "acrylic painting, visible brush strokes, painted canvas texture, illustrated artwork, not a photo"
        ),
        style_preset="fantasy-art"
    )

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