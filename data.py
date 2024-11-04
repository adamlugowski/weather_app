import requests
from dotenv import load_dotenv
import os
import re

load_dotenv()
api_key = os.getenv('API_KEY')


class Station:
    """
    A class to manage weather and pollution data retrieval for a specific city and country using the OpenWeatherMap API.

    The Station class allows users to verify valid city names, retrieve current weather and pollution data,
    and save this information to a database. It uses the OpenWeatherMap API to fetch weather and air quality data
    and supports error handling for API requests and database operations.

    Attributes:
    ----------
    city : str
        The name of the city for which weather and pollution data is requested.
    country : str
        The country code for the specified city.
    api_key : str
        The API key used for accessing the OpenWeatherMap API, sourced from environment variables.

    Methods:
    -------
    is_valid_city_name(city_name):
        Checks if the input city name is valid, containing only letters and spaces, and not exceeding 50 characters.

    get_weather():
        Fetches the current weather data (temperature in Celsius and humidity) for the specified city and country.

    get_pollution():
        Retrieves the air pollution level for the specified city and country based on geographical coordinates.

    save_to_db(db):
        Saves the retrieved weather and pollution data for the city to a database if both data points are available.

    display_weather_data(city_name):
        Displays the current temperature and air quality level for the requested city.

    """
    def __init__(self, city, country):
        self.city = city
        self.country = country
        self.api_key = api_key

    def is_valid_city_name(self, city_name):
        """
        This method checks if the user input is a non-empty string
        containing valid characters and is not longer than 50 letters.

        Args:
            city_name: name of city from user input
        """
        if not city_name:
            print('City name cannot be empty. ')
            return False
        if not re.match("^[A-Za-zĄĆĘŁŃÓŚŻŹąćęłńóśżź ]+$", city_name):
            print('City name can only contain letters and spaces. ')
            return False
        if len(city_name) > 50:
            print('City name is too long. ')
            return False
        else:
            return True

    def get_weather(self):
        """
        This method fetches the current weather data for a specified city and country using the OpenWeatherMap API.
        It processes the temperature and humidity data, converting the temperature from Kelvin to Celsius.
        """
        weather_url = f'https://api.openweathermap.org/data/2.5/weather?q={self.city},{self.country}&APPID={self.api_key}'
        try:
            response = requests.get(weather_url)
            result = response.json()
            if result.get('cod') == '404':
                print(f"Error: City '{self.city}' not found.")
                return None
            if not result:
                print(f"Error: No geographical data found for the city '{self.city}'")
                return None

            weather_data = {}
            for key, value in result['main'].items():
                if key == 'temp':
                    new_value = value - 273.15
                    weather_data[key] = round(new_value, 2)
                elif key == 'humidity':
                    weather_data[key] = value

            return weather_data

        except requests.exceptions.RequestException as error:
            print(f"Error: {error}")
            return None

        except requests.exceptions.HTTPError as http_error:
            print(f'HTTP error occurred: {http_error}')
            return None

    def get_pollution(self):
        """
        This method retrieves the air pollution level for a specified city and country by first obtaining
        the geographical coordinates (latitude and longitude)
        and then querying the air pollution data using these coordinates
        """
        geo_url = f'https://api.openweathermap.org/geo/1.0/direct?q={self.city},{self.country}&limit=1&appid={self.api_key}'
        air_pollution_url = None
        try:
            geo_response = requests.get(geo_url)
            geo_response.raise_for_status()
            geo_result = geo_response.json()
            if not geo_result:
                print(f"Error: No geographical data found for the city '{self.city}'.")
                return None
            lat = geo_result[0]['lat']
            lon = geo_result[0]['lon']
            air_pollution_url = f'https://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={self.api_key}'
            air_pollution_response = requests.get(air_pollution_url)
            air_pollution_response.raise_for_status()
            air_pollution_result = air_pollution_response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error during API request: {e}")
            return None
        except IndexError:
            print(f"No geographical data found for the city '{self.city}'")

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
        """
        This method checks if weather and pollution data is accessible for requested city.
        Afterward it retrieves weather and pollution data for a specific city and country
        and then saves this data to a database.

        Args:
            db: instance of Database class
        """
        weather_data = self.get_weather()
        pollution_level = self.get_pollution()
        if weather_data is None or pollution_level is None:
            print(f"Error: Failed to retrieve data for {self.city}. Data not saved.")
            return
        try:
            if weather_data and pollution_level:
                db.insert_data_to_db(self.city, weather_data, pollution_level)
        except Exception as e:
            print(f"Error while inserting data to the database: {e}")

    def display_weather_data(self, city_name):
        """
        Displaying current weather for requested city.

        Args:
            city_name: name of city from user input
        """
        pollution_level = self.get_pollution()
        weather_data = self.get_weather()
        try:
            temperature = weather_data.get('temp')
            print(f'Temperature in {city_name} is {temperature} Celcius. Air quality is {pollution_level.lower()}. ')
        except AttributeError as error:
            print(f"Error: No geographical data found for the city '{self.city}'. ")

