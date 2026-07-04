import json
import torch
import os

os.environ["USE_TF"] = "0"
os.environ["USE_TORCH"] = "1"

from transformers import AutoModelForImageClassification, AutoImageProcessor
from PIL import Image

# -----------------------------
# CONFIG
# -----------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_NAME = "google/siglip-base-patch16-224"
MODEL_PATH = os.path.join(BASE_DIR, "saved_model", "medium_classifier.pth")
LABELS_PATH = os.path.join(BASE_DIR, "saved_model", "labels.json")
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# -----------------------------
# LOAD LABELS
# -----------------------------
with open(LABELS_PATH, "r") as f:
    CLASS_NAMES = json.load(f)

# -----------------------------
# LOAD MODEL + PROCESSOR
# -----------------------------
processor = AutoImageProcessor.from_pretrained(MODEL_NAME)

model = AutoModelForImageClassification.from_pretrained(
    MODEL_NAME,
    num_labels=len(CLASS_NAMES),
    ignore_mismatched_sizes=True
)

state_dict = torch.load(MODEL_PATH, map_location=DEVICE)
model.load_state_dict(state_dict)
model.to(DEVICE)
model.eval()

# -----------------------------
# PREDICT FUNCTION
# -----------------------------
def classify_medium(image_path):
    image = Image.open(image_path).convert("RGB")

    inputs = processor(images=image, return_tensors="pt").to(DEVICE)

    with torch.no_grad():
        outputs = model(**inputs)
        probabilities = torch.softmax(outputs.logits, dim=1)
        confidence, prediction = torch.max(probabilities, dim=1)

    medium = CLASS_NAMES[prediction.item()]
    confidence = round(confidence.item() * 100, 2)

    return {
        "medium": medium,
        "confidence": confidence
    }