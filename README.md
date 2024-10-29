# Weather Station Project with pollution level

This project involves building a weather station that provides real-time weather data along with air quality info (pollution_level) using data from OpenWeatherMap. The data is stored in a PostgreSQL database and the project utilizes `python-dotenv` for managing environment variables.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Setup and Installation](#setup-and-installation)
- [Usage](#usage)
- [Database Schema](#database-schema)
- [Contributing](#contributing)

## Introduction

The Weather Station Project is designed to collect and display real-time weather data, including temperature, humidity, and air quality (pollution level). By leveraging the OpenWeatherMap API, the application fetches current weather conditions and air pollution data, which is then stored in a PostgreSQL database. 

## Features

- **Real-time Weather Data**: Fetches current weather data from OpenWeatherMap API.
- **Air Quality Indices**: Retrieves air pollution data (pollution_level) from OpenWeatherMap API.
- **Data Storage**: Stores weather and air quality data in a PostgreSQL database.
- **Environment Variable Management**: Utilizes `python-dotenv` to manage API keys and database credentials securely.

## Technologies Used

- **Programming Language**: Python 3.11
- **APIs**: OpenWeatherMap
- **Database**: PostgreSQL
- **Libraries**:
  - `requests`
  - `psycopg2`
  - `python-dotenv`

## Setup and Installation

### Prerequisites

- Python 3.x
- PostgreSQL
- OpenWeatherMap API Key

### Installation

1. **Clone the repository**:
    ```bash
    git clone https://github.com/adamlugowski/weather-station.git
    cd weather-station
    ```

2. **Create and activate a virtual environment**:
    ```bash
    python -m venv venv
    source venv/bin/activate   # On Windows use `venv\Scripts\activate`
    ```

3. **Install the required packages**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Set up environment variables**:
    - Create a `.env` file in the project root directory and add the following variables:
      ```env
      OPENWEATHERMAP_API_KEY=your_api_key_here
      DATABASE_URL=postgresql://username:password@localhost:5432/weather_db
      ```

5. **Initialize the database**:
    - Create the database and table using the provided schema (see [Database Schema](#database-schema) section).

## Usage

1. **Run the script**:
    ```bash
    python main.py
    ```

## Database Schema

The PostgreSQL database schema for storing weather and air quality data includes the following table:

- **weather_data**:
  - `id` (Primary Key)
  - `city` (Text)
  - `temperature` (Float)
  - `humidity` (Float)
  - `pollution_level` (Text)
  - `created_at` (Datetime)

## Contributing

Contributions are welcome! Please fork this repository and submit a pull request for any improvements or bug fixes.
