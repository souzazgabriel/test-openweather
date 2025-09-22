# Weather ETL Project

Este projeto implementa um pipeline ETL que extrai dados climáticos da API OpenWeatherMap, processa as informações e armazena em um banco de dados MySQL. O projeto utiliza Airflow para orquestração, Flask para fornecer endpoints de consulta e Docker para gerenciar os serviços.

## Tecnologias

- Python 3.x
- Flask
- SQLAlchemy
- MySQL (via Docker)
- Apache Airflow
- Docker & Docker Compose

## Pré-requisitos

- Docker Desktop instalado
- Docker Compose
- Git
- Python 3.x
- PowerShell (para configuração do ambiente virtual no Windows)

## Configuração e Execução

Siga os passos abaixo para configurar e rodar o projeto:

### 1. Clonar o Repositório

Clone o repositório e navegue até a pasta do projeto:

```bash
git clone <URL_DO_REPOSITORIO>
cd <PASTA_DO_PROJETO>
```

### 2. Criar um Ambiente Virtual (PowerShell)

Crie e ative um ambiente virtual para isolar as dependências:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 3. Instalar Dependências

Instale as dependências listadas no arquivo `requirements.txt`:

```powershell
pip install -r requirements.txt
```

### 4. Criar o Arquivo de Configuração

Crie o arquivo `scripts/config.py` na pasta `scripts` com as configurações do banco de dados e da API OpenWeatherMap. Use placeholders para dados sensíveis e carregue-os de variáveis de ambiente no código real, se possível:

```python
class Config:
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://airflow:airflow@mysql:3306/weather_db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    API_KEY = 'sua_chave_api_openweathermap'
    BASE_URL = 'https://api.openweathermap.org/data/2.5/weather'
```

### 5. Criar o Arquivo `.env`

Crie um arquivo `.env` na raiz do projeto com as variáveis de ambiente necessárias:

```env
MYSQL_ROOT_PASSWORD=senha_root
MYSQL_DATABASE=weather_db
MYSQL_USER=airflow
MYSQL_PASSWORD=airflow
OPENWEATHER_API_KEY=sua_chave_api_openweathermap
```

**Nota**: Substitua `sua_chave_api_openweathermap` pela sua chave válida da API OpenWeatherMap. As credenciais do banco podem ser ajustadas conforme necessário.

### 6. Iniciar os Contêineres com Docker

Execute o comando abaixo para subir os serviços definidos no `docker-compose.yaml` (MySQL, Airflow, etc.) em modo detached:

```powershell
docker-compose up -d
```

### 7. Inicializar o Airflow

Inicialize o banco de dados do Airflow e crie um usuário administrador:

```powershell
docker exec -it <NOME_DO_CONTÊINER_AIRFLOW> airflow db init
docker exec -it <NOME_DO_CONTÊINER_AIRFLOW> airflow users create --username admin --firstname Admin --lastname User --role Admin --email admin@example.com --password admin
```

Substitua `<NOME_DO_CONTÊINER_AIRFLOW>` pelo nome do contêiner do Airflow (verifique com `docker ps`).

### 8. Verificar Contêineres

Confirme que os contêineres estão rodando:

```powershell
docker ps
```

Você deve ver os contêineres do MySQL, Airflow (e outros serviços definidos no `docker-compose.yaml`).

### 9. Executar o Arquivo `init.sql`

Para inicializar o banco de dados com o script `init.sql`, execute o seguinte comando no PowerShell, assumindo que o arquivo `init.sql` está na raiz do projeto:

```powershell
docker exec -i <NOME_DO_CONTÊINER_MYSQL> mysql -u airflow -pairflow weather_db < init.sql
```

Substitua `<NOME_DO_CONTÊINER_MYSQL>` pelo nome do contêiner MySQL (verificado em `docker ps`). Este comando redireciona o conteúdo do `init.sql` para o banco `weather_db`.

### 10. Conectar o Airflow ao Banco de Dados MySQL

No arquivo de configuração do Airflow (`airflow.cfg` ou via variável de ambiente), assegure-se de que a conexão com o MySQL está configurada. No `docker-compose.yaml`, isso geralmente já está definido, mas você pode verificar:

```yaml
environment:
  AIRFLOW__DATABASE__SQL_ALCHEMY_CONN: mysql+pymysql://airflow:airflow@mysql:3306/airflow
```

Se necessário, atualize o `docker-compose.yaml` e reinicie os contêineres:

```powershell
docker-compose down
docker-compose up -d
```

Acesse a interface web do Airflow em `http://localhost:8080` (usuário: admin, senha: admin) para confirmar que está funcionando.

### 11. Executar o Aplicativo Flask

Inicie o aplicativo Flask localmente:

```powershell
python app.py
```

O Flask estará disponível em `http://localhost:5000`.

### 12. Acessar os Endpoints do Flask

Acesse os endpoints da aplicação Flask em:

```
http://localhost:5000
```

**Exemplos de Endpoints**:

- `/etl` — Executa o pipeline ETL para as cidades configuradas
- `/cities` — Lista todas as cidades cadastradas
- `/weather/hot-cities` — Cidades com temperatura acima de 25°C
- `/weather/avg-temperature` — Temperatura média por cidade
- `/weather` — Lista todos os dados meteorológicos
- `/generate_summary` — Gera resumo diário

## Observações

- **Banco de Dados**: Os dados são armazenados no banco MySQL (`weather_db`) definido no `docker-compose.yaml`.
- **Portas**: Certifique-se de que as portas usadas no `docker-compose.yaml` (como 3306 para MySQL, 8080 para Airflow, 5000 para Flask) não estão em uso.
- **Airflow**: As DAGs devem estar na pasta configurada no `docker-compose.yaml` (geralmente `/opt/airflow/dags`). Copie suas DAGs para essa pasta, se necessário.
- **Flask Local**: Se rodar o Flask localmente, use `localhost` em vez de `mysql` na `SQLALCHEMY_DATABASE_URI` em `scripts/config.py`.
- **Testes**: O projeto foi testado com Docker Desktop e PowerShell no Windows.
- **Chave da API**: Obtenha uma chave válida da OpenWeatherMap em `https://openweathermap.org/api`.
