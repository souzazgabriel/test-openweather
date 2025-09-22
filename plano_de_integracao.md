# Plano de Integração de Dados Meteorológicos

## Estrutura do Pipeline ETL

- **Extração**: Consome dados da API OpenWeatherMap para cidades (São Paulo, Rio de Janeiro, Curitiba) usando `requests` com `units=metric` para temperaturas em Celsius.
- **Transformação**: Processa dados com Pandas, extraindo `city_id`, `name`, `country`, `latitude`, `longitude` para `cities` e `temperature`, `humidity`, `timestamp`, `windspeed`, `weather_condition`, `precipitation` para `weather_data`. Retorna dois DataFrames em uma tupla.
- **Carga**: Insere em tabelas MySQL (`cities` e `weather_data`) via SQLAlchemy, usando `ON DUPLICATE KEY UPDATE` para evitar erros de chave duplicada em `cities`.

## Definição das Tabelas

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
  - `city_id` (INT, FOREIGN KEY → cities.id): ID da cidade.
  - `date` (DATE): Data do resumo.
  - `avg_temperature` (FLOAT): Temperatura média.
  - `avg_humidity` (FLOAT): Umidade média.
  - `record_count` (INT): Número de registros.

## Estratégia de Monitoramento de Qualidade

- **Valores Nulos**: Verifica nulos em `city_id`, `temperature`, `humidity`, `timestamp` no DataFrame antes da carga.