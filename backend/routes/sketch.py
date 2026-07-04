from flask import Blueprint, request, jsonify
from services.opencv_sketch import photo_to_sketch

sketch_bp = Blueprint("sketch", __name__)

@sketch_bp.route("/api/sketch", methods=["POST"])
def convert_sketch():
    if "image" not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    image_bytes = request.files["image"].read()
    b64_sketch = photo_to_sketch(image_bytes)
    return jsonify({"sketch": b64_sketch})