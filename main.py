from database import db_init, insert_data_to_db
from data import get_pollution, get_weather


if __name__ == '__main__':
    db_init()
    insert_data_to_db(get_weather(), get_pollution())
