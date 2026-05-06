from deep_translator import GoogleTranslator

# -------------------------------------------------
# Translation Utility
# -------------------------------------------------
def translate_text(text: str, target_lang: str = 'en') -> str:
    """
    Translates input text to the target language using GoogleTranslator.
    Handles multilingual input including Hindi, Gujarati, and other scripts.

    Args:
        text (str): Input text to be translated (can be in any language).
        target_lang (str): Target language code (default 'en' for English).

    Returns:
        str: Translated text, or original input if translation fails.
    """
    if not text or not text.strip():
        return ""

    try:
        translator = GoogleTranslator(source='auto', target=target_lang)
        translated = translator.translate(text)
        return translated.strip()
    except Exception as e:
        print(f"[Translation Error] {e}")
        return text.strip()  # fallback to original input
