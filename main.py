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



def main():
    print("Starting COVID-19 Tracker and Predictor Voice Assistant :]")
    print("NOTE: Say STOP to stop the program!")

    data = Data(API_KEY, PROJECT_TOKEN)

    #potential phrases
    END = 'STOP'
    TOTAL_PATT = {
        re.compile("[\w\s]+ total [\w\s]+ cases"): data.getTotalCases,
        re.compile("[\w\s]+ total cases "): data.getTotalCases,
        re.compile("[\w\s]+ total [\w\s]+ cases [\w\s]+"): data.getTotalCases,
        re.compile("[\w\s]+ total cases [\w\s]+"): data.getTotalCases,

        re.compile("[\w\s]+ total [\w\s]+ deaths"): data.getTotalDeaths(),
        re.compile("[\w\s]+ total deaths"): data.getTotalDeaths(),
        re.compile("[\w\s]+ total [\w\s]+ deaths [\w\s]+"): data.getTotalDeaths(),
        re.compile("[\w\s]+ total deaths [\w\s]+"): data.getTotalDeaths(),

        re.compile("[\w\s]+ total [\w\s]+ recoveries "): data.getTotalRecovered(),
        re.compile("[\w\s]+ total recoveries"): data.getTotalRecovered(),
        re.compile("[\w\s]+ total [\w\s]+ recoveries [\w\s]+"): data.getTotalRecovered(),
        re.compile("[\w\s]+ total recoveries [\w\s]+"): data.getTotalRecovered()
    }

    COUNTRY_PATT = {
        re.compile("[\w\s]+ cases [\w\s]+"): lambda country: data.getCountryData(country)['total_cases']
    }


    while True:
        print("\nListening: ")
        text = getAudio()
        result = None

        for pattern, func in TOTAL_PATT.items():
            if pattern.match(text):
                result = func()
                break

        if result:
            speak(result)

        if text.find(END) != -1:
            break

main()
