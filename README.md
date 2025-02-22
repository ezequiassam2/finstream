## Finstream

ETL para processamento de relatórios financeiros em Python.

### Visão Geral do Projeto

Este projeto é projetado para processar arquivos TXT e JSON contendo relatórios de transações financeiras. Ele segue uma arquitetura modular para garantir a manutenção, escalabilidade e reutilização. Padrões de design como Strategy e Factory são utilizados.

#### Estrutura de Diretórios

- **core/**: Funcionalidades e utilitários principais.
   - **models/**: Modelos de dados.
   - **strategies/**: Estratégias de parsing.
   - **utils/**: Funções utilitárias.
- **etl/**: Componentes ETL.
   - **reader/**: Leitores de arquivos.
   - **processor/**: Processadores de dados.
   - **writer/**: Bulk inserts.
- **orchestrator/**: Lógica de orquestração produtor-consumidor.

### Como Executar

#### Pré-requisitos

- Docker
- Python 3.9
- PostgreSQL

#### Executando Localmente

1. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

2. Configure as variáveis de ambiente:
   ```bash
   cp .env.example .env
   ```

3. Coloque os arquivos de dados nos diretórios apropriados:
   - Arquivos TXT: `data/raw/EP747/`
   - Arquivos JSON: `data/raw/VISA_CLEARING/`

4. Execute a aplicação:
   ```bash
   python main.py
   ```

5. Execute os scripts SQL para consultar os calculos:
   ```bash
   psql -U postgres -d finstream -f scripts.sql
   ```

#### Executando com Docker

1. Construa e inicie os contêineres:
   ```bash
   docker-compose up --build
   ```

2. Coloque os arquivos de dados nos diretórios apropriados:
   - Arquivos TXT: `data/raw/EP747/`
   - Arquivos JSON: `data/raw/VISA_CLEARING/`

3. Execute os scripts SQL para consultar os calculos:
   ```bash
   docker exec -i finstream_db psql -U postgres -d finstream < scripts.sql
   ```

### Funcionalidades Principais

- **Design Modular**: Garante manutenção e escalabilidade.
- **Padrão Strategy**: Implementa diferentes estratégias de parsing para cada tipo de relatório.
- **Arquitetura Produtor-Consumidor**: Gerencia o controle de fluxo com uma fila.
- **Processamento Paralelo**: Distribui o processamento em diferentes segmentos de arquivo.
- **Bulk Insert**: Inserção otimizada de dados usando SQLAlchemy.

### Queries SQL

Os scripts SQL que realizar cálculos específicos estão localizados no arquivo `scripts.sql`. Eles incluem consultas para somar valores de compras e saques em diferentes moedas, bem como calcular o repasse líquido.