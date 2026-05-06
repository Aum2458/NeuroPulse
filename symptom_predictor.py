"""
FINAL safe SymptomPredictor replacement for NeuroPulse project.
AI is ONLY used for explanation of risk levels.
No predictions or disease diagnosis.
"""

from ai.ai_chat_response import get_ai_response

class SymptomPredictor:
    """
    Explanation-only AI agent.
    """
    def __init__(self):
        pass  # No ML model required

    def explain_risk(self, risk_level: str) -> str:
        """
        Generate AI explanation for a risk level.
        """
        try:
            prompt = f"""
            You are a medical educator AI.
            Explain the health risk level '{risk_level}' in simple, general terms.
            Do NOT give a diagnosis.
            Do NOT suggest any medicine.
            Provide 2-3 general health awareness tips.
            """
            explanation = get_ai_response(prompt)
            return explanation
        except Exception as e:
            return f"⚠️ Explanation unavailable: {e}"
