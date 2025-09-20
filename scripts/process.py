import pandas as pd

def process_weather_data(raw_data):
    """
    Função para processar os dados meteorológicos.
    Aqui, por exemplo, podemos ajustar a unidade de temperatura de Kelvin para Celsius.
    """
    # Extraindo as informações de interesse
    temperature_kelvin = raw_data['main']['temp']  # Temperatura em Kelvin
    humidity = raw_data['main']['humidity']  # Umidade relativa
    city_name = raw_data['name']  # Nome da cidade
    
    # Convertendo a temperatura de Kelvin para Celsius
    temperature_celsius = temperature_kelvin - 273.15
    
    # Processando os dados em um DataFrame para facilitar o manuseio
    weather_df = pd.DataFrame([{
        'city': city_name,
        'temperature': temperature_celsius,
        'humidity': humidity,
    }])
    
    return weather_df
