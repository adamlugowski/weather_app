import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

db_name = os.getenv('DB_NAME')
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')
db_host = os.getenv('DB_HOST')
db_port = os.getenv('DB_PORT')


class Database:
    def __init__(self):
        self.db_name = os.getenv('DB_NAME')
        self.db_user = os.getenv('DB_USER')
        self.db_password = os.getenv('DB_PASSWORD')
        self.db_host = os.getenv('DB_HOST')
        self.db_port = os.getenv('DB_PORT')
        self.connection = None

    def connect(self):
        try:
            self.connection = psycopg2.connect(
                    dbname=self.db_name,
                    user=self.db_user,
                    password=self.db_password,
                    host=self.db_host,
                    port=self.db_port)
        except psycopg2.DatabaseError as e:
            print(f"A database error occurred: {e}")

    def close(self):
        if self.connection:
            self.connection.close()
            self.connection = None

    def db_init(self):
        """
        Initialize the database by creating the weather_data table if it does not exist
        """
        try:
            self.connect()
            with self.connection.cursor() as cursor:
                cursor.execute('''create table if not exists weather_data(
                        id serial primary key, 
                        city varchar(255), 
                        temperature float, 
                        humidity float, 
                        pollution_level varchar(50), 
                        created_at timestamp);''')
            self.connection.commit()
        except psycopg2.DatabaseError as e:
            print(f"A database error occurred: {e}")
            raise
        finally:
            self.close()

    def insert_data_to_db(self, city, weather_data, pollution_level):
        """
        Insert weather data and pollution level into the database for a specific city.
        
        Args:
            city (str): The name of the city.
            weather_data (dict): Dictionary containing temperature and humidity data.
            pollution_level (int): The pollution level for the city.
        """
        try:
            self.connect()
            with self.connection.cursor() as cursor:
                cursor.execute('''
                    INSERT INTO weather_data(city, temperature, humidity, pollution_level, created_at)
                    VALUES (%s, %s, %s, %s, CURRENT_TIMESTAMP)
                    ''', (city, weather_data['temp'], weather_data['humidity'], pollution_level))

            self.connection.commit()
        except psycopg2.Error as error:
            print(f"Error: {error}")
            raise
        finally:
            self.close()
