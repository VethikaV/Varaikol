from PIL import Image
import torch
from transformers import AutoProcessor, AutoModel

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

MODEL_NAME = "google/siglip-base-patch16-224"

processor = AutoProcessor.from_pretrained(MODEL_NAME)

model = AutoModel.from_pretrained(MODEL_NAME).to(DEVICE)

model.eval()


# Labels to classify
LABELS = [

    "person",
    "portrait",

    "cat",
    "dog",
    "horse",
    "elephant",
    "lion",
    "tiger",
    "bird",
    "fish",
    "butterfly",

    "flower",
    "tree",
    "forest",
    "mountain",
    "river",
    "beach",
    "sunset",

    "house",
    "building",
    "bridge",
    "castle",

    "car",
    "bicycle",
    "motorcycle",
    "train",
    "airplane",

    "fruit",
    "apple",
    "banana",

    "cup",
    "book",
    "chair",
    "clock"
]


def detect_subject(image_path):

    image = Image.open(image_path).convert("RGB")

    inputs = processor(
        text=LABELS,
        images=image,
        return_tensors="pt",
        padding=True
    ).to(DEVICE)

    with torch.no_grad():

        outputs = model(**inputs)

    logits = outputs.logits_per_image

    probs = logits.softmax(dim=1)

    score, idx = torch.max(probs, dim=1)

    return {

        "subject": LABELS[idx.item()],

        "confidence": round(score.item() * 100, 2)

    }