import requests


from config import Config




def fetch_weather_data(city_name):
    """
    Função para buscar os dados meteorológicos de uma cidade via API.
    """
    params = {'q': city_name, 'appid': Config.API_KEY, 'units': 'metric'}  # 'metric' para obter a temperatura em Celsius
    response = requests.get(Config.BASE_URL, params=params)
    
    if response.status_code == 200:
        return response.json()  # Retorna os dados em formato JSON
    else:
        raise Exception(f"Erro ao buscar dados para a cidade {city_name}: {response.status_code}")
