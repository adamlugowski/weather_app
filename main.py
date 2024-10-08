from database import Database
from data import Station


def main():
    database = Database()
    database.db_init()
    city = input('Enter city name to check weather: ').strip().lower().capitalize()
    station = Station(city, 'pl')
    if station.is_valid_city_name(city):
        station.save_to_db(database)
        station.display_weather_data(city)
    else:
        print('Invalid city name. Please try again. ')


if __name__ == '__main__':
    main()
