import sys, os

# Adiciona o caminho absoluto da pasta 'scripts' ao PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from airflow.decorators import dag, task
from datetime import datetime
from scripts.extract import fetch_weather_data
from scripts.process import process_weather_data
from scripts.load import load_weather_data

# Lista de cidades para o pipeline
cities = ["São Paulo", "Rio de Janeiro", "Curitiba"]

# Defina o DAG
@dag(
    dag_id="weather_etl_dag",
    start_date=datetime(2025, 9, 18),
    schedule="0 9 * * *",
    catchup=False,
)
def weather_etl():
    @task
    def extract(city):
        return fetch_weather_data(city)

    @task
    def process(raw_data):
        return process_weather_data(raw_data)

    @task
    def load(data):
        return load_weather_data(data)

    for city in cities:
        raw = extract(city)
        processed = process(raw)
        load(processed)

weather_etl()