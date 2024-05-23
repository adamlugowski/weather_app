import requests
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv('API_KEY')


def get_weather():
    weather_url = f'https://api.openweathermap.org/data/2.5/weather?q=Wroclaw,pl&APPID={api_key}'
    response = requests.get(weather_url)
    result = response.json()
    weather_data = {}
    for key, value in result['main'].items():
        if key == 'temp':
            new_value = value - 273.15
            weather_data[key] = round(new_value, 2)
        elif key == 'humidity':
            weather_data[key] = value

    return weather_data


def get_pollution():
    geo_url = f'https://api.openweathermap.org/geo/1.0/direct?q=Wroclaw,pl&limit=1&appid={api_key}'
    geo_response = requests.get(geo_url)
    geo_result = geo_response.json()
    lat = geo_result[0]['lat']
    lon = geo_result[0]['lon']
    air_pollution_url = f'https://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={api_key}'
    air_pollution_response = requests.get(air_pollution_url)
    air_pollution_result = air_pollution_response.json()
    pollution_level = None
    for main in air_pollution_result['list']:
        for key, value in main.items():
            if key == 'main':
                aqi = value['aqi']
                match aqi:
                    case 1:
                        pollution_level = 'Excellent'
                    case 2:
                        pollution_level = 'Good'
                    case 3:
                        pollution_level = 'Lightly polluted'
                    case 4:
                        pollution_level = 'Moderately polluted'
                    case 5:
                        pollution_level = 'Heavily polluted'
                    case _:
                        pollution_level = 'Unknown'
                break
        break

    return pollution_level
