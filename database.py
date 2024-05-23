import psycopg2
from dotenv import load_dotenv
import os
from datetime import datetime

load_dotenv()

db_name = os.getenv('DB_NAME')
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')
db_host = os.getenv('DB_HOST')
db_port = os.getenv('DB_PORT')


def db_init():
    connection = psycopg2.connect(
        dbname=db_name,
        user=db_user,
        password=db_password,
        host=db_host,
        port=db_port
    )
    cursor = connection.cursor()
    cursor.execute('''create table if not exists weather_data(
            id serial primary key, 
            city varchar(255), 
            temperature float, 
            humidity float, 
            pollution_level varchar(50), 
            created_at timestamp);''')
    connection.commit()
    connection.close()


def insert_data_to_db(weather_data, pollution_level):
    today = datetime.today()
    try:
        connection = psycopg2.connect(
            dbname=db_name,
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port
        )
        cursor = connection.cursor()
        cursor.execute('''
            INSERT INTO weather_data(city, temperature, humidity, pollution_level, created_at)
            VALUES (%s, %s, %s, %s, %s)
            ''', ('Wroclaw', weather_data['temp'], weather_data['humidity'], pollution_level, today.strftime('%d/%m/%y')))

        connection.commit()
    except Exception as error:
        print(f"Error: {error}")
    finally:
        if connection:
            cursor.close()
            connection.close()

