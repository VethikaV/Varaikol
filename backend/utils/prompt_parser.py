import re

def parse_llm_output(text: str) -> dict:
    result = {"easy": "", "medium": "", "hard": ""}
    for line in text.splitlines():
        line = line.strip()
        if line.upper().startswith("EASY:"):
            result["easy"] = line.split(":", 1)[1].strip()
        elif line.upper().startswith("MEDIUM:"):
            result["medium"] = line.split(":", 1)[1].strip()
        elif line.upper().startswith("HARD:"):
            result["hard"] = line.split(":", 1)[1].strip()
    return result