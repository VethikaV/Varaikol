import os
from werkzeug.utils import secure_filename
from flask import Blueprint, request, jsonify

from services.medium_classifier import classify_medium
from services.feedback_generator import generate_feedback

analyze_bp = Blueprint("analyze", __name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@analyze_bp.route("/analyze", methods=["POST"])
def analyze():

    file = request.files.get("image")

    if file is None:
        return jsonify({"error": "No image uploaded"}), 400

    filename = secure_filename(file.filename)
    path = os.path.join(UPLOAD_FOLDER, filename)

    file.save(path)

    result = classify_medium(path)

    if result["medium"] == "Photo":
        return jsonify({
            "type": "Photo",
            "message": "This is a photograph.",
            "confidence": result["confidence"]
        })

    feedback_result = generate_feedback(medium=result["medium"])

    return jsonify({
        "type": "Drawing",
        "medium": result["medium"],
        "confidence": result["confidence"],
        "feedback": feedback_result["feedback"],
        "tips": feedback_result["tips"]
    })