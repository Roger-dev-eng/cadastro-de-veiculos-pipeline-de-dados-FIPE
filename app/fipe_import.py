import requests
import time
import pandas as pd
from sqlalchemy import text
from tqdm import tqdm
from app import engine 

def obter_marcas():
    url = "https://parallelum.com.br/fipe/api/v1/carros/marcas"
    try:
        resposta = requests.get(url)
        time.sleep(0.5)
        resposta.raise_for_status()
        dados = resposta.json()
        if isinstance(dados, list) and all(isinstance(m, dict) for m in dados):
            return dados
        print(" Retorno inesperado da API de marcas.")
        return []
    except Exception as e:
        print(f" Erro ao obter marcas: {e}")
        return []

def obter_modelos(codigo_marca):
    url = f"https://parallelum.com.br/fipe/api/v1/carros/marcas/{codigo_marca}/modelos"
    resposta = requests.get(url)
    time.sleep(0.5)
    return resposta.json().get("modelos", [])

def obter_anos(codigo_marca, codigo_modelo):
    url = f"https://parallelum.com.br/fipe/api/v1/carros/marcas/{codigo_marca}/modelos/{codigo_modelo}/anos"
    resposta = requests.get(url)
    time.sleep(0.5)
    return resposta.json()

def obter_detalhes(codigo_marca, codigo_modelo, codigo_ano):
    url = f"https://parallelum.com.br/fipe/api/v1/carros/marcas/{codigo_marca}/modelos/{codigo_modelo}/anos/{codigo_ano}"
    resposta = requests.get(url)
    time.sleep(0.5)
    return resposta.json()

def coletar_dados_fipe(limite_registros=700):
    registros = []
    marcas = obter_marcas()
    contador = 0

    print(f"\nColetando dados da API da FIPE (limite: {limite_registros})...\n")

    for marca in marcas:
        cod_marca = marca.get("codigo")
        nome_marca = marca.get("nome")
        print(f"Processando marca: {nome_marca}")

        modelos = obter_modelos(cod_marca)
        for modelo in modelos:
            cod_modelo = modelo["codigo"]
            nome_modelo = modelo["nome"]

            anos = obter_anos(cod_marca, cod_modelo)
            if not anos:
                continue

            for ano in anos:
                cod_ano = ano["codigo"] if isinstance(ano, dict) else ano
                try:
                    detalhe = obter_detalhes(cod_marca, cod_modelo, cod_ano)
                    ano_modelo = detalhe.get("AnoModelo")
                    if isinstance(ano_modelo, int) and ano_modelo > 2025:
                        ano_modelo = None
                        
                    registros.append({
                        "marca": nome_marca,
                        "modelo": nome_modelo,
                        "ano_modelo": ano_modelo,
                        "combustivel": detalhe.get("Combustivel"),
                        "valor_str": detalhe.get("Valor"),
                        "valor": _limpar_valor(detalhe.get("Valor")),
                        "codigo_fipe": detalhe.get("CodigoFipe"),
                        "sigla_combustivel": detalhe.get("SiglaCombustivel"),
                        "data_consulta": detalhe.get("DataConsulta")
                    })
                    contador += 1
                    print(f"Registros coletados: {contador}", end="\r")
                    if contador >= limite_registros:
                        print(f"\nLimite de {limite_registros} registros atingido.")
                        return pd.DataFrame(registros)
                except Exception as e:
                    print(f"Erro ao obter detalhes de {nome_marca} {nome_modelo} ({cod_ano}): {e}")
                    continue

    df = pd.DataFrame(registros)
    print(f"\nTotal de registros coletados: {len(df)}")
    return df



def _limpar_valor(valor):
    if not valor:
        return None
    try:
        return float(valor.replace("R$", "").replace(".", "").replace(",", ".").strip())
    except:
        return None

def salvar_no_banco(df):
    if df.empty:
        print("\nNenhum dado coletado.")
        return

    with engine.begin() as conn:
        conn.execute(text("""
        CREATE TABLE IF NOT EXISTS fipe_carros (
            id SERIAL PRIMARY KEY,
            marca VARCHAR(100),
            modelo VARCHAR(150),
            ano_modelo INTEGER,
            combustivel VARCHAR(50),
            valor_str VARCHAR(20),
            valor FLOAT,
            codigo_fipe VARCHAR(20),
            sigla_combustivel VARCHAR(10),
            data_consulta VARCHAR(50),
            CONSTRAINT unique_fipe UNIQUE (codigo_fipe, ano_modelo, combustivel)
        );
        """))

        insert_sql = text("""
        INSERT INTO fipe_carros (
          marca, modelo, ano_modelo, combustivel,
          valor_str, valor, codigo_fipe,
          sigla_combustivel, data_consulta
        ) VALUES (
          :marca, :modelo, :ano_modelo, :combustivel,
          :valor_str, :valor, :codigo_fipe,
          :sigla_combustivel, :data_consulta
        )
        ON CONFLICT (codigo_fipe, ano_modelo, combustivel)
        DO NOTHING
        """)

        conn.execute(insert_sql, df.to_dict(orient="records"))


    print(f"{len(df)} registros inseridos com sucesso no PostgreSQL.")


def importar_dados_fipe(limite_registros=1000):
    df = coletar_dados_fipe(limite_registros)
    salvar_no_banco(df)
    print("\n Pipeline FIPE concluído com sucesso.")

if __name__ == "__main__":
    importar_dados_fipe()
