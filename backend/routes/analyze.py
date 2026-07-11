import os
from werkzeug.utils import secure_filename
from flask import Blueprint, request, jsonify

from services.medium_classifier import classify_medium
from rag.prompt import build_prompt
from services.openrouter import call_llm

analyze_bp = Blueprint("analyze", __name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@analyze_bp.route("/analyze", methods=["POST"])
def analyze():

    file = request.files.get("image")

    if file is None:
        return jsonify({"error": "No image uploaded"}), 400


    # Save uploaded image
    filename = secure_filename(file.filename)
    path = os.path.join(UPLOAD_FOLDER, filename)

    file.save(path)


    # Detect drawing medium using ML model
    result = classify_medium(path)


    # If uploaded file is a photo, return immediately
    if result["medium"] == "Photo":
        return jsonify({
            "type": "Photo",
            "message": "This is a photograph.",
            "confidence": result["confidence"]
        })


    # Build RAG prompt using detected medium
    prompt = build_prompt(result["medium"])


    # Send BOTH prompt + image to Vision LLM
    feedback = call_llm(
        prompt=prompt,
        image_path=path
    )


    return jsonify({
        "type": "Drawing",
        "medium": result["medium"],
        "confidence": result["confidence"],
        "feedback": feedback
    })