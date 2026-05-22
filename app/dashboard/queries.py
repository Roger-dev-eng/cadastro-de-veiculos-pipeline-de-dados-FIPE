import os

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, text


def get_database_url():
    load_dotenv(dotenv_path=".env")
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise RuntimeError("DATABASE_URL nao definida no arquivo .env")
    return database_url


def get_engine():
    return create_engine(get_database_url(), pool_pre_ping=True)


def load_fipe_data(engine):
    query = text("""
        SELECT
            id,
            marca,
            modelo,
            ano_modelo,
            combustivel,
            valor_str,
            valor,
            codigo_fipe,
            sigla_combustivel,
            data_consulta
        FROM fipe_carros
        ORDER BY marca, modelo, ano_modelo DESC
    """)
    return pd.read_sql_query(query, engine)


def table_exists(engine):
    query = text("""
        SELECT EXISTS (
            SELECT 1
            FROM information_schema.tables
            WHERE table_schema = 'public'
              AND table_name = 'fipe_carros'
        )
    """)
    with engine.connect() as conn:
        return bool(conn.execute(query).scalar())
