from app.fipe_import import importar_dados_fipe
from app.utils.funções import log

if __name__ == "__main__":
    log(" Iniciando pipeline de dados FIPE...")

    importar_dados_fipe()

    log(" Pipeline finalizado com sucesso!")