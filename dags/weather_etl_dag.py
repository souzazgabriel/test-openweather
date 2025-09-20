import sys
import os

# Adiciona o caminho absoluto da pasta 'scripts' ao PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '.', 'scripts')))

from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
from scripts.extract import fetch_weather_data
from scripts.process import process_weather_data
from scripts.load import load_weather_data

# Lista de cidades para o pipeline
cities = ["São Paulo", "Rio de Janeiro", "Curitiba"]

# Defina o DAG
with DAG(
    dag_id='weather_etl_dag',
    default_args={
        'owner': 'airflow',
        'retries': 1,
    },
    description='ETL de dados meteorológicos',
    schedule_interval='0 9 * * *',  # Executa diariamente às 9h
    start_date=datetime(2024, 12, 1),
    catchup=False,
) as dag:

    # Dicionário para armazenar as tarefas de cada cidade
    tasks = {}

    for city in cities:
        # Tarefa de extração
        extract_task = PythonOperator(
            task_id=f'extract_weather_data_{city.replace(" ", "_").lower()}',
            python_callable=fetch_weather_data,
            op_args=[city],  # Passa a cidade como argumento
        )

        # Tarefa de processamento
        process_task = PythonOperator(
            task_id=f'process_weather_data_{city.replace(" ", "_").lower()}',
            python_callable=process_weather_data,
        )

        # Tarefa de carga
        load_task = PythonOperator(
            task_id=f'load_weather_data_{city.replace(" ", "_").lower()}',
            python_callable=load_weather_data,
        )

        # Definindo a ordem das tarefas
        extract_task >> process_task >> load_task

        # Salvando tarefas no dicionário
        tasks[city] = {
            'extract': extract_task,
            'process': process_task,
            'load': load_task,
        }

