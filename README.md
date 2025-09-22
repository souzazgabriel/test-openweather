# Weather ETL Project

Este projeto consiste em um pipeline ETL que extrai dados climáticos da API OpenWeatherMap, processa as informações e as armazena em um banco de dados MySQL. Também disponibiliza endpoints em Flask para consultar dados de cidades, temperaturas, resumos diários e condições meteorológicas.

## Tecnologias

- Python 3.x
- Flask
- SQLAlchemy
- MySQL (via Docker)
- Docker & Docker Compose

## Pré-requisitos

- Docker Desktop instalado
- Docker Compose

## Configuração

1. Crie o arquivo `scripts/config.py` com a seguinte configuração:

```python
class Config:
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://airflow:airflow@mysql:3306/weather_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    API_KEY = '4ca56aa5b0eec444c9fee770b077517f'
    BASE_URL = 'https://api.openweathermap.org/data/2.5/weather'
```

2. Instale as dependências do projeto:

```bash
pip install -r requirements.txt
```

## Rodando o projeto

1. Clone este repositório:

```bash
git clone <URL_DO_REPOSITORIO>
cd <PASTA_DO_PROJETO>
```

2. Crie um arquivo `.env` na raiz do projeto com as variáveis de ambiente:

```env
MYSQL_ROOT_PASSWORD=senha_root
MYSQL_DATABASE=weather_db
MYSQL_USER=airflow
MYSQL_PASSWORD=senha_airflow
OPENWEATHER_API_KEY=sua_chave_api_openweathermap
```

3. Inicie os contêineres usando Docker Compose:

```bash
docker-compose up -d
```

Isso irá subir os serviços definidos no `docker-compose.yaml`, incluindo:

- MySQL
- Airflow (ou aplicação Flask/ETL, se incluída no Compose)

4. Verifique se os contêineres estão rodando:

```bash
docker ps
```

5. Acesse os endpoints da aplicação Flask em:

```
http://localhost:5000
```

### Exemplos de endpoints:

- `/etl` — Executa o pipeline ETL para as cidades configuradas
- `/cities` — Lista todas as cidades cadastradas
- `/weather/hot-cities` — Cidades com temperatura acima de 25°C
- `/weather/avg-temperature` — Temperatura média por cidade
- `/weather` — Lista todos os dados meteorológicos
- `/generate_summary` — Gera resumo diário

## Observações

- Todos os dados são armazenados no banco MySQL definido no `docker-compose.yaml`.
- Certifique-se de que as portas no Docker Compose não estão sendo usadas por outros serviços.
- O projeto foi testado utilizando Docker Desktop e rodando os contêineres via `docker-compose.yaml`.