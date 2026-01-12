import requests
from requests.adapters import HTTPAdapter, Retry
import pandas as pd
from sqlalchemy import text
from app import engine

session = requests.Session()
retry_strategy = Retry(
    total=3,
    backoff_factor=0.3,
    status_forcelist=[429,500,502,503,504]
)
adapter = HTTPAdapter(max_retries=retry_strategy)
session.mount("https://", adapter)
session.mount("http://", adapter)

def obter_marcas():
    url = "https://parallelum.com.br/fipe/api/v1/carros/marcas"
    try:
        resposta = session.get(url, timeout=10)
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
    resposta = session.get(url, timeout=10)
    return resposta.json().get("modelos", [])

def obter_anos(codigo_marca, codigo_modelo):
    url = f"https://parallelum.com.br/fipe/api/v1/carros/marcas/{codigo_marca}/modelos/{codigo_modelo}/anos"
    resposta = session.get(url, timeout=10)
    return resposta.json()

def obter_detalhes(codigo_marca, codigo_modelo, codigo_ano):
    url = f"https://parallelum.com.br/fipe/api/v1/carros/marcas/{codigo_marca}/modelos/{codigo_modelo}/anos/{codigo_ano}"
    resposta = session.get(url, timeout=10)
    return resposta.json()

def coletar_dados_fipe(limite_registros=650):
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
                    if isinstance(ano_modelo, int):
                        if not (1800 <=ano_modelo <=2026):
                          ano_modelo = None
                    else:
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
                except requests.RequestException as e:
                    print(f"API Error [{nome_marca} {nome_modelo}]: {e}")
                    continue
                except Exception as e:
                    print(f"Unexpected error [{nome_marca} {nome_modelo}]: {e}")
                    continue

    df = pd.DataFrame(registros)
    print(f"\nTotal de registros coletados: {len(df)}")
    return df

def _limpar_valor(valor):
    if not valor:
        return None
    try:
        limpo = valor.replace("R$", "").replace(".", "").replace(",", ".").strip()
        return float(limpo)
    except (ValueError, AttributeError):
        return None

def salvar_no_banco(df):
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

        if df.empty:
            print("\nNenhum dado coletado. Tabela garantida.")
            return
        
        df = df.copy()
        df["ano_modelo"] = df["ano_modelo"].apply(
            lambda x: int(x) if pd.notna(x) else None
        )
        df["valor"] = df["valor"].where(pd.notna(df["valor"]), None)

        df = df [
            df["codigo_fipe"].notna() &
            df["ano_modelo"].notna() &
            df["valor"].notna()
        ]

        if df.empty:
            print("\nNenhun dado válido após filtros.")
            return

        batch_size = 100
        total_inserido = 0    

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

        for i in range(0, len(df), batch_size):
            batch = df.iloc[i:i + batch_size]
            try:
                conn.execute(insert_sql,batch.to_dict(orient="records"))
                total_inserido += len(batch)
                print(f"Batch {i//batch_size + 1}: {len(batch)} registros", end="\r")
            except Exception as e:
                print(f"\n Erro no batch {i//batch_size +1}: {e}")
                continue
        print(f"\n Total inserido: {total_inserido} registros")        

def importar_dados_fipe(limite_registros=650):
    df = coletar_dados_fipe(limite_registros)
    salvar_no_banco(df)
    print("\n Pipeline FIPE concluído com sucesso.")
    print("Observe as análise em notebooks/analise_fipe.ipynb")

if __name__ == "__main__":
    importar_dados_fipe()
