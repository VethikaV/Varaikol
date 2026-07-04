from PIL import Image
import torch
import clip
import io

device = "cuda" if torch.cuda.is_available() else "cpu"
model, preprocess = clip.load("ViT-B/32", device=device)

LABELS = [
    "pencil sketch", "charcoal drawing", "watercolor painting",
    "ink drawing", "digital art", "oil painting", "pastel drawing"
]

def classify_medium(image_bytes: bytes) -> str:
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    image_input = preprocess(image).unsqueeze(0).to(device)
    text_inputs = clip.tokenize(LABELS).to(device)

    with torch.no_grad():
        image_features = model.encode_image(image_input)
        text_features = model.encode_text(text_inputs)
        logits = (image_features @ text_features.T).softmax(dim=-1)
        best_idx = logits.argmax().item()

    return LABELS[best_idx]