import os
from werkzeug.utils import secure_filename
from flask import Blueprint, request, jsonify

from services.medium_classifier import classify_medium
from services.color_analysis import detect_colors
from rag.prompt import build_prompt
from services.openrouter import call_llm


analyze_bp = Blueprint("analyze", __name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@analyze_bp.route("/analyze", methods=["POST"])
def analyze():

    file = request.files.get("image")

    if file is None:
        return jsonify({
            "error": "No image uploaded"
        }), 400


    # Save uploaded image
    filename = secure_filename(file.filename)
    path = os.path.join(
        UPLOAD_FOLDER,
        filename
    )

    file.save(path)


    # -----------------------------
    # 1. Detect Drawing Medium
    # -----------------------------
    medium_result = classify_medium(path)


    medium = medium_result["top_prediction"]["medium"]
    confidence = medium_result["top_prediction"]["confidence"]


    # -----------------------------
    # 2. Handle Photo separately
    # -----------------------------
    if medium == "Photo":

        return jsonify({

            "type": "Photo",

            "message": "This is a photograph, not a drawing.",

            "medium": medium,

            "confidence": confidence

        })


    # -----------------------------
    # 3. Detect Colors
    # -----------------------------
    detected_colors = detect_colors(
        path,
        medium=medium
    )


    colors_used = [
        color["color"]
        for color in detected_colors
    ]


    # -----------------------------
    # 4. Build RAG Prompt
    # -----------------------------
    prompt = build_prompt(
        medium=medium,
        colors=colors_used
    )


    # -----------------------------
    # 5. Generate Feedback
    # -----------------------------
    feedback = call_llm(
        prompt=prompt,
        image_path=path
    )


    # -----------------------------
    # Final Response
    # -----------------------------
    return jsonify({

        "type": "Drawing",

        "medium": medium,

        "confidence": confidence,

        "colors": colors_used,

        "feedback": feedback

    })