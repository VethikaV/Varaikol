import os
import json
import torch
import numpy as np

from PIL import Image
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, classification_report

from torchvision.datasets import ImageFolder
from torchvision import transforms
from torchvision.transforms import InterpolationMode

from torch.utils.data import DataLoader, Subset
from transformers import AutoImageProcessor, AutoModelForImageClassification
from torch.optim import AdamW
from torch.nn import CrossEntropyLoss
from tqdm import tqdm

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(device)

DATASET_PATH = "dataset"
MODEL_NAME = "google/siglip-base-patch16-224"

# -----------------------------------------------------------
# Load processor FIRST — training transforms must match exactly
# what services/medium_classifier.py uses at inference time.
# -----------------------------------------------------------
processor = AutoImageProcessor.from_pretrained(MODEL_NAME)
image_mean = processor.image_mean
image_std = processor.image_std

train_transform = transforms.Compose([
    transforms.Resize((224, 224), interpolation=InterpolationMode.BICUBIC),
    transforms.RandomHorizontalFlip(),
    transforms.RandomRotation(10),
    transforms.ColorJitter(brightness=0.1, contrast=0.1, saturation=0.1),
    transforms.ToTensor(),
    transforms.Normalize(mean=image_mean, std=image_std),  # <-- was missing before
])

val_transform = transforms.Compose([
    transforms.Resize((224, 224), interpolation=InterpolationMode.BICUBIC),
    transforms.ToTensor(),
    transforms.Normalize(mean=image_mean, std=image_std),  # <-- was missing before
])

# -----------------------------------------------------------
# Stratified split (old random_split didn't preserve class ratios)
# -----------------------------------------------------------
base_dataset = ImageFolder(DATASET_PATH)  # no transform, just used for indices/targets
print(base_dataset.classes)

targets = [label for _, label in base_dataset.samples]
train_idx, val_idx = train_test_split(
    list(range(len(base_dataset))),
    test_size=0.2,
    stratify=targets,
    random_state=42
)

train_dataset_full = ImageFolder(DATASET_PATH, transform=train_transform)
val_dataset_full = ImageFolder(DATASET_PATH, transform=val_transform)

train_dataset = Subset(train_dataset_full, train_idx)
val_dataset = Subset(val_dataset_full, val_idx)

train_loader = DataLoader(train_dataset, batch_size=16, shuffle=True)
val_loader = DataLoader(val_dataset, batch_size=16, shuffle=False)

# -----------------------------------------------------------
# Model
# -----------------------------------------------------------
model = AutoModelForImageClassification.from_pretrained(
    MODEL_NAME,
    num_labels=len(base_dataset.classes),
    ignore_mismatched_sizes=True
)
model.to(device)

# -----------------------------------------------------------
# Freeze most of the backbone — full fine-tuning on ~950 images
# is what caused train acc to hit 99.8% while val stalled at 79.5%.
# Only unfreeze the last 2 encoder layers + classifier head.
# -----------------------------------------------------------
for param in model.vision_model.parameters():
    param.requires_grad = False

for param in model.vision_model.encoder.layers[-2:].parameters():
    param.requires_grad = True

for param in model.classifier.parameters():
    param.requires_grad = True

optimizer = AdamW([
    {"params": model.vision_model.encoder.layers[-2:].parameters(), "lr": 1e-5},
    {"params": model.classifier.parameters(), "lr": 1e-4},
], weight_decay=0.01)

criterion = CrossEntropyLoss()

# -----------------------------------------------------------
# Train with early stopping on best val accuracy
# -----------------------------------------------------------
epochs = 15
best_val_acc = 0.0

for epoch in range(epochs):
    model.train()
    total_loss, correct, total = 0, 0, 0

    for images, labels in tqdm(train_loader):
        images, labels = images.to(device), labels.to(device)

        optimizer.zero_grad()
        outputs = model(pixel_values=images)
        loss = criterion(outputs.logits, labels)
        loss.backward()
        optimizer.step()

        total_loss += loss.item()
        preds = torch.argmax(outputs.logits, dim=1)
        correct += (preds == labels).sum().item()
        total += labels.size(0)

    train_acc = correct / total

    # ---- validation ----
    model.eval()
    val_correct, val_total = 0, 0
    all_preds, all_labels = [], []

    with torch.no_grad():
        for images, labels in val_loader:
            images, labels = images.to(device), labels.to(device)
            outputs = model(pixel_values=images)
            preds = outputs.logits.argmax(dim=1)

            val_correct += (preds == labels).sum().item()
            val_total += labels.size(0)
            all_preds.extend(preds.cpu().numpy())
            all_labels.extend(labels.cpu().numpy())

    val_acc = val_correct / val_total

    print(f"Epoch {epoch+1} | Loss: {total_loss:.2f} | "
          f"Train Acc: {train_acc:.4f} | Val Acc: {val_acc:.4f}")

    if val_acc > best_val_acc:
        best_val_acc = val_acc
        torch.save(model.state_dict(), "medium_classifier.pth")
        print(f"  -> New best model saved (val_acc={val_acc:.4f})")

print(f"\nBest validation accuracy: {best_val_acc:.4f}")

# -----------------------------------------------------------
# Confusion matrix — shows exactly which mediums get confused
# -----------------------------------------------------------
print("\nConfusion Matrix:")
print(confusion_matrix(all_labels, all_preds))
print("\nClassification Report:")
print(classification_report(all_labels, all_preds, target_names=base_dataset.classes))

with open("labels.json", "w") as f:
    json.dump(base_dataset.classes, f)
print("Labels saved!")