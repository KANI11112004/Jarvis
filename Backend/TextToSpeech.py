import pyttsx3

def TextToSpeech(text: str, rate: int = 150, volume: float = 1.0, voice_index: int = 0):
    engine = pyttsx3.init()
    engine.setProperty('rate', rate)
    engine.setProperty('volume', volume)
    
    voices = engine.getProperty('voices')
    if 0 <= voice_index < len(voices):
        engine.setProperty('voice', voices[voice_index].id)
    
    engine.say(text)
    engine.runAndWait()
