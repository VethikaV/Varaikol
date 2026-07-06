import re

def parse_llm_output(text: str) -> dict:
    result = {"easy": "", "medium": "", "hard": ""}

    if not text:
        return result

    # Strip markdown bold so "**EASY:**" still matches
    cleaned = re.sub(r"\*\*", "", text)

    patterns = {
        "easy":   r"(?:E?ASY)\s*:?\s*(.+?)(?=\n\s*(?:\*\*)?MEDIUM\s*:|\Z)",
        "medium": r"MEDIUM\s*:\s*(.+?)(?=\n\s*(?:\*\*)?HARD\s*:|\Z)",
        "hard":   r"HARD\s*:\s*(.+)",
    }

    for key, pattern in patterns.items():
        match = re.search(pattern, cleaned, re.IGNORECASE | re.DOTALL)
        if match:
            result[key] = " ".join(match.group(1).split()).strip()

    # Fallback: if "easy" still didn't match anything, grab whatever text
    # appears before "MEDIUM:" — handles cases where the model mangles
    # or drops the "EASY:" label entirely.
    if not result["easy"]:
        fallback = re.split(r"\n\s*MEDIUM\s*:", cleaned, flags=re.IGNORECASE)[0].strip()
        # Strip a stray leading label fragment like "ASY" or "EASY" if present
        fallback = re.sub(r"^(E?ASY)\s*:?\s*", "", fallback, flags=re.IGNORECASE).strip()
        if fallback:
            result["easy"] = fallback

    return result