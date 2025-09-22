class Config:
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://airflow:airflow@mysql:3306/weather_db' # Endereço do banco de dados
    SQLALCHEMY_TRACK_MODIFICATIONS = False # Desativa o rastreamento de modificações
    API_KEY = '4ca56aa5b0eec444c9fee770b077517f' # Chave da API da OpenWeather
    BASE_URL = 'https://api.openweathermap.org/data/2.5/weather' # Endereço da OpenWeather