import os
import google.generativeai as genai

# -------------------- CONFIG --------------------
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
if not GEMINI_API_KEY:
    print("⚠️ Warning: GEMINI_API_KEY not set. Gemini AI calls will fail.")

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-pro")

# -------------------- FUNCTIONS --------------------

def get_gemini_response(prompt: str) -> str:
    """
    Generates a safe text response from Gemini AI.

    Args:
        prompt (str): Input prompt to Gemini.

    Returns:
        str: Generated text or fallback message.
    """
    if not prompt.strip():
        return "⚠️ No input provided to Gemini."

    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"[Gemini API Error] {e}")
        return f"⚠️ Gemini error: {str(e)}"

def paraphrase_symptoms(symptoms: str) -> str:
    """
    Clarifies or rephrases user symptoms for internal processing.

    Args:
        symptoms (str): Raw symptom input.

    Returns:
        str: Clarified symptoms in English.
    """
    prompt = (
        "Rewrite the following user-provided medical symptoms clearly in English, "
        "without giving any diagnosis or medical advice:\n\n"
        f"{symptoms}"
    )
    return get_gemini_response(prompt)

def translate_text(text: str, target_lang: str = "en") -> str:
    """
    Translates user input to a target language using Gemini AI.

    Args:
        text (str): Input text.
        target_lang (str): Target language code (default 'en').

    Returns:
        str: Translated text.
    """
    if target_lang.lower() == "en":
        return paraphrase_symptoms(text)

    prompt = (
        f"Translate the following text to {target_lang}, keeping meaning accurate "
        f"and without giving any medical advice:\n\n{text}"
    )
    return get_gemini_response(prompt)


# -------------------- LOCAL TEST --------------------
if __name__ == "__main__":
    sample_symptoms = "headache, mild fever, and nausea for 2 days"
    print("Original Symptoms:", sample_symptoms)
    print("Paraphrased Symptoms:", paraphrase_symptoms(sample_symptoms))
    print("Translated Symptoms (to Spanish):", translate_text(sample_symptoms, "es"))
