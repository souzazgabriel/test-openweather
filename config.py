import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://victor:Stevengerr%40rd8!@localhost/weather_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    API_KEY = os.getenv('OPENWEATHER_API_KEY', 'c382ff3939ee26d23fefdb72347fdbdd')
    BASE_URL = 'https://api.openweathermap.org/data/2.5/weather'
