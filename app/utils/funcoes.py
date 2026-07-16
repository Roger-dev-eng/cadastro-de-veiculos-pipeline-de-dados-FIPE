import logging
from datetime import datetime
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


def validar_ano(ano):
    try:
        ano = int(ano)
        return 1900 <= ano <= datetime.now().year
    except (ValueError, TypeError):
        return False
