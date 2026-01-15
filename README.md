# Cadastro de Veículos - Pipeline de Dados FIPE

## Conteúdo
- [Descrição](#Descrição)
- [Objetivo](#objetivo)
- [Estrutura do projeto](#estrutura-do-projeto)
- [Explicação dos principais componentes](#explicação-dos-principais-componentes)
- [Resultados e análises](#resultados-e-análises)
- [Dados analisados](#dados-analisados)
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
│   └── utils/
│         ├── __init__.py     # Permite importar funções de utilidade
│         ├── funções.py      # Tem funções de limpeza, validação e logs
│ 
├── config/
│   ├── db_config.py          # Carrega e valida a string de conexão com o PostgreSQL
│
├── logs/                     # Armazena logs
│
├── notebooks/
│   └── analise_fipe.ipynb    # Notebook para visualizações e análises dos dados
│
├── run.py                    # Executa toda a pipeline
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

#### `analise_fipe.ipynb`
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

## Dados analisados

### Dados brutos

| id  | marca  | modelo                                   | ano_modelo | combustivel | valor_str     | valor    | codigo_fipe | sigla_combustivel | data_consulta |
|-----|--------|------------------------------------------|------------|-------------|---------------|----------|-------------|-------------------|---------------|
| 84  | Acura  | Integra GS 1.8                           | 1992       | Gasolina    | R$ 10.963,00  | 10963.0  | 038003-2    | G                 | None          |
| 85  | Acura  | Integra GS 1.8                           | 1991       | Gasolina    | R$ 10.241,00  | 10241.0  | 038003-2    | G                 | None          |
| 86  | Acura  | Legend 3.2/3.5                          | 1998       | Gasolina    | R$ 25.096,00  | 25096.0  | 038002-4    | G                 | None          |
| 87  | Acura  | Legend 3.2/3.5                          | 1997       | Gasolina    | R$ 22.312,00  | 22312.0  | 038002-4    | G                 | None          |
| 88  | Acura  | Legend 3.2/3.5                          | 1996       | Gasolina    | R$ 20.981,00  | 20981.0  | 038002-4    | G                 | None          |
| 89  | Acura  | Legend 3.2/3.5                          | 1995       | Gasolina    | R$ 18.857,00  | 18857.0  | 038002-4    | G                 | None          |
| 90  | Acura  | Legend 3.2/3.5                          | 1994       | Gasolina    | R$ 18.048,00  | 18048.0  | 038002-4    | G                 | None          |
| 91  | Acura  | Legend 3.2/3.5                          | 1993       | Gasolina    | R$ 16.087,00  | 16087.0  | 038002-4    | G                 | None          |
| 92  | Acura  | Legend 3.2/3.5                          | 1992       | Gasolina    | R$ 14.625,00  | 14625.0  | 038002-4    | G                 | None          |
| 93  | Acura  | Legend 3.2/3.5                          | 1991       | Gasolina    | R$ 14.049,00  | 14049.0  | 038002-4    | G                 | None          |
| 94  | Acura  | NSX 3.0                                 | 1995       | Gasolina    | R$ 40.508,00  | 40508.0  | 038001-6    | G                 | None          |
| 95  | Acura  | NSX 3.0                                 | 1994       | Gasolina    | R$ 39.083,00  | 39083.0  | 038001-6    | G                 | None          |
| 96  | Acura  | NSX 3.0                                 | 1993       | Gasolina    | R$ 37.783,00  | 37783.0  | 038001-6    | G                 | None          |
| 97  | Acura  | NSX 3.0                                 | 1992       | Gasolina    | R$ 36.106,00  | 36106.0  | 038001-6    | G                 | None          |
| 98  | Acura  | NSX 3.0                                 | 1991       | Gasolina    | R$ 33.002,00  | 33002.0  | 038001-6    | G                 | None          |
| 99  | Agrale | MARRUÁ 2.8 12V 132cv TDI Diesel          | 2007       | Diesel      | R$ 47.681,00  | 47681.0  | 060001-6    | D                 | None          |
| 100 | Agrale | MARRUÁ 2.8 12V 132cv TDI Diesel          | 2006       | Diesel      | R$ 46.251,00  | 46251.0  | 060001-6    | D                 | None          |
| 101 | Agrale | MARRUÁ 2.8 12V 132cv TDI Diesel          | 2005       | Diesel      | R$ 45.122,00  | 45122.0  | 060001-6    | D                 | None          |
| 102 | Agrale | MARRUÁ 2.8 12V 132cv TDI Diesel          | 2004       | Diesel      | R$ 37.484,00  | 37484.0  | 060001-6    | D                 | None          |
| 103 | Agrale | MARRUÁ AM 100 2.8 CS TDI Diesel          | 2015       | Diesel      | R$ 107.264,00 | 107264.0 | 060003-2    | D                 | None          |


### Preço médio por marca
![exemplo1](https://private-user-images.githubusercontent.com/205425623/536246290-d3cebc83-52a8-4253-8819-46257b9f766a.png?jwt=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3Njg0ODU0NTksIm5iZiI6MTc2ODQ4NTE1OSwicGF0aCI6Ii8yMDU0MjU2MjMvNTM2MjQ2MjkwLWQzY2ViYzgzLTUyYTgtNDI1My04ODE5LTQ2MjU3YjlmNzY2YS5wbmc_WC1BbXotQWxnb3JpdGhtPUFXUzQtSE1BQy1TSEEyNTYmWC1BbXotQ3JlZGVudGlhbD1BS0lBVkNPRFlMU0E1M1BRSzRaQSUyRjIwMjYwMTE1JTJGdXMtZWFzdC0xJTJGczMlMkZhd3M0X3JlcXVlc3QmWC1BbXotRGF0ZT0yMDI2MDExNVQxMzUyMzlaJlgtQW16LUV4cGlyZXM9MzAwJlgtQW16LVNpZ25hdHVyZT1hOTQwMzYxNjg1N2IxYmRkNTVhY2Y0Y2QxODliOTIwZTJlZmM4OGM3NGQxZThjYTk0ZjRjNzA1YmZlZWFjNzkzJlgtQW16LVNpZ25lZEhlYWRlcnM9aG9zdCJ9.zM6KrtYVdhTdfq2hpJdDgdFI0jeqbmx3Jg3FW1tgXQ0)

### Evolução do preço médio por ano
![exemplo3](https://private-user-images.githubusercontent.com/205425623/536250412-20f8de95-c3c8-49c2-87f8-bc4215ae0377.png?jwt=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3Njg0ODYwNDEsIm5iZiI6MTc2ODQ4NTc0MSwicGF0aCI6Ii8yMDU0MjU2MjMvNTM2MjUwNDEyLTIwZjhkZTk1LWMzYzgtNDljMi04N2Y4LWJjNDIxNWFlMDM3Ny5wbmc_WC1BbXotQWxnb3JpdGhtPUFXUzQtSE1BQy1TSEEyNTYmWC1BbXotQ3JlZGVudGlhbD1BS0lBVkNPRFlMU0E1M1BRSzRaQSUyRjIwMjYwMTE1JTJGdXMtZWFzdC0xJTJGczMlMkZhd3M0X3JlcXVlc3QmWC1BbXotRGF0ZT0yMDI2MDExNVQxNDAyMjFaJlgtQW16LUV4cGlyZXM9MzAwJlgtQW16LVNpZ25hdHVyZT1mMmRmYjgwMTAzNmI4OTUzZjA3MDRlMWFjZmE5NzhiMTIyODA5ZWI3NjkzZTVmMTg1NGFhMjc0NDBlMmQ5ZjFjJlgtQW16LVNpZ25lZEhlYWRlcnM9aG9zdCJ9.SLm2DOPontSflrm_pAXTRT1zgtFlJq9fVia6lrYELdw)

### Preço médio por combustível
![exemplo2](https://private-user-images.githubusercontent.com/205425623/536246502-917a98b5-68fd-4df6-b9f0-229a0033f4e7.png?jwt=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3Njg0ODU5NzIsIm5iZiI6MTc2ODQ4NTY3MiwicGF0aCI6Ii8yMDU0MjU2MjMvNTM2MjQ2NTAyLTkxN2E5OGI1LTY4ZmQtNGRmNi1iOWYwLTIyOWEwMDMzZjRlNy5wbmc_WC1BbXotQWxnb3JpdGhtPUFXUzQtSE1BQy1TSEEyNTYmWC1BbXotQ3JlZGVudGlhbD1BS0lBVkNPRFlMU0E1M1BRSzRaQSUyRjIwMjYwMTE1JTJGdXMtZWFzdC0xJTJGczMlMkZhd3M0X3JlcXVlc3QmWC1BbXotRGF0ZT0yMDI2MDExNVQxNDAxMTJaJlgtQW16LUV4cGlyZXM9MzAwJlgtQW16LVNpZ25hdHVyZT1kZWY0NGI2ZmMwMWMyM2EzMTViZTkwNWUzZGQ2OGViMThkMDA5MmU4MTI5OTZkYzI3NzRjMDM5OTRhODY3M2M2JlgtQW16LVNpZ25lZEhlYWRlcnM9aG9zdCJ9._s2Ax3wbFq2kpc9T-VlLxUIW0OeaX7TJBMSYc6Oh9SM)


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