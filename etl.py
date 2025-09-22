import requests
from datetime import datetime
from models import City, WeatherData, db,DailySummary
from sqlalchemy.sql import func
from scripts.config import Config

def fetch_weather_data(city_name):
    """Extrai dados da API do OpenWeatherMap, incluindo novos campos.""" 
    url = f"{Config.BASE_URL}?q={city_name}&appid={Config.API_KEY}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Erro ao buscar dados para {city_name}: {response.status_code}")

def process_weather_data(raw_data):
    """Transforma os dados extraídos, incluindo novos campos.""" 
    # Dados da cidade
    city_info = raw_data["sys"]  # Informações sobre o país
    weather_info = raw_data["weather"][0]  # Condição do tempo
    main_info = raw_data["main"]  # Temperatura e umidade
    wind_info = raw_data["wind"]  # Informações sobre o vento

    return {
        "temperature": main_info["temp"],  # Temperatura em Celsius
        "humidity": main_info["humidity"],  # Umidade
        "timestamp": datetime.fromtimestamp(raw_data["dt"]),  # Timestamp convertido para datetime
        "windspeed": wind_info["speed"],  # Velocidade do vento
        "weather_condition": weather_info["description"],  # Condição do tempo (ex: 'broken clouds')
        "precipitation": raw_data.get("rain", {}).get("1h", 0),  # Precipitação (caso exista)
        "country": city_info["country"],  # País (BR no caso)
        "latitude": raw_data["coord"]["lat"],  # Latitude
        "longitude": raw_data["coord"]["lon"],  # Longitude
    }

def load_weather_data(city_name, processed_data):
    """Carrega os dados no banco, incluindo novos campos.""" 
    # Verifica se a cidade já existe
    city = City.query.filter_by(name=city_name).first()
    if not city:
        city = City(
            name=city_name,
            country=processed_data["country"],
            latitude=processed_data["latitude"],
            longitude=processed_data["longitude"]
        )
        db.session.add(city)
        db.session.commit()

    # Adiciona os dados meteorológicos
    weather_data = WeatherData(
        city_id=city.id,
        temperature=processed_data["temperature"],
        humidity=processed_data["humidity"],
        timestamp=processed_data["timestamp"],
        windspeed=processed_data["windspeed"],
        weather_condition=processed_data["weather_condition"],
        precipitation=processed_data["precipitation"]
    )
    db.session.add(weather_data)
    db.session.commit()


def generate_daily_summary():
    """
    Gera resumos diários por cidade e insere na tabela 'daily_summary'.
    """
    # Consulta para calcular média e contagem por cidade e data
    summaries = (
        db.session.query(
            WeatherData.city_id,
            func.date(WeatherData.timestamp).label('date'),
            func.avg(WeatherData.temperature).label('avg_temperature'),
            func.avg(WeatherData.humidity).label('avg_humidity'),
            func.count(WeatherData.id).label('record_count')
        )
        .group_by(WeatherData.city_id, func.date(WeatherData.timestamp))
        .all()
    )

    # Inserindo os resumos na tabela DailySummary
    for summary in summaries:
        existing_summary = DailySummary.query.filter_by(
            city_id=summary.city_id, date=summary.date
        ).first()

        if not existing_summary:
            daily_summary = DailySummary(
                city_id=summary.city_id,
                date=summary.date,
                avg_temperature=summary.avg_temperature,
                avg_humidity=summary.avg_humidity,
                record_count=summary.record_count
            )
            db.session.add(daily_summary)
    
    db.session.commit()
