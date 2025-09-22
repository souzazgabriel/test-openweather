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
    timestamp = pd.to_datetime(raw_data['dt'], unit='s')
    longitude = raw_data['coord']['lon']
    latitude = raw_data['coord']['lat']
    country = raw_data['sys']['country']
    windspeed = raw_data['wind']['speed']
    weather_condition = raw_data['weather'][0]['description']
    precipitation = raw_data.get("rain", {}).get("1h", 0)
    
    # Convertendo a temperatura de Kelvin para Celsius
    temperature_celsius = temperature_kelvin - 273.15
    print(temperature_celsius)
    cities_df = pd.DataFrame([{
        'id': city_id,  # Renomeado para corresponder à coluna 'id' em cities
        'name': name,
        'country': country,
        'latitude': latitude,
        'longitude': longitude
    }])
    
    # Processando os dados em um DataFrame para facilitar o manuseio
    weather_df = pd.DataFrame([{
        'city_id': city_id,
        'temperature': temperature_celsius,
        'humidity': humidity,
        'timestamp': timestamp,
        'windspeed': windspeed,
        'weather_condition': weather_condition,
        'precipitation': precipitation
    }])
    
    return (cities_df, weather_df)
