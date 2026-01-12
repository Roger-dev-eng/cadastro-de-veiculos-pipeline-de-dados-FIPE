# Cadastro de Veículos - Pipeline de Dados FIPE

## Conteúdo
- [Descrição](#Descrição)
- [Objetivo](#objetivo)
- [Estrutura do projeto](#estrutura-do-projeto)
- [Explicação dos principais componentes](#explicação-dos-principais-componentes)
- [Resultados e análises](#resultados-e-análises)
- [Exemplos](#exemplos)
- [Tecnologias utilizadas](#tecnologias-utilizadas)


## Descrição

Este projeto implementa uma **pipeline de dados automatizada** para coletar, armazenar e analisar informações da **tabela FIPE**, que contém dados de veículos (marca, modelo, ano, combustível e preço).  
O objetivo é demonstrar o processo completo de **extração, transformação e carregamento (ETL)** de dados de uma API pública até um banco de dados relacional, com visualizações analíticas para insights.

A pipeline foi construída em **Python**, utilizando **PostgreSQL** como banco de dados e diversas bibliotecas para manipulação e visualização dos dados.

## Objetivo

-  Automatizar a **coleta de dados** da API FIPE (Parallelum).
- Fazer a **limpeza e padronização** dos dados coletados.
- Armazenar os dados tratados em um **banco PostgreSQL**.
- Evitar inserções duplicadas no banco.
- Gerar **análises estatísticas e visuais** sobre os preços médios por marca e tipo de combustível.

## Estrutura do Projeto

```
cadastro-veiculos/
│
├── app/
│   ├── __init__.py           # Inicializa a conexão com o banco PostgreSQL
│   ├── fipe_import.py        # Pipeline de coleta e inserção de dados da API FIPE
│   ├── analysis.py           # Funções de análise e consultas SQL
│   └── utils/
│         ├── __init__.py     # Permite importar funções de utilidade
│         ├── helpers.py      # Tem funções de limpeza, validação e logs
│ 
├── config/
│   ├── db_config.py         # Carrega e valida a string de conexão com o PostgreSQL
│
├── data/                     # Armazena logs
│
├── notebooks/
│   └── analise_fipe.ipynb    # Notebook para visualizações e análises dos dados
│
├── requirements.txt
│
├── .env
│
└── README.md
```

---


## Explicação dos principais componentes

#### `fipe_import.py`
Responsável por:
- Coletar dados da **API FIPE**.
- Tratar os dados (limpeza de campos, substituição de anos inválidos por `N/A`, etc.).
- Evitar duplicidade ao inserir no banco.
- Criar a tabela `fipe_carros` caso não exista.
- Inserir os dados tratados no banco PostgreSQL.

#### `analysis.py`
Contém consultas SQL e funções de análise, como:
- Cálculo do **preço médio por marca**.
- Cálculo do **preço médio por tipo de combustível**.
- Retorno de DataFrames prontos para visualização.

#### `visualization.ipynb`
Notebook com:
- Conexão ao banco de dados.
- Leitura dos dados FIPE armazenados.
- Visualizações com **Matplotlib**, **Seaborn** e **Plotly** (ex.: distribuição de preços, comparação por combustível, etc.).

#### `run.py`
Executa a pipeline completa, incluindo:
1. Coleta dos dados FIPE.
2. Armazenamento no banco.
3. Execução das análises de preço médio.

---

## Resultados e Análises

### Visão Geral

Após a execução da pipeline, os dados extraídos da API FIPE são processados, armazenados e analisados, gerando insights valiosos sobre o mercado automotivo brasileiro.


Os dados são persistidos na tabela **`fipe_carros`** do PostgreSQL, contendo informações completas sobre:
- Marcas e modelos de veículos
- Preços de referência FIPE
- Anos de fabricação
- Tipos de combustível
- Códigos FIPE

---

## Exemplos

### Média de Preço por Marca

| Marca      | Preço Médio (R$) | Total de Modelos |
|------------|------------------|------------------|
| Agrale     | 213.013,96       | 85              |
| Acura      | 23.885,73        | 15              |
| Audi       | 180.450,20       | 342             |
| BMW        | 195.320,50       | 278             |
| Chevrolet  | 85.430,18        | 1.245           |
| Fiat       | 68.920,45        | 987             |
| Ford       | 92.150,33        | 856             |
| Honda      | 110.280,67       | 423             |
| Hyundai    | 95.670,89        | 512             |
| Toyota     | 125.890,12       | 645             |

### Média de Preço por Tipo de Combustível

| Combustível | Preço Médio (R$) | Total de Veículos |
|-------------|------------------|-------------------|
| Diesel      | 213.013,96       | 85               |
| Gasolina    | 89.450,32        | 4.823            |
| Flex        | 76.320,15        | 3.567            |
| Elétrico    | 285.670,00       | 42               |
| Híbrido     | 198.450,50       | 156              |
| GNV         | 45.230,80        | 234              |


##  Tecnologias Utilizadas


| Tecnologia    | Versão  | Função                                    |
|---------------|---------|-------------------------------------------|
| **Python**    | 3.13    | Linguagem principal do projeto            |
| **PostgreSQL**| 15+     | Banco de dados relacional                 |
| **SQLAlchemy**| 2.0+    | ORM para mapeamento objeto-relacional     |
| **Pandas**    | 2.1+    | Manipulação e análise de dados            |
| **Requests**  | 2.31+   | Cliente HTTP para consumo da API FIPE     |
| **Matplotlib**  | 3.8+    | Criação de gráficos estáticos          |
| **Seaborn**     | 0.13+   | Visualizações estatísticas avançadas   |
| **Plotly**      | 5.18+   | Gráficos interativos (opcional)        |
| **Jupyter**     | 1.0+    | Ambiente de notebooks interativos      |
| **tqdm**         | 4.66+   | Barras de progresso para ETL           |
| **python-dotenv**| 1.0+    | Gerenciamento de variáveis de ambiente |
| **psycopg2**     | 2.9+    | Driver PostgreSQL para Python          |
| **loguru**       | 0.7+    | Sistema de logs estruturado            |
---