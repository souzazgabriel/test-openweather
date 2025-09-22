# Plano de Integração de Dados Meteorológicos

## Estrutura do Pipeline ETL

- **Extração**: Consome dados da API OpenWeatherMap para cidades (São Paulo, Rio de Janeiro, Curitiba) usando `requests` com `units=metric` para temperaturas em Celsius (`etl.py`).
- **Transformação**: Processa dados com Pandas, extraindo `id`, `name`, `country`, `latitude`, `longitude` para `cities` e `city_id`, `temperature`, `humidity`, `timestamp`, `windspeed`, `weather_condition`, `precipitation` para `weather_data`. Retorna dois DataFrames em uma tupla (`process.py`).
- **Carga**: Insere em tabelas MySQL (`cities` e `weather_data`) via SQLAlchemy, usando `ON DUPLICATE KEY UPDATE` para evitar erros de chave duplicada em `cities` (`load.py` e `etl.py`).

## Integração com Flask

- **Propósito**: O Flask (`app.py`) fornece endpoints para executar o pipeline ETL, consultar dados e gerar resumos, conectando-se ao MySQL via Flask-SQLAlchemy (`models.py`).
- **Endpoints** (`app.py`):
  - `/etl`: Executa o pipeline ETL para cidades configuradas.
  - `/cities`: Lista todas as cidades.
  - `/weather/hot-cities`: Cidades com temperatura > 25°C.
  - `/weather/avg-temperature`: Temperatura média por cidade.
  - `/weather`: Lista todos os dados meteorológicos.
  - `/daily_summary`: Lista resumos diários.
  - `/generate_summary`: Gera resumo diário (`daily_summary`).
- **Conexão com Banco**: Configurada em `app.py` com `SQLALCHEMY_DATABASE_URI` (de `config.py`) e `db.init_app(app)` usando `pymysql` como driver MySQL.

## Definição das Tabelas (`models.py` e `init.sql`)

- **cities**:
  - `id` (INT, PRIMARY KEY): ID da cidade (ex.: 3448439 para São Paulo).
  - `name` (VARCHAR): Nome da cidade.
  - `country` (VARCHAR): Código do país (ex.: BR).
  - `latitude` (FLOAT): Latitude.
  - `longitude` (FLOAT): Longitude.
- **weather_data**:
  - `id` (INT, PRIMARY KEY, AUTO_INCREMENT): ID único do registro.
  - `city_id` (INT, FOREIGN KEY → cities.id): ID da cidade.
  - `temperature` (FLOAT): Temperatura (°C).
  - `humidity` (FLOAT): Umidade (%).
  - `timestamp` (DATETIME): Data/hora do dado.
  - `windspeed` (FLOAT, NULLABLE): Velocidade do vento (m/s).
  - `weather_condition` (VARCHAR, NULLABLE): Condição (ex.: "broken clouds").
  - `precipitation` (FLOAT, NULLABLE): Precipitação (mm/h).
- **daily_summary**:
  - `id` (INT, PRIMARY KEY, AUTO_INCREMENT): ID único.
  - `city_id` (INT, FOREIGN KEY → cities.id): ID da cidade.
  - `date` (DATE): Data do resumo.
  - `avg_temperature` (FLOAT): Temperatura média.
  - `avg_humidity` (FLOAT): Umidade média.
  - `record_count` (INT): Número de registros.

## Estratégia de Monitoramento de Qualidade

- **Valores Nulos**: Verifica nulos em `id`, `name`, `country`, `latitude`, `longitude` (para `cities`) e `city_id`, `temperature`, `humidity`, `timestamp` (para `weather_data`) antes da carga, usando `isna().any()` em `process.py`.