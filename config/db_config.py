from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path=".env")

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError(" DATABASE_URL não definida no arquivo .env")

engine = create_engine(DATABASE_URL)

print(" Conexão com o banco configurada com sucesso!")

def get_engine():
    return engine
