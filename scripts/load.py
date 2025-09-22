from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError
from airflow.hooks.base import BaseHook
from scripts.config import Config

def load_weather_data(processed_data):
    # Criação de conexão com o banco de dados MySQL
    engine = create_engine(f"{Config.SQLALCHEMY_DATABASE_URI}")
    """
    Função para carregar os dados no banco de dados MySQL.
    """

    # Desempacotamento da tupla
    cities_df, weather_df = processed_data

    try:
        try:
            cities_df.to_sql('cities', con=engine, if_exists='append', index=False)
        except IntegrityError as e:
            pass # Ignora se cidade já existe
        weather_df.to_sql('weather_data', con=engine, if_exists='append', index=False)
        print("Dados inseridos com sucesso!")
    except Exception as e:
        raise Exception(f"Erro ao inserir dados no banco de dados: {str(e)}")
