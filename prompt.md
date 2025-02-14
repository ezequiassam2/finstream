## Prompt de Implementação do Projeto

### Arquitetura do Projeto

Este projeto foi estruturado de maneira modular para processar arquivos TXT e JSON. A arquitetura foi organizada para facilitar a manutenção, escalabilidade e reuso, adotando padrões de design como Strategy e Factory.

#### Estrutura de Diretórios

- **data/**: Diretório para armazenar arquivos de dados brutos.
- **scripts/**: Scripts principais para executar o fluxo completo de processamento.
- **src/**: Diretório principal do código-fonte.
  - **reader/**: Módulos para leitura de arquivos.
    - **txt_reader.py**: Leitor específico para arquivos TXT.
    - **json_reader.py**: Leitor específico para arquivos JSON.
  - **processor/**: Coordena estratégias para parsing.
    - **item_processor.py**: Orquestra as estratégias de parsing.
    - **strategies/**: Estratégias concretas para diferentes relatórios.
      - **parsing_strategy.py**: Classe base para estratégia de parsing.
      - **parse_vss610.py**: Estratégia para parsing do relatório VSS-610.
      - **parse_vss110.py**: Estratégia para parsing do relatório VSS-110.
  - **writer/**: Módulo para escrita e persistência de dados.
    - **item_writer.py**: Gerência a inserção de dados em bancos de dados.
  - **factory/**: Gerenciamento de criação de estrategias e leitores.
    - **processor_factory.py**: Implementação do padrão Factory para criar leitores/pares específicos).
  - **utilities/**: Utilidades e configurações globais.
    - **logger.py**: Configuração de logging.
    - **config.py**: Configurações gerais.

- **tests/**: Testes automatizados para garantir qualidade do código.

### Passos de Implementação

1. **Revisão e Integração do Script VSS-110:**

   - **Adapte** o script existente(process_table_posicinal.py) para parsing do VSS-110 no módulo `src/processor/strategies/parse_vss110.py`.
   - **Garanta** que o script segue o padrão definido por `ParsingStrategy`, utilizando regex ou lógica já existente.

2. **Implementação do Fluxo de Processamento:**

   - **Codifique** a lógica de leitura nos módulos `txt_reader.py` e `json_reader.py` para que eles possam extrair dados em partes, lendo linha a linha.
   - **Orquestre** o processamento no `item_processor.py`, utilizando o `ProcessorFactory` para determinar e executar a estratégia correta para cada arquivo.
   - **Implemente** o processamento paralelo usando `concurrent.futures` para distribuir processamento em diferentes segmentos de arquivo.

3. **Processamento por Seção:**

   - **Desenvolva** o controle de seção no loop principal de leitura para identificar delimitadores e iniciadores de cada seção do relatório.
   - **Utilize** o loop de leitura para parse e processamento imediatos das linhas, minimizando o uso de memória.

4. **Escrita de Dados:**

   - **Implemente** a classe `ItemWriter` para persistir com segurança em uma base de dados, utilizando transações SQLAlchemy.

5. **Implementação de Testes:**

   - **Escreva** testes unitários para todas as classes principais em `tests/`, garantindo cobertura de funcionalidade crítica.

6. **Otimização Final e Testes:**

   - **Compile** todos os componentes e **execute** testes extensivos para confirmar a correta instalação e execução do fluxo de trabalho de parsing.
   - **Depure** e **otimize** baseando-se em logs para resolver quaisquer problemas de desempenho ou bugs restantes.

### Execução e Performance

**Execute** todos os passos conforme descrito, assegurando que o processamento é otimizado para performance, tanto em termos de tempo com processamento paralelo, quanto de memória com leitura linha a linha. Implemente logs detalhados para visualizar o desempenho e possíveis gargalos.