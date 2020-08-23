import requests
import json


API_KEY = "tJCdZW--kTTg"
PROJECT_TOKEN = "t_DySoSWgWyY"
RUN_TOKEN = "tRVY24_6Mi6n"

response = requests.get(f'https://www.parsehub.com/api/v2/projects/{PROJECT_TOKEN}/last_ready_run/data', params={"api_key": API_KEY})
data = json.loads(response.text)
print(data)