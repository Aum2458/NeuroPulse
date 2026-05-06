"""
AI module for safe risk explanation.
No diagnosis, no medicines, no confidence scoring.
"""

from ai.ai_chat_response import get_ai_response

class SymptomAI:
    def __init__(self):
        pass

    def explain_risk(self, risk_level: str) -> str:
        try:
            prompt = f"""
            Explain the health risk level '{risk_level}' in simple, educational terms.
            Do NOT give a diagnosis.
            Do NOT suggest medications.
            Give 2-3 general tips or awareness points.
            """
            explanation = get_ai_response(prompt)
            return explanation
        except Exception as e:
            return f"⚠️ AI explanation unavailable: {e}"
