import requests
import json
import threading
from time import sleep

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
        response = requests.post(f'https://www.parsehub.com/api/v2/projects/{self.project_token}/run',
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
