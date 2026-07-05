# 📊 Dataset & Model Training

## Dataset

The artwork medium classification model was trained on a custom dataset consisting of different types of visual artwork. Images were collected from publicly available sources and manually categorized into distinct artistic mediums.

### Dataset Structure

dataset/
│
├── Acrylic/
├── ColorPencil/
├── GraphitePencil/
├── Oil/
├── Pastel/
├── Photo/
└── Watercolor/
```

### Dataset Distribution

- **Acrylic:** 196 images
- **Color Pencil:** 137 images
- **Graphite Pencil:** 142 images
- **Oil Painting:** 200 images
- **Pastel:** 200 images
- **Photo:** 125 images
- **Watercolor:** 170 images

**Total Dataset Size:** **1,170 images**

---


# Data Preprocessing

Before training, all images were preprocessed using the **SigLIP AutoImageProcessor** provided by Hugging Face.

The preprocessing pipeline included:

- Automatic image resizing to **224 × 224**
- RGB conversion
- Pixel normalization
- Tensor conversion
- Batch loading using PyTorch DataLoader

The dataset was divided into:

- **80% Training**
- **20% Validation/Test**

---

# Model Architecture

The artwork classifier was developed using **Transfer Learning** with Google's **SigLIP** model.

### Base Model

**Model Name**

```
google/siglip-base-patch16-224
```

SigLIP is a Vision Transformer (ViT)-based image encoder pretrained on a large-scale image-text dataset using Sigmoid Loss. It produces highly discriminative visual embeddings, making it suitable for image classification tasks.

---

# Training Configuration

| Parameter | Value |
|------------|--------|
| Framework | PyTorch |
| Model | Google SigLIP Base Patch16-224 |
| Image Size | 224 × 224 |
| Epochs | 5 |
| Optimizer | AdamW |
| Loss Function | CrossEntropyLoss |
| Device | CUDA / CPU |
| Classification Head | Fine-tuned |

---

# Training Procedure

The following steps were used during training:

1. Load the pretrained SigLIP image classification model.
2. Replace the original classification layer with a new layer matching the number of artwork classes.
3. Load images using the PyTorch DataLoader.
4. Process images using the SigLIP AutoImageProcessor.
5. Compute predictions using the model.
6. Calculate Cross Entropy Loss.
7. Perform backpropagation.
8. Update model weights using the optimizer.
9. Repeat for **5 epochs**.
10. Save the trained model for inference.

---

# Training Algorithm

The model follows the supervised learning workflow:

```
Input Image
      │
      ▼
SigLIP AutoImageProcessor
      │
      ▼
Pretrained SigLIP Vision Transformer
      │
      ▼
Classification Head
      │
      ▼
CrossEntropy Loss
      │
      ▼
Backpropagation
      │
      ▼
AdamW Optimizer
```

---

# Evaluation

The model performance is evaluated using:

- Training Accuracy
- Validation Accuracy
- Test Accuracy
- Cross Entropy Loss



# Technologies Used

- Python
- PyTorch
- Hugging Face Transformers
- SigLIP
- NumPy
- OpenCV
- TorchVision

---

# Why SigLIP?

Google SigLIP was selected because it provides:

- Strong visual representation learning
- State-of-the-art transfer learning performance
- High classification accuracy with limited training data
- Efficient fine-tuning
- Excellent generalization across different image domains

Its pretrained visual encoder significantly reduces training time while achieving high accuracy on artwork medium classification.

---

