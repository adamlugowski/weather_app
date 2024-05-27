import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

db_name = os.getenv('DB_NAME')
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')
db_host = os.getenv('DB_HOST')
db_port = os.getenv('DB_PORT')


def db_init():
    try:
        with psycopg2.connect(
            dbname=db_name,
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port
        ) as connection:
            cursor = connection.cursor()
            cursor.execute('''create table if not exists weather_data(
                    id serial primary key, 
                    city varchar(255), 
                    temperature float, 
                    humidity float, 
                    pollution_level varchar(50), 
                    created_at timestamp);''')
            connection.commit()
    except psycopg2.DatabaseError as e:
        print(f"A database error occurred: {e}")


def insert_data_to_db(weather_data, pollution_level):
    try:
        with psycopg2.connect(
            dbname=db_name,
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port
        ) as connection:
            cursor = connection.cursor()
            cursor.execute('''
                INSERT INTO weather_data(city, temperature, humidity, pollution_level, created_at)
                VALUES (%s, %s, %s, %s, CURRENT_TIMESTAMP)
                ''', ('Wroclaw', weather_data['temp'], weather_data['humidity'], pollution_level))

            connection.commit()
    except psycopg2.Error as error:
        print(f"Error: {error}")
        raise error
    finally:
        if connection:
            cursor.close()
            connection.close()

