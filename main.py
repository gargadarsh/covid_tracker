import requests
import json
import pyttsx3
import speech_recognition as sr
import re

import threading
from time import sleep

import config


class Data:
    def __init__(self, api_key, project_token):
        self.api_key = api_key
        self.project_token = project_token
        self.params = {
            "api_key": self.api_key
        }
        self.data = self.getData()

    def getData(self):
        response = requests.get(f'https://www.parsehub.com/api/v2/projects/{self.project_token}/last_ready_run/data',
                                params=self.params)
        data = json.loads(response.text)
        return data

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

    def updateData(self):
        response = requests.post(f'https://www.parsehub.com/api/v2/projects/{config.PROJECT_TOKEN}/run',
                                params=self.params)
        oldData = self.data

        def pull():
            sleep(0.1)
            check = True
            while check:
                newData = self.getData()
                if newData != oldData:
                    self.data = newData
                    print("Data Updated!")
                    check = False
                sleep(5)


        thread = threading.Thread(target=pull)
        thread.start()




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

    data = Data(config.API_KEY, config.PROJECT_TOKEN)
    countries = data.getListOfCountries()


    #potential phrases
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
        re.compile("[\w\s]+ cases [\w\s]+"): lambda country: data.getCountryData(country)['total_cases'],
        re.compile("[\w\s]+ deaths [\w\s]+"): lambda country: data.getCountryData(country)['total_deaths'],

        re.compile("[\w\s]+ recovered [\w\s]+"): lambda country: data.getCountryData(country)['total_recoveries'],
        re.compile("[\w\s]+ recoveries [\w\s]+"): lambda country: data.getCountryData(country)['total_recoveries']
    }

    UPDATE_PATT = "update"


    while True:
        print("\nListening: ")
        text = getAudio()
        result = None


        #for outputting country specific data
        for pattern, func in COUNTRY_PATT.items():
            if pattern.match(text):
                words = list(text.split(" "))
                for country in countries:
                    if country in words:
                        result = func(country)
                        break


        #for outputting total
        for pattern, func in TOTAL_PATT.items():
            if pattern.match(text):
                result = func()
                break

        #to update data
        if text == UPDATE_PATT:
            print("Data is being updated... This may take a while...")
            speak("Data is being updated... This may take a while...")
            data.updateData()
            print("Data is up to date!")
            speak("Data is up to date")




        if result:
            speak(result)

        if text.find("stop") != -1:
            print("Program has stopped")
            break

main()
