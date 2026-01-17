from dotenv import load_dotenv
from sqlalchemy import create_engine
import os

load_dotenv(dotenv_path=".env")

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL nao definida")

engine = create_engine(DATABASE_URL, pool_pre_ping=True)

