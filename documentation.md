# Decisões de Projeto – Weather ETL

Este documento registra as principais escolhas de design feitas no desenvolvimento do pipeline Weather ETL e dos serviços relacionados. A ideia é justificar por que certas abordagens foram adotadas.

## Estrutura Modular (`scripts/`)

- O projeto foi dividido em `extract.py`, `process.py` e `load.py`, refletindo claramente as etapas do ETL (extração, transformação e carga).

- Essa separação facilita testes unitários e manutenção: podemos alterar a forma de extração (por exemplo, outra API) sem impactar a transformação ou a carga.

## Configuração Centralizada

- As variáveis sensíveis e reutilizadas (URI do banco, API key e endpoint base da OpenWeather) ficam em `config.py`.

- Isso garante que qualquer ajuste seja feito em um único lugar, evitando repetição e reduzindo risco de erro.

## Uso do Airflow (`weather_etl_dag.py`)

- O Airflow foi adotado para orquestrar o pipeline, já que permite agendamento e monitoramento confiável.

- O DAG foi configurado para rodar diariamente às 9h `(schedule="0 9 * * *")` — um horário em que geralmente já há dados consolidados do dia anterior, evitando consultas incompletas.

- Foi usada a API de decorators (`@dag` e `@task`) para manter o código mais enxuto e fácil de ler.

## Processamento de Dados

- A transformação (`process.py`) extrai apenas os campos relevantes da resposta da API (nome da cidade, coordenadas, temperatura, etc.).

- A conversão de `Kelvin → Celsius` foi feita manualmente porque a API retorna temperatura em Kelvin por padrão. Isso mantém compatibilidade caso seja necessário desativar o parâmetro `units=metric` no futuro.

- Foi adicionada verificação de valores nulos antes de gravar no banco. Isso evita violação de restrições `NOT NULL` definidas no schema SQL.

## Armazenamento em Banco (`load.py` / `init.sql` / `models.py`)

- O banco escolhido foi MySQL por sua familiaridade com integração em pipelines ETL.

- A modelagem separa cidades (`cities`) de dados meteorológicos (`weather_data`) para evitar redundância. Cada medição aponta para uma cidade via chave estrangeira.

- Foi criada a tabela `daily_summary` para armazenar agregados, acelerando consultas comuns (como médias diárias por cidade).

- O método de carga ignora inserções duplicadas de cidades (tratando `IntegrityError`), pois a cidade não muda, apenas suas medições.

## Integração com Flask (`app.py`)

- O Flask foi adicionado para expor endpoints REST, permitindo consulta dos dados por aplicações externas.

- Endpoints foram criados para listar cidades, dados meteorológicos crus, dados agregados (ex.: médias de temperatura) e resumos diários.

- O retorno usa `json_response` com `ensure_ascii=False`, garantindo que acentos sejam exibidos corretamente (importante para nomes de cidades brasileiras).

## Resumos Diários (etl.py)

- A função `generate_daily_summary` consolida os dados meteorológicos de cada dia e grava em `daily_summary`.

- Essa escolha evita recalcular agregados a cada requisição e melhora o desempenho para consultas analíticas.

## Decisão de Tecnologias

- Airflow → orquestração e agendamento.

- Flask + SQLAlchemy → API de consulta e abstração do banco.

- Pandas → manipulação e validação de dados na etapa de transformação.

- MySQL → persistência relacional com suporte a integridade referencial.