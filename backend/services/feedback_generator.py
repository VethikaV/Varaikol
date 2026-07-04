def generate_feedback(medium, colors=None, objects=None, style=None):
    """
    Generate AI feedback for a drawing based on analysis results.
    """

    colors = colors or []
    objects = objects or []

    feedback_parts = []
    tips = []

    # -------------------------
    # MEDIUM ANALYSIS
    # -------------------------
    if medium == "pencil sketch":
        feedback_parts.append(
            "Your pencil sketch shows good basic structure and shading potential."
        )
        tips.extend([
            "Focus on smoother shading transitions.",
            "Improve line consistency for cleaner outlines.",
            "Add more depth using cross-hatching techniques."
        ])

    elif medium == "colored drawing":
        feedback_parts.append(
            "Your colored artwork shows creativity in color usage."
        )
        tips.extend([
            "Try blending colors for smoother gradients.",
            "Avoid overusing similar tones in one area.",
            "Balance warm and cool colors for better contrast."
        ])

    elif medium == "digital art":
        feedback_parts.append(
            "Your digital artwork demonstrates modern styling techniques."
        )
        tips.extend([
            "Use layer separation for better control.",
            "Experiment with lighting effects.",
            "Refine edges for a polished look."
        ])

    else:
        feedback_parts.append(
            "Your artwork has a unique style and creative expression."
        )
        tips.append("Try exploring shading and proportion improvements.")

    # -------------------------
    # COLOR ANALYSIS
    # -------------------------
    if colors:
        dominant_colors = [c.get("color") for c in colors[:3]]

        feedback_parts.append(
            f"The dominant colors used are {', '.join(dominant_colors)}."
        )

        if "Black" in dominant_colors and "White" in dominant_colors:
            tips.append("Strong contrast detected — try adding mid-tones for depth.")

        if "Red" in dominant_colors:
            tips.append("Red adds strong emotion — use it strategically for focus areas.")

    # -------------------------
    # OBJECT ANALYSIS
    # -------------------------
    if objects:
        feedback_parts.append(
            f"Detected subjects include: {', '.join(objects)}."
        )

        tips.append("Ensure proportions are consistent for all detected objects.")
        tips.append("Maintain perspective alignment between objects.")

    # -------------------------
    # STYLE ANALYSIS
    # -------------------------
    if style:
        feedback_parts.append(
            f"The overall style appears to be {style}."
        )

        if style == "realistic":
            tips.append("Enhance fine details like texture and lighting realism.")
        elif style == "cartoon":
            tips.append("Exaggerate features slightly for stronger visual impact.")

    # -------------------------
    # FINAL OUTPUT
    # -------------------------
    feedback = " ".join(feedback_parts)

    return {
        "feedback": feedback,
        "tips": tips[:6]  # limit output for UI cleanliness
    }