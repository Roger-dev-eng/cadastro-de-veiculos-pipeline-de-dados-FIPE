import re
import logging
from pathlib import Path

LOG_DIR = Path("logs")
LOG_DIR.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    filename=LOG_DIR / "logs.txt",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def log(msg):
    logging.info(msg)
    print(msg)

def limpar_valor(valor):
    if not valor:
        return None
    try:
        return float(valor.replace("R$", "").replace(".", "").replace(",", ".").strip())
    except:
        return None

def normalizar_texto(texto):
    if not texto:
        return ""
    texto = re.sub(r'\s+', ' ', texto.strip())
    return texto.title()

def validar_ano(ano):
    try:
        ano = int(ano)
        return 1900 <= ano <= 2025
    except:
        return False
