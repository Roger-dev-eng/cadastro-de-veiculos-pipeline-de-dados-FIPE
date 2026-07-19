import subprocess
import sys
from pathlib import Path

from app.utils.funcoes import log


PROJECT_ROOT = Path(__file__).resolve().parent
DASHBOARD_FILE = PROJECT_ROOT / "app" / "dashboard" / "dashboard.py"

if __name__ == "__main__":
    log(" Iniciando dashboard Streamlit da FIPE...")
    subprocess.run(
        [
            sys.executable,
            "-m",
            "streamlit",
            "run",
            str(DASHBOARD_FILE),
        ],
        cwd=PROJECT_ROOT,
        check=True,
    )
