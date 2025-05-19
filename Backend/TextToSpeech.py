import pyttsx3
import threading

def speak_text(text):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    for voice in voices:
        if "Ravi" in voice.name or "India" in voice.name:
            engine.setProperty('voice', voice.id)
            break

    engine.setProperty('rate', 170)
    engine.setProperty('volume', 1.0)
    engine.say(text)
    engine.runAndWait()

def TextToSpeech(text):
    t = threading.Thread(target=speak_text, args=(text,))
    t.start()
