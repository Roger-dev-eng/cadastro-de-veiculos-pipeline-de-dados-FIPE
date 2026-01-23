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
│   ├── __init__.py
│   ├── clients/
│   │   └── __init__.py
│   ├── db/
│   │   ├── __init__.py
│   │   └── engine.py         # Inicializa a conexao com o PostgreSQL
│   ├── pipeline/
│   │   ├── __init__.py
│   │   └── fipe_import.py    # Pipeline de coleta e insercao de dados da API FIPE
│   └── utils/
│       ├── __init__.py
│       └── funcoes.py        # Funcoes de limpeza, validacao e logs
│
├── logs/                     # Armazena logs e cache
│
├── notebooks/
│   └── analise_fipe.ipynb    # Notebook para visualizacoes e analises dos dados
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

#### `app/pipeline/fipe_import.py`
Responsável por:
- Coletar dados da **API FIPE**.
- Tratar os dados (limpeza de campos, substituicao de anos invalidos por `N/A`, etc.).
- Evitar duplicidade ao inserir no banco.
- Criar a tabela `fipe_carros` caso nao exista.
- Inserir os dados tratados no banco PostgreSQL.


#### `notebooks/analise_fipe.ipynb`
Notebook com:
- Conexao ao banco de dados.
- Leitura dos dados FIPE armazenados.
- Visualizacoes com **Matplotlib**, **Seaborn** e **Plotly** (ex.: distribuicao de precos, comparacao por combustivel, etc.).


#### `run.py`
Executa a pipeline completa, incluindo:
1. Coleta dos dados FIPE.
2. Armazenamento no banco.
3. Execucao das analises de preco medio.


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
![exemplo1](https://private-user-images.githubusercontent.com/205425623/540004789-8d0bd079-d565-413e-8833-886f62492625.png?jwt=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3NjkyMTE3NTcsIm5iZiI6MTc2OTIxMTQ1NywicGF0aCI6Ii8yMDU0MjU2MjMvNTQwMDA0Nzg5LThkMGJkMDc5LWQ1NjUtNDEzZS04ODMzLTg4NmY2MjQ5MjYyNS5wbmc_WC1BbXotQWxnb3JpdGhtPUFXUzQtSE1BQy1TSEEyNTYmWC1BbXotQ3JlZGVudGlhbD1BS0lBVkNPRFlMU0E1M1BRSzRaQSUyRjIwMjYwMTIzJTJGdXMtZWFzdC0xJTJGczMlMkZhd3M0X3JlcXVlc3QmWC1BbXotRGF0ZT0yMDI2MDEyM1QyMzM3MzdaJlgtQW16LUV4cGlyZXM9MzAwJlgtQW16LVNpZ25hdHVyZT0wYmMzNjRkZTQxYWIwNjVmNDJiOTAyNWNkYmY2ZTgwY2QyMjE5M2UzMDRiZDY1Y2JhNTk2MTZhYzUzZjFhNzQ1JlgtQW16LVNpZ25lZEhlYWRlcnM9aG9zdCJ9.uGAVA2lUU9c3PZZkkK-lcULddgHp0Ha6PV0JBqyzF-U)

### Evolução do preço médio por ano
![exemplo3](https://private-user-images.githubusercontent.com/205425623/536250412-20f8de95-c3c8-49c2-87f8-bc4215ae0377.png?jwt=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3NjkyMTE1NjcsIm5iZiI6MTc2OTIxMTI2NywicGF0aCI6Ii8yMDU0MjU2MjMvNTM2MjUwNDEyLTIwZjhkZTk1LWMzYzgtNDljMi04N2Y4LWJjNDIxNWFlMDM3Ny5wbmc_WC1BbXotQWxnb3JpdGhtPUFXUzQtSE1BQy1TSEEyNTYmWC1BbXotQ3JlZGVudGlhbD1BS0lBVkNPRFlMU0E1M1BRSzRaQSUyRjIwMjYwMTIzJTJGdXMtZWFzdC0xJTJGczMlMkZhd3M0X3JlcXVlc3QmWC1BbXotRGF0ZT0yMDI2MDEyM1QyMzM0MjdaJlgtQW16LUV4cGlyZXM9MzAwJlgtQW16LVNpZ25hdHVyZT0yMGQ4YjFiZDk0MmRjOGNiZTBlY2IwMDUzMDE3ZTc5NjNlNWVmYzgxMzA4NzRiNzY0MzVhNzdiZGM1ZjRkZGNjJlgtQW16LVNpZ25lZEhlYWRlcnM9aG9zdCJ9.4bbdsH0in4fDhJQ9BMS-_hrra-9NPytEOR47hElwWLg)

### Preço médio por combustível
![exemplo2](https://private-user-images.githubusercontent.com/205425623/536246502-917a98b5-68fd-4df6-b9f0-229a0033f4e7.png?jwt=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3NjkyMTE1MDIsIm5iZiI6MTc2OTIxMTIwMiwicGF0aCI6Ii8yMDU0MjU2MjMvNTM2MjQ2NTAyLTkxN2E5OGI1LTY4ZmQtNGRmNi1iOWYwLTIyOWEwMDMzZjRlNy5wbmc_WC1BbXotQWxnb3JpdGhtPUFXUzQtSE1BQy1TSEEyNTYmWC1BbXotQ3JlZGVudGlhbD1BS0lBVkNPRFlMU0E1M1BRSzRaQSUyRjIwMjYwMTIzJTJGdXMtZWFzdC0xJTJGczMlMkZhd3M0X3JlcXVlc3QmWC1BbXotRGF0ZT0yMDI2MDEyM1QyMzMzMjJaJlgtQW16LUV4cGlyZXM9MzAwJlgtQW16LVNpZ25hdHVyZT04OTdjYmNiZWMzNGFiMzdhMTYzYjY0MzUyMzhjMjJhYTBiNDgxYzNlM2FhNDk3ZDYwYmUyNTgxMjc0ZTNlYzVlJlgtQW16LVNpZ25lZEhlYWRlcnM9aG9zdCJ9.iR_6rgV1jkUlWHF3fzJ74K0mqM5ub2sVfuFWP4sfAaA)


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
