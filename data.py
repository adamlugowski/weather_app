import requests
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv('API_KEY')


class Station:
    def __init__(self, city, country):
        self.city = city
        self.country = country
        self.api_key = api_key

    def get_weather(self):
        weather_url = f'https://api.openweathermap.org/data/2.5/weather?q={self.city},{self.country}&APPID={self.api_key}'
        try:
            response = requests.get(weather_url)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
            return None

        result = response.json()
        weather_data = {}
        for key, value in result['main'].items():
            if key == 'temp':
                new_value = value - 273.15
                weather_data[key] = round(new_value, 2)
            elif key == 'humidity':
                weather_data[key] = value

        return weather_data

    def get_pollution(self):
        geo_url = f'https://api.openweathermap.org/geo/1.0/direct?q={self.city},{self.country}&limit=1&appid={self.api_key}'
        try:
            geo_response = requests.get(geo_url)
            geo_response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Error during geo request: {e}")
            return None
        geo_result = geo_response.json()
        lat = geo_result[0]['lat']
        lon = geo_result[0]['lon']
        air_pollution_url = f'https://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={self.api_key}'
        try:
            air_pollution_response = requests.get(air_pollution_url)
            air_pollution_response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Error during air pollution request: {e}")
            return None

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

    def save_to_db(self, db):
        weather_data = self.get_weather()
        pollution_level = self.get_pollution()
        if weather_data and pollution_level:
            db.insert_data_to_db(self.city, weather_data, pollution_level)
        else:
            print("Failed to retrieve weather or pollution data")
