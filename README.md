# Cadastro de Veículos - Pipeline de Dados FIPE

## Conteúdo
- [Descrição](#descrição)
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
│   ├── db/
│   │   ├── __init__.py
│   │   └── engine.py         # Inicializa a conexão com o PostgreSQL
│   ├── dashboard/
│   │   ├── __init__.py
│   │   ├── charts.py         # Gráficos interativos do dashboard
│   │   ├── dashboard.py      # Interface Streamlit
│   │   └── queries.py        # Consultas ao banco para o dashboard
│   ├── pipeline/
│   │   ├── __init__.py
│   │   └── fipe_import.py    # Pipeline de coleta e inserção de dados da API FIPE
│   └── utils/
│       ├── __init__.py
│       └── funcoes.py        # Funções de limpeza, validação e logs
│
├── logs/                     # Armazena logs e cache
│
├── run.py                    # Executa toda a pipeline
│
├── requirements.txt
│
├── .env                      # Configuração local das variáveis de ambiente
│
└── README.md
```


---


## Explicação dos principais componentes

#### `app/pipeline/fipe_import.py`
Responsável por:
- Coletar dados da **API FIPE**.
- Tratar os dados, incluindo limpeza de valores monetários e validação de anos.
- Evitar duplicidade ao inserir no banco.
- Criar a tabela `fipe_carros` caso não exista.
- Inserir os dados tratados no banco PostgreSQL.


#### `app/dashboard/dashboard.py`
Interface web em **Streamlit** com:
- Filtros por marca, combustível e ano.
- Indicadores de volume, marcas, preço médio e maior preço.
- Gráficos interativos com **Plotly**.
- Tabela dos registros filtrados.
- Botão opcional para executar a importação dos dados FIPE.


#### `run.py`
Executa a pipeline completa, incluindo:
1. Coleta dos dados FIPE.
2. Armazenamento no banco.
3. Geração da base utilizada no dashboard Streamlit.


---

## Como executar

Instale as dependências:

```bash
pip install -r requirements.txt
```

Execute a pipeline para carregar dados no PostgreSQL:

```bash
python run.py
```

Abra o dashboard Streamlit:

```bash
streamlit run app/dashboard/dashboard.py
```

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
<img width="1157" height="651" alt="Captura de tela 2026-01-23 203701" src="https://github.com/user-attachments/assets/fb009276-a40d-45d0-9f6b-939f2456cf16" />

### Evolução do preço médio por ano
<img width="1065" height="591" alt="Captura de tela 2026-01-15 110157" src="https://github.com/user-attachments/assets/14fd3212-1975-4e8d-a4e8-a94594d86e98" />

### Preço médio por combustível
<img width="600" height="631" alt="Captura de tela 2026-01-15 105026" src="https://github.com/user-attachments/assets/70c92ab4-9dfe-4908-9061-5424dc445ed3" />

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
| **Streamlit**   | 1.57+   | Interface web e dashboard interativo   |
| **Plotly**      | 6.7+    | Gráficos interativos                   |
| **python-dotenv**| 1.0+    | Gerenciamento de variáveis de ambiente |
| **psycopg2-binary** | 2.9+ | Driver PostgreSQL para Python          |
---
