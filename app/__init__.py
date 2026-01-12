from dotenv import load_dotenv
from sqlalchemy import create_engine
from config.db_config import DATABASE_URL
import os

load_dotenv(dotenv_path="config/.env")

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError(" Variável DATABASE_URL não encontrada no arquivo .env!")

engine = create_engine(DATABASE_URL, pool_pre_ping=True)

print(" Conexão com banco inicializada (via app.__init__)")
