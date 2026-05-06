import speech_recognition as sr

# -------------------------------------------------
# Voice Capture Utility
# -------------------------------------------------
def capture_symptom_voice() -> str:
    """
    Captures voice input from the user and converts it to text using Google Speech Recognition.

    Returns:
        str: Transcribed text from speech input.
             Returns an empty string if audio is unclear or recognition fails.
    """
    recognizer = sr.Recognizer()

    try:
        with sr.Microphone() as source:
            print("🎤 Please speak your symptoms clearly...")
            recognizer.adjust_for_ambient_noise(source, duration=1)  # reduce noise
            audio = recognizer.listen(source, timeout=10, phrase_time_limit=15)
    except Exception as e:
        print(f"⚠️ Microphone error: {e}")
        return ""

    try:
        text = recognizer.recognize_google(audio)
        print(f"✅ You said: {text}")
        return text.strip()
    except sr.UnknownValueError:
        print("⚠️ Sorry, could not understand the audio.")
        return ""
    except sr.RequestError as e:
        print(f"⚠️ Could not request results from Google Speech Recognition service; {e}")
        return ""
