import speech_recognition as sr

# Initialize recognizer
recognizer = sr.Recognizer()
recognizer.pause_threshold = 1.5  # Allow longer pause before stopping (default is 0.8)
recognizer.energy_threshold = 300  # May need tuning depending on your mic environment

def SpeechToText():
    with sr.Microphone() as source:
        print("Say something...")

        # Optionally adjust for ambient noise
        recognizer.adjust_for_ambient_noise(source, duration=1)

        try:
            # Listen with a timeout (optional) and phrase time limit (optional)
            audio = recognizer.listen(source, timeout=5)  # Increase timeout if needed
            text = recognizer.recognize_google(audio)
            return text
        except sr.UnknownValueError:
            print("Sorry, I could not understand the audio.")
        except sr.RequestError as e:
            print(f"Could not request results; {e}")
        except Exception as e:
            print(f"An error occurred: {e}")
