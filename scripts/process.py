import pandas as pd

def process_weather_data(raw_data):
    """
    Função para processar os dados meteorológicos.
    Aqui, por exemplo, podemos ajustar a unidade de temperatura de Kelvin para Celsius.
    """
    # Extraindo as informações de interesse
    name = raw_data['name']
    temperature_kelvin = raw_data['main']['temp']  # Temperatura em Kelvin
    humidity = raw_data['main']['humidity']  # Umidade relativa
    city_id = raw_data['id']  # Nome da cidade
    timestamp = pd.to_datetime(raw_data['dt'], unit='s') # Data de consulta
    longitude = raw_data['coord']['lon'] # Longitude da cidade
    latitude = raw_data['coord']['lat'] # Latitude da cidade
    country = raw_data['sys']['country'] # País da cidade
    windspeed = raw_data['wind']['speed'] # Velocidade do vento
    weather_condition = raw_data['weather'][0]['description'] # Condições climáticas
    precipitation = raw_data.get("rain", {}).get("1h", 0) # Nível de preipitação
    
    # Convertendo a temperatura de Kelvin para Celsius
    temperature_celsius = temperature_kelvin - 273.15

    # DataFrame para cities
    cities_df = pd.DataFrame([{
        'id': city_id,  # Renomeado para corresponder à coluna 'id' em cities
        'name': name,
        'country': country,
        'latitude': latitude,
        'longitude': longitude
    }])
    
    # DataFrame para weather_data
    weather_df = pd.DataFrame([{
        'city_id': city_id,
        'temperature': temperature_celsius,
        'humidity': humidity,
        'timestamp': timestamp,
        'windspeed': windspeed,
        'weather_condition': weather_condition,
        'precipitation': precipitation
    }])

    # Verifica nulos nas colunas obrigatórias (NOT NULL no schema)
    for df, cols in [
        (cities_df, ['id', 'name', 'country', 'latitude', 'longitude']),
        (weather_df, ['city_id', 'temperature', 'humidity', 'timestamp'])
    ]:
        if df[cols].isna().any().any():
            null_cols = df[cols].isna().any()[df[cols].isna().any()].index.tolist()
            raise ValueError(f"Valores nulos em colunas obrigatórias: {null_cols}")
    
    return (cities_df, weather_df) # Retorna os dataframes em uma tupla
