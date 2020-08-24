import pyttsx3
import speech_recognition as sr

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def getAudio():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        audio = recognizer.listen(source)
        said = ""
        try:
            said = recognizer.recognize_google(audio)
        except Exception as e:
            print("Sorry, I didn't get that. Can you try again? Or say stop to terminate the program!")

    return said.lower()

