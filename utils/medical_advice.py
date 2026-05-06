from typing import Dict
from ai.ai_chat_response import get_ai_response

# -------------------- SAFETY CONSTANTS --------------------
MIN_CONFIDENCE = 50.0  # Minimum AI confidence to provide suggestions

SAFETY_NOTE = (
    "⚠️ This information is for awareness only and is NOT a medical prescription. "
    "Always consult a qualified doctor before taking any medication."
)

# -------------------- MEDICATION SUGGESTIONS --------------------
def get_medications(result: Dict[str, float]) -> Dict[str, str]:
    """
    Generates SAFE, NON-PRESCRIPTIVE medication names using AI.
    Only provides medicines for diseases with confidence >= MIN_CONFIDENCE.

    Args:
        result (Dict[str, float]): Mapping of disease names to confidence percentages.

    Returns:
        Dict[str, str]: Mapping of disease to AI-suggested medicines with safety note.
    """
    medications: Dict[str, str] = {}

    if not isinstance(result, dict):
        return {"error": "Invalid prediction format"}

    for disease, confidence in result.items():
        try:
            confidence = float(confidence)
        except (ValueError, TypeError):
            continue

        if confidence < MIN_CONFIDENCE:
            continue  # Skip low-confidence predictions

        prompt = (
            "You are a medical awareness assistant.\n"
            f"Disease: {disease}\n\n"
            "Task:\n"
            "- List only common medicine NAMES (not dosages)\n"
            "- Do NOT prescribe\n"
            "- Do NOT claim cure\n"
            "- Keep it short (3–5 items)\n"
            "- End with a safety warning\n"
        )

        try:
            ai_text = get_ai_response(prompt)
            medications[disease] = f"{ai_text}\n\n{SAFETY_NOTE}"
        except Exception:
            medications[disease] = (
                "General medicines may be used depending on doctor advice.\n\n"
                f"{SAFETY_NOTE}"
            )

    return medications

# -------------------- LIFESTYLE SUGGESTIONS --------------------
def get_suggestions(result: Dict[str, float]) -> Dict[str, str]:
    """
    Generates SAFE lifestyle suggestions using AI.
    Only provides suggestions for diseases with confidence >= MIN_CONFIDENCE.

    Args:
        result (Dict[str, float]): Mapping of disease names to confidence percentages.

    Returns:
        Dict[str, str]: Mapping of disease to AI-generated lifestyle tips.
    """
    suggestions: Dict[str, str] = {}

    if not isinstance(result, dict):
        return {"error": "Invalid prediction format"}

    for disease, confidence in result.items():
        try:
            confidence = float(confidence)
        except (ValueError, TypeError):
            continue

        if confidence < MIN_CONFIDENCE:
            continue

        prompt = (
            "You are a health-support assistant.\n"
            f"Condition: {disease}\n\n"
            "Task:\n"
            "- Suggest simple daily lifestyle improvements\n"
            "- No medical claims\n"
            "- No alternative medicine\n"
            "- Use easy language\n"
            "- Max 5 bullet points\n"
        )

        try:
            suggestions[disease] = get_ai_response(prompt)
        except Exception:
            # Fallback generic suggestions
            suggestions[disease] = (
                "• Maintain a healthy routine\n"
                "• Eat balanced meals\n"
                "• Stay active as per comfort\n"
                "• Get enough rest\n"
                "• Consult a healthcare professional"
            )

    return suggestions
