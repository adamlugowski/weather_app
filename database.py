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
    """
    A class to manage PostgreSQL database connection, setup, and data insertion for weather-related information.

    This class uses environment variables to establish a connection to a PostgreSQL database and provides methods
    to initialize the database with a weather_data table, as well as insert new weather data entries.

    Attributes:
    ----------
    db_name : str
        The name of the PostgreSQL database, obtained from environment variables.
    db_user : str
        The PostgreSQL database username, obtained from environment variables.
    db_password : str
        The password for the PostgreSQL user, obtained from environment variables.
    db_host : str
        The host address for the PostgreSQL database, obtained from environment variables.
    db_port : str
        The port number for the PostgreSQL database, obtained from environment variables.
    connection : psycopg2.connection or None
        The current database connection object, initially set to None.

    Methods:
    -------
    connect():
        Establishes a connection to the PostgreSQL database using credentials specified in environment variables.
        Handles any database errors that may occur.

    close():
        Closes the current database connection if it exists and sets the connection attribute to None.

    db_init():
        Initializes the database by creating the weather_data table if it does not already exist. The table
        includes fields for city, temperature, humidity, pollution level, and a timestamp indicating when
        the data was recorded. Commits the changes if successful and handles database errors.

    insert_data_to_db(city, weather_data, pollution_level):
        Inserts weather data and pollution level information into the weather_data table for a specified city.

        Args:
            city (str): The name of the city.
            weather_data (dict): A dictionary containing 'temp' (temperature) and 'humidity' values.
            pollution_level (str): A description of the pollution level for the city.

        Handles any database errors and closes the connection after the insertion.
    """
    def __init__(self):
        self.db_name = os.getenv('DB_NAME')
        self.db_user = os.getenv('DB_USER')
        self.db_password = os.getenv('DB_PASSWORD')
        self.db_host = os.getenv('DB_HOST')
        self.db_port = os.getenv('DB_PORT')
        self.connection = None

    def connect(self):
        """
        This method is for establishing the connection using the environment variables.
        """
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
        """
        This method is for closing the connection
        """
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
        finally:
            self.close()
