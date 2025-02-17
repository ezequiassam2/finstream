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



*Introdução Geral**
Elabore um projeto em Python que realize o processamento de relatórios financeiros, onde será lido um arquivo txt que contem vários tipos de relatórios com os totalizadores e vários arquivos json que contem as transações. Inicie o projeto adotando as boas práticas de engenharia de software que incluem, mas não se limitam a, design modular, código limpo, documentação clara e uso coerente de padrões de projeto. Certifique-se de que cada módulo ou componente seja coeso e que os acoplamentos entre eles sejam minimizados para facilitar a manutenção, escalabilidade e reutilização do código. Lembre de adicionar uma documentação de código informando do que se trata cada arquivo/classe contendo resumidamente as técnicas ali abordadas.

**Estrutura do Projeto**
- **Diretório `finstream`**
- **Descrição**: Raiz do projeto, onde terá os demais arquivos relevantes mais o main onde será o ponto de entrada.
- **Técnicas**: Crie Readme, requirements, arquivos de docker com as configurações de um banco postgres, .env e outros se necessário
- 
- **Diretório `core/models`**
- **Descrição**: Modelos de dados para representar as informações extraídas dos relatórios e transações.
  - **Técnicas**: [Crie um arquivo schemas para definir os modelos de dados criando as classes Report(report_id: str,reporting_for: str,page: int,proc_date: datetime,rollup_to: str,report_date: datetime,funds_xfer_entity: str,settlement_currency: str,summary: List[str],amounts: List[Amount(section: str, label: str, count: Decimal, credit_amount: Decimal, debit_amount: Decimal, total_amount: Decimal)]);  Utilize as validações de pydantic para conversão no parser; Utilize indices em campos chaves; A relação entre tabelas deve ser otimizada para performace em grandes processamentos, os campos DECIMAL devem ter precisão e escalas definidas;]

- **Diretório `core/strategies`**
- **Descrição**: Padrão de projeto Strategy para implementar diferentes estratégias de parsing para cada tipo de relatório.
- **Técnicas**: Crie arquivo base_strategy(class ParsingStrategy) e use reflection para carregar strategies dinamicamente estendido como Factory Method. Implemente auto-registro de classes que herdam ParsingStrategy. O ParsingStrategy deve conter metodos abristratos, como parse_header e parse_amounts, além de ter um metodo que gerencia o parse executando coisas comuns em todos os relatorios. Crie um arquivo para cada tipo de relatório, como VSS-110, e implemente a lógica de parsing específica para cada um.

- **Diretório `core/utils`**
- **Descrição**: Utilidades e configurações globais.
- **Técnicas**: Configure o looging para gerar logs estruturados de execução e erros. Em todos os lugares necessários devem utilizar essas configurações de log contextual. O log deve ser salvo em um arquivo, separando em erros e infos por exemplos. Crie um arquivo de lógica de retry para tentar novamente a execução de um bloco de código que falhou.

- **Diretório `etl/reader`**
- **Descrição**: Leitura de arquivos
- **Técnicas**: Use Streaming para ler arquivos grandes, evitando carregar todo o arquivo na memória. Deve ler pedaços(seção) a pedaço  e processar imediatamente, minimizando o uso de memória.

- **Diretório `etl/processor`**
- **Descrição**: Transformação + validação
- **Técnicas**: Deve seguir o padrão pipeline transform. Utilize retry para tentar novamente a execução de um bloco de código que falhou. Gerencie os passos do processemento, gerenciando exceções de forma apropriada, registrando erros e não permitindo a continuação do processamento. O processamento será feito para cada seção de forma atomica, garantindo que se uma seção falhar, as demais seções sejam processadas. Caso apresente erro deve ser adicionado em algo semelhante ao Dead Letter Queue para posterior analise.
- **Diretório `etl/write`**
- **Descrição**: Bulk insert otimizado
- **Técnicas**: Deve inserir os dados em um banco de dados de forma otimizada, utilizando transações e bulk insert. Utilize o SQLAlchemy para gerenciar a conexão com o banco de dados e a inserção de dados.

- **Diretório `orchestrator`**
- **Descrição**: Controle de fluxo
- **Técnicas**: Utilize a Arquitetura Produtor-Consumidor tendo um Controle de fluxo com fila., Orquestre o processamento de arquivos txt e json, utilizando o processamento em paralelo para distribuir o processamento em diferentes segmentos de arquivo e recuperando dinamicamente o fluxo de processamento de acordo com o tipo do arquivo.

- **Diretório `tests`**
- **Descrição**: Testes automatizados
- **Técnicas**: Crie os testes para garantir a qualidade do código. Utilize o Pytest para escrever e executar testes. Garanta cobertura de funcionalidades críticas.

**Revisão Final**
Após a geração de todos os componentes solicitados, revisite cada parte do projeto para garantir que todos os requisitos foram atendidos e que o código segue as práticas recomendadas de engenharia de software. Certifique-se de incluir quaisquer ajustes necessários para melhorar a eficiência, legibilidade e manutenção do código.

**Sugestões de Melhoria**
No final do projeto, analise o que pode ser melhorado, considerando:
- Reorganização da estrutura do código para aumentar a eficiência.
- Melhorias de desempenho e otimizações potenciais.
- Outras práticas que poderiam ser adotadas para melhorar a qualidade do software.