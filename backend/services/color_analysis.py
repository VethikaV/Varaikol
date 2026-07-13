import cv2
import numpy as np
from sklearn.cluster import KMeans
from services.color_database import classify_color
import numpy as np

def detect_colors(image_path, medium="ColorPencil", n_colors=14, min_percent=1.0):
    """
    Detects the specific colors used in a drawing.
    Returns [{"color": name, "percentage": float}, ...].

    If the detected medium is Graphite Pencil, color detection is skipped
    and only "Pencil" is returned.
    """

    # Normalize medium name
    medium_name = medium.lower().replace(" ", "").replace("_", "")

    # Skip color detection for graphite pencil drawings
    if medium_name == "graphitepencil":
        return [
            {
                "color": "Pencil",
                "percentage": 100.0
            }
        ]

    image = cv2.imread(image_path)
    if image is None:
        return []

    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    pixels = image.reshape(-1, 3)

    # Remove near-white background/paper
    pixels = pixels[np.any(pixels < 245, axis=1)]

    if len(pixels) == 0:
        return []

    # Number of clusters
    k = min(n_colors, len(pixels))

    kmeans = KMeans(
        n_clusters=k,
        random_state=42,
        n_init=10
    )

    labels = kmeans.fit_predict(pixels)
    centers = kmeans.cluster_centers_

    counts = np.bincount(labels)
    percentages = counts / counts.sum()

    merged = {}

    for center, percent in zip(centers, percentages):

        if percent * 100 < min_percent:
            continue

        name = classify_color(center.astype(int))

        merged[name] = merged.get(name, 0) + percent

    result = sorted(
        merged.items(),
        key=lambda x: x[1],
        reverse=True
    )

    return [
        {
            "color": name,
            "percentage": round(percent * 100, 1)
        }
        for name, percent in result
    ]