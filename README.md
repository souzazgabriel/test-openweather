
# Weather ETL API

## Descrição

Este projeto é uma API para processar e consultar dados meteorológicos utilizando um pipeline ETL. Os dados extraídos são processados, armazenados em um banco de dados e disponibilizados para consulta através de diversos endpoints.

## Endpoints Disponíveis

### 1. **`GET /etl`**
Executa o pipeline ETL para as cidades Rio de Janeiro, Curitiba e São Paulo.  
- **Processo:** 
  1. Extração dos dados meteorológicos via API.
  2. Processamento dos dados extraídos.
  3. Armazenamento dos dados no banco.
- **Resposta:** Retorna o status do processo para cada cidade.
- **Exemplo de Resposta:**
  ```json
  [
    {"city": "Rio de Janeiro", "status": "success", "message": "Dados para Rio de Janeiro inseridos com sucesso!"},
    {"city": "Curitiba", "status": "success", "message": "Dados para Curitiba inseridos com sucesso!"},
    {"city": "São Paulo", "status": "success", "message": "Dados para São Paulo inseridos com sucesso!"}
  ]
  ```

---

### 2. **`GET /cities`**
Lista todas as cidades cadastradas no banco de dados.  
- **Resposta:** Uma lista de cidades com seus IDs e nomes.
- **Exemplo de Resposta:**
  ```json
  [
    {"id": 1, "name": "Rio de Janeiro"},
    {"id": 2, "name": "Curitiba"},
    {"id": 3, "name": "São Paulo"}
  ]
  ```

---

### 3. **`GET /weather/hot-cities`**
Lista cidades onde a temperatura foi superior a 25°C.  
- **Resposta:** Lista de cidades e suas temperaturas.
- **Exemplo de Resposta:**
  ```json
  [
    {"city": "Rio de Janeiro", "temperature": 30.5},
    {"city": "São Paulo", "temperature": 26.2}
  ]
  ```

---

### 4. **`GET /weather/avg-temperature`**
Calcula a temperatura média por cidade.  
- **Resposta:** Lista de cidades com suas temperaturas médias.
- **Exemplo de Resposta:**
  ```json
  [
    {"city": "Rio de Janeiro", "avg_temperature": 27.4},
    {"city": "Curitiba", "avg_temperature": 22.1}
  ]
  ```

---

### 5. **`GET /daily_summary`**
Lista os resumos diários dos dados meteorológicos por cidade.  
- **Resposta:** Resumos com informações como temperatura média, umidade média, e total de registros.
- **Exemplo de Resposta:**
  ```json
  [
    {
      "city_name": "Rio de Janeiro",
      "date": "2024-12-01",
      "avg_temperature": 27.5,
      "avg_humidity": 60,
      "record_count": 50
    }
  ]
  ```

---

### 6. **`GET /weather`**
Lista todas as informações climáticas registradas no banco.  
- **Resposta:** Detalhes climáticos como temperatura, umidade, condição climática, entre outros.
- **Exemplo de Resposta:**
  ```json
  [
    {
      "city": "São Paulo",
      "country": "Brazil",
      "latitude": -23.5505,
      "longitude": -46.6333,
      "temperature": 25.3,
      "humidity": 70,
      "timestamp": "2024-12-01 09:00:00",
      "windspeed": 12.5,
      "weather_condition": "Clear",
      "precipitation": 0
    }
  ]
  ```

---

### 7. **`GET /generate_summary`**
Gera o resumo diário para todas as cidades.  
- **Processo:** Consolida os dados meteorológicos do dia, calculando médias e agregados.
- **Resposta:** Retorna uma mensagem de sucesso.
- **Exemplo de Resposta:**
  ```json
  {"message": "Resumo diário gerado com sucesso!"}
  ```

---

## Configuração e Execução do Airflow

Para iniciar o Airflow, siga as etapas abaixo:

1. **Inicializar o banco de dados do Airflow**:
   Caso seja a primeira vez que você está rodando o Airflow, inicialize o banco de dados do Airflow com o seguinte comando:
   ```bash
   airflow db init
   ```


#### 1.1. **Configuração do `AIRFLOW_HOME`**
Se você está usando o Windows com WSL2, defina a variável `AIRFLOW_HOME` para o diretório onde seus DAGs estão armazenados. No seu caso, é:

```bash
export AIRFLOW_HOME=/mnt/c/Users/User/OneDrive/Documentos/ESTUDOS/Python/pyWeather/dags
```

   
2. **Iniciar o Scheduler do Airflow**:
   O Airflow precisa de um scheduler para monitorar e executar os DAGs. Para iniciar o scheduler, execute:
   ```bash
   airflow scheduler
   ```

3. **Iniciar o Webserver do Airflow**:
   Para iniciar o servidor web do Airflow e acessar a interface web, execute:
   ```bash
   airflow webserver --port 8080
   ```
   O servidor web do Airflow será iniciado e você poderá acessar a interface web na URL `http://localhost:8080`.


## Cronograma (Schedule)

O pipeline ETL neste projeto é configurado para ser executado diariamente às 09h, como definido no arquivo de configuração do DAG. No arquivo do DAG, o `schedule_interval` é configurado da seguinte maneira:

```python
schedule_interval=- `0 9 * * *`: Executa diariamente às 9h.
```
- `@daily`: Executa uma vez por dia.
- `0 9 * * *`: Executa diariamente às 9h.


## Acessando a Interface Web do Airflow

Após iniciar o servidor web com o comando acima, você pode acessar a interface do Airflow no seu navegador em `http://localhost:8080`. O Airflow tem uma interface web amigável onde você pode monitorar, ativar, desativar e visualizar o status de seus DAGs.

## Configuração do Projeto

1. **Banco de Dados:** Certifique-se de configurar corretamente as informações do banco no arquivo `config.py`.
2. **ETL Scripts:** Os scripts para extração, processamento e carga estão localizados no diretório `scripts`.

## Como Executar

1. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

2. Execute as migrações do banco:
   ```bash
   flask db upgrade
   ```

3. Inicie o servidor Flask:
   ```bash
   python app.py
   ```

4. Acesse os endpoints em `http://localhost:5000`.

---

## Windows

O Apache Airflow é uma ferramenta poderosa de orquestração de workflows, mas foi projetado principalmente para rodar em ambientes baseados em Unix/Linux. No Windows, há desafios técnicos que podem tornar a instalação e execução mais complicadas. Portanto, o uso do **WSL2 (Windows Subsystem for Linux 2)** é altamente recomendado para facilitar a execução do Airflow.

### Como Configurar o WSL2

Siga os tutoriais abaixo para configurar o WSL2:

- [Como instalar o WSL2 no Windows](https://www.freecodecamp.org/news/how-to-install-wsl2-windows-subsystem-for-linux-2-on-windows-10/)
- [Instalando o Apache Airflow no Windows com WSL2](https://www.freecodecamp.org/news/install-apache-airflow-on-windows-without-docker/)

### Configuração do WSL2:

1. Instalar o Python 3:
   ```bash
   sudo apt update
   sudo apt install software-properties-common
   sudo add-apt-repository ppa:deadsnakes/ppa
   sudo apt update
   sudo apt install python3.11
   sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.11 1
   sudo apt install python-is-python3
   ```

2. Instalar pip:
   ```bash
   sudo apt install python3-pip
   ```

3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

4. Atualize cffi (se necessário):
   ```bash
   pip install --upgrade --force-reinstall cffi
   ```

5. Iniciar o banco de dados do Airflow:
   ```bash
   airflow db init
   ```



6. Iniciar o scheduler do Airflow:
   ```bash
   airflow scheduler
   ```

7. Iniciar o servidor web do Airflow:
   ```bash
   airflow webserver --port 8080
   ```

8. Criar um novo usuário no Airflow:
   ```bash
   airflow users create \
     --username admin \
     --firstname Admin \
     --lastname User \
     --email admin@example.com \
     --role Admin \
     --password adminpassword
   ```

---

## Tecnologias Utilizadas

- **Flask:** Framework para desenvolvimento web.
- **Pandas:** Processamento de Dados.
- **Requests:** Consumo de API REST.
- **SQLAlchemy:** ORM para interação com o banco de dados.
- **Flask-Migrate:** Gerenciamento de migra
