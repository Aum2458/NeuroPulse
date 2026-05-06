import sounddevice as sd
from scipy.io.wavfile import write
import speech_recognition as sr

fs = 44100  # Sample rate
seconds = 5  # Duration of recording

print("🎤 Speak now...")

try:
    # Record audio
    recording = sd.rec(int(seconds * fs), samplerate=fs, channels=1, dtype='int16')
    sd.wait()
    write("output.wav", fs, recording)
    print("✅ Audio recorded and saved as output.wav")

    # Convert to text
    recognizer = sr.Recognizer()
    with sr.AudioFile("output.wav") as source:
        audio = recognizer.record(source)
        try:
            print("🗣️ You said:", recognizer.recognize_google(audio))
        except sr.UnknownValueError:
            print("⚠️ Could not understand the audio.")
        except sr.RequestError as e:
            print(f"❌ API error: {e}")

except Exception as e:
    print(f"❌ Error: {e}")
