from app.fipe_import import importar_dados_fipe
from app.analysis import media_preco_por_marca, media_preco_por_combustivel
from app.utils.helpers import log

if __name__ == "__main__":
    log(" Iniciando pipeline de dados FIPE...")

    importar_dados_fipe()

    media_preco_por_marca()
    media_preco_por_combustivel()

    log(" Pipeline finalizado com sucesso!")