import cv2
import numpy as np
import base64


def draw_dotted_line(img, start, end, color=120, radius=2, gap=12):
    """
    Draw a dotted line between two points.
    """
    dist = int(np.hypot(end[0] - start[0], end[1] - start[1]))

    for i in range(0, dist + 1, gap):
        r = i / dist if dist else 0
        x = int(start[0] + (end[0] - start[0]) * r)
        y = int(start[1] + (end[1] - start[1]) * r)

        cv2.circle(img, (x, y), radius, color, -1)


def photo_to_sketch(image_bytes: bytes) -> str:
    # Decode image
    nparr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Invert grayscale image
    inv = 255 - gray

    # Blur the inverted image
    blur = cv2.GaussianBlur(inv, (21, 21), 0)

    # Invert the blurred image
    inv_blur = 255 - blur

    # Create pencil sketch
    sketch = cv2.divide(gray, inv_blur, scale=256.0)

# Convert grayscale sketch to BGR so colored lines can be drawn
    sketch = cv2.cvtColor(sketch, cv2.COLOR_GRAY2BGR)

    # -------------------------------
    # Draw centered dotted "+"
    # -------------------------------
    h, w = sketch.shape[:2]
    cx, cy = w // 2, h // 2

    # Vertical dotted line
    draw_dotted_line(
    sketch,
    (cx, 0),
    (cx, h - 1),
    color=(0, 0, 255),  # Red (BGR)
    radius=2,
    gap=12
    )

    # Horizontal dotted line
    draw_dotted_line(
    sketch,
    (0, cy),
    (w - 1, cy),
    color=(0, 0, 255),  # Red (BGR)
    radius=2,
    gap=12
    ) 

    # Encode sketch as PNG
    _, buffer = cv2.imencode(".png", sketch)

    # Return Base64 string
    return base64.b64encode(buffer).decode("utf-8")