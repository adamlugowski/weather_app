from database import Database
from data import Station


def main():
    database = Database()
    database.db_init()
    station = Station('Wroclaw', 'pl')
    station.save_to_db(database)
    database.display_data()


if __name__ == '__main__':
    main()
