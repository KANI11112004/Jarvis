import speech_recognition as sr

# Initialize recognizer
recognizer = sr.Recognizer()

def SpeechToText():
    # Use the microphone
    with sr.Microphone() as source:
        print("Say something...")
        audio = recognizer.listen(source)

        try:
            # Convert speech to text using Google's API
            text = recognizer.recognize_google(audio)
            return text
        except sr.UnknownValueError:
            print("Sorry, I could not understand the audio.")
        except sr.RequestError as e:
            print(f"Could not request results; {e}")
        except Exception as e:
            print(f"An error occurred: {e}")