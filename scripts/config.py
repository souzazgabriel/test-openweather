import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://airflow:airflow@localhost:3306/weather_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    API_KEY = os.getenv('OPENWEATHER_API_KEY', '4ca56aa5b0eec444c9fee770b077517f')
    BASE_URL = 'https://api.openweathermap.org/data/2.5/weather'
