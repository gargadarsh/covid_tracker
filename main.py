import requests
import json
import pyttsx3
import speech_recognition as sr
import re

API_KEY = "tJCdZW--kTTg"
PROJECT_TOKEN = "t_DySoSWgWyY"
RUN_TOKEN = "tRVY24_6Mi6n"

class Data:
    def __init__(self, api_key, project_token):
        self.api_key = api_key
        self.project_token = project_token
        self.params = {
            "api_key": self.api_key
        }
        self.getData()

    def getData(self):
        response = requests.get(f'https://www.parsehub.com/api/v2/projects/{PROJECT_TOKEN}/last_ready_run/data',
                                params={"api_key": API_KEY})
        self.data = json.loads(response.text)

    def getTotalCases(self):
        data = self.data['total']

        for item in data:
            if item['name'] == "Coronavirus Cases:":
                return item['value']

    def getTotalDeaths(self):
        data = self.data['total']

        for item in data:
            if item['name'] == "Deaths:":
                return item['value']
        return "None"

    def getTotalRecovered(self):
        data = self.data['total']

        for item in data:
            if item['name'] == "Recovered:":
                return item['value']

    def getCountryData(self, country):
        data = self.data['country']
        for item in data:
            if item['name'].lower() == country.lower():
                return item
        return "None"

    def getListOfCountries(self):
        countries = []
        for country in self.data['country']:
            countries.append(country['name'].lower())
        return countries

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
            print("Exceptions: ", str(e))

    return said.lower()


data = Data(API_KEY, PROJECT_TOKEN)


def main():
    print("Starting COVID-19 Tracker and Predictor Voice Assistant :]")
    print("NOTE: Say STOP to stop the program!")
    END_PHRASE = 'STOP'


    while True:
        print("Listening: ")
        text = getAudio()

        if text.find(END_PHRASE):
            break

print(data.getListOfCountries())
