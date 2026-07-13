import colorsys


def classify_color(rgb):

    r, g, b = rgb

    # Normalize RGB
    r = r / 255
    g = g / 255
    b = b / 255

    # Convert RGB to HSV
    h, s, v = colorsys.rgb_to_hsv(r, g, b)

    h = h * 360
    s = s * 100
    v = v * 100


    # Black (very dark)
    if v < 20:
        return "Black"


    # Low saturation colors -> treat based on brightness
    if s < 15:

        if v < 50:
            return "Black"

        return "Brown"


    # RED (0-15, 345-360)
    if h < 15 or h > 345:

        if v < 45:
            return "Dark Red"

        return "Red"



    # PINK (330-345)
    if h >= 330 and h <= 345:

        if v < 70:
            return "Dark Pink"

        return "Pink"



    # ORANGE/YELLOW
    if h >= 15 and h < 70:

        if s < 40:
            return "Light Brown"

        return "Yellow"



    # GREEN
    if h >= 70 and h < 170:

        if v < 45:
            return "Dark Green"

        elif v > 75:
            return "Light Green"

        return "Green"



    # BLUE
    if h >= 170 and h < 260:

        if v < 45:
            return "Dark Blue"

        elif v > 75:
            return "Light Blue"

        return "Blue"



    # PURPLE -> map to Pink/Dark Pink
    if h >= 260 and h < 330:

        if v < 50:
            return "Dark Pink"

        return "Pink"



    # BROWN
    if h >= 10 and h < 50:

        if v < 40:
            return "Dark Brown"

        elif v > 70:
            return "Light Brown"

        return "Brown"


    # fallback (never unknown)
    return "Brown"