import requests
from dotenv import load_dotenv
import os


def get_weather():
    load_dotenv()
    api_key = os.getenv('API_KEY')
    url = f'https://api.openweathermap.org/data/2.5/weather?q=Wroclaw,pl&APPID={api_key}'
    response = requests.get(url)
    result = response.json()
    town_weather = {}
    for key, value in result['main'].items():
        if key == 'temp':
            new_value = value - 273.15
            town_weather[key] = round(new_value, 2)
        elif key == 'humidity':
            town_weather[key] = value

    print(town_weather)


get_weather()
