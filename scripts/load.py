from sqlalchemy import create_engine
from airflow.hooks.base import BaseHook
import pandas as pd

from scripts.config import Config

# Criação de conexão com o banco de dados MySQL
#engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)

def load_weather_data(processed_data):
    conn=BaseHook.get_connection('weather_mysql')
    engine = create_engine(f"mysql+pymysql://{conn.login}:{conn.password}@{conn.host}:{conn.port}/{conn.schema}")
    """
    Função para carregar os dados no banco de dados MySQL.
    """
    try:
        processed_data.to_sql('weather_data', con=engine, if_exists='append', index=False)
        print("Dados inseridos com sucesso!")
    except Exception as e:
        raise Exception(f"Erro ao inserir dados no banco de dados: {str(e)}")
