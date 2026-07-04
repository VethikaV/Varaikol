import cv2
import numpy as np
import base64

def photo_to_sketch(image_bytes: bytes) -> str:
    # Decode image
    nparr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Invert
    inv = 255 - gray

    # Blur
    blur = cv2.GaussianBlur(inv, (21, 21), 0)

    # Invert blurred image
    inv_blur = 255 - blur

    # Pencil sketch
    sketch = cv2.divide(gray, inv_blur, scale=256.0)

    # Encode as PNG
    _, buffer = cv2.imencode(".png", sketch)
    return base64.b64encode(buffer).decode("utf-8")