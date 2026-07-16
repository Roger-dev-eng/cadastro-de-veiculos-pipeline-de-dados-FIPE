import json
import os
import threading
from concurrent.futures import FIRST_COMPLETED, ThreadPoolExecutor, wait
from datetime import datetime

import pandas as pd
import requests
from requests.adapters import HTTPAdapter, Retry
from sqlalchemy import text

from app.db.engine import engine

_CACHE_PATH = os.getenv("FIPE_CACHE_PATH", "logs/fipe_cache.json")
_MAX_WORKERS = int(os.getenv("FIPE_MAX_WORKERS", "10"))
_TIMEOUT = int(os.getenv("FIPE_TIMEOUT", "10"))

_cache = {}
_cache_dirty = False
_cache_lock = threading.Lock()
_thread_local = threading.local()

retry_strategy = Retry(
    total=3,
    backoff_factor=0.3,
    status_forcelist=[429, 500, 502, 503, 504]
)


def _get_session():
    session = getattr(_thread_local, "session", None)
    if session is None:
        session = requests.Session()
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("https://", adapter)
        session.mount("http://", adapter)
        _thread_local.session = session
    return session


def _load_cache():
    global _cache
    if not os.path.exists(_CACHE_PATH):
        _cache = {}
        return
    try:
        with open(_CACHE_PATH, "r", encoding="utf-8") as cache_file:
            _cache = json.load(cache_file)
    except (json.JSONDecodeError, OSError):
        _cache = {}


def _save_cache():
    global _cache_dirty
    with _cache_lock:
        if not _cache_dirty:
            return
        data = dict(_cache)
        _cache_dirty = False
    os.makedirs(os.path.dirname(_CACHE_PATH), exist_ok=True)
    with open(_CACHE_PATH, "w", encoding="utf-8") as cache_file:
        json.dump(data, cache_file, ensure_ascii=True)


def _cache_get(key):
    with _cache_lock:
        return _cache.get(key)


def _cache_set(key, value):
    global _cache_dirty
    with _cache_lock:
        _cache[key] = value
        _cache_dirty = True


_load_cache()


def _emit(progress_callback, event, message, **data):
    print(message)
    if callable(progress_callback):
        progress_callback({
            "event": event,
            "message": message,
            **data,
        })



def obter_marcas():
    url = "https://parallelum.com.br/fipe/api/v1/carros/marcas"
    cache_key = "marcas"
    cached = _cache_get(cache_key)
    if cached is not None:
        return cached
    try:
        resposta = _get_session().get(url, timeout=_TIMEOUT)
        resposta.raise_for_status()
        dados = resposta.json()
        if isinstance(dados, list) and all(isinstance(m, dict) for m in dados):
            _cache_set(cache_key, dados)
            return dados
        print(" Retorno inesperado da API de marcas.")
        return []
    except Exception as e:
        print(f" Erro ao obter marcas: {e}")
        return []



def obter_modelos(codigo_marca):
    url = f"https://parallelum.com.br/fipe/api/v1/carros/marcas/{codigo_marca}/modelos"
    cache_key = f"modelos:{codigo_marca}"
    cached = _cache_get(cache_key)
    if cached is not None:
        return cached
    try:
        resposta = _get_session().get(url, timeout=_TIMEOUT)
        resposta.raise_for_status()
        dados = resposta.json().get("modelos", [])
        _cache_set(cache_key, dados)
        return dados
    except Exception as e:
        print(f" Erro ao obter modelos da marca {codigo_marca}: {e}")
        return []



def obter_anos(codigo_marca, codigo_modelo):
    url = f"https://parallelum.com.br/fipe/api/v1/carros/marcas/{codigo_marca}/modelos/{codigo_modelo}/anos"
    cache_key = f"anos:{codigo_marca}:{codigo_modelo}"
    cached = _cache_get(cache_key)
    if cached is not None:
        return cached
    try:
        resposta = _get_session().get(url, timeout=_TIMEOUT)
        resposta.raise_for_status()
        dados = resposta.json()
        _cache_set(cache_key, dados)
        return dados
    except Exception as e:
        print(f" Erro ao obter anos [{codigo_marca}/{codigo_modelo}]: {e}")
        return []



def obter_detalhes(codigo_marca, codigo_modelo, codigo_ano):
    url = f"https://parallelum.com.br/fipe/api/v1/carros/marcas/{codigo_marca}/modelos/{codigo_modelo}/anos/{codigo_ano}"
    cache_key = f"detalhes:{codigo_marca}:{codigo_modelo}:{codigo_ano}"
    cached = _cache_get(cache_key)
    if cached is not None:
        return cached
    try:
        resposta = _get_session().get(url, timeout=_TIMEOUT)
        resposta.raise_for_status()
        dados = resposta.json()
        _cache_set(cache_key, dados)
        return dados
    except Exception as e:
        print(f" Erro ao obter detalhes: {e}")
        return {}



def _coletar_detalhe(cod_marca, nome_marca, cod_modelo, nome_modelo, cod_ano):
    try:
        detalhe = obter_detalhes(cod_marca, cod_modelo, cod_ano)
        if not detalhe:
            return None

        ano_modelo = detalhe.get("AnoModelo")
        if isinstance(ano_modelo, int):
            if not (1900 <= ano_modelo <= datetime.now().year):
                ano_modelo = None
        else:
            ano_modelo = None

        return {
            "marca": nome_marca,
            "modelo": nome_modelo,
            "ano_modelo": ano_modelo,
            "combustivel": detalhe.get("Combustivel"),
            "valor_str": detalhe.get("Valor"),
            "valor": _limpar_valor(detalhe.get("Valor")),
            "codigo_fipe": detalhe.get("CodigoFipe"),
            "sigla_combustivel": detalhe.get("SiglaCombustivel"),
            "data_consulta": detalhe.get("DataConsulta")
        }
    except requests.RequestException as e:
        print(f"\n API Error [{nome_marca} {nome_modelo}]: {e}")
        return None
    except Exception as e:
        print(f"\n Unexpected error [{nome_marca} {nome_modelo}]: {e}")
        return None


def _drain_futures(futures, registros, limite_registros, progress_callback=None):
    done, _ = wait(futures, return_when=FIRST_COMPLETED)
    for future in done:
        futures.remove(future)
        resultado = future.result()
        if resultado:
            registros.append(resultado)
            if len(registros) % 10 == 0:
                print(f" Registros coletados: {len(registros)}", end="\r")
                if callable(progress_callback):
                    progress_callback({
                        "event": "records",
                        "message": f"{len(registros)} registros coletados",
                        "current": len(registros),
                        "total": limite_registros,
                    })
            if len(registros) >= limite_registros:
                return True
    return False


def coletar_dados_fipe(limite_registros=600, progress_callback=None):
    registros = []
    marcas = obter_marcas()

    _emit(
        progress_callback,
        "collect_start",
        f"Coletando dados da API FIPE (limite: {limite_registros})",
        current=0,
        total=limite_registros,
    )

    with ThreadPoolExecutor(max_workers=_MAX_WORKERS) as executor:
        futures = []
        for marca_index, marca in enumerate(marcas, start=1):
            cod_marca = marca.get("codigo")
            nome_marca = marca.get("nome")
            _emit(
                progress_callback,
                "brand",
                f"Processando marca {marca_index}/{len(marcas)}: {nome_marca}",
                current=len(registros),
                total=limite_registros,
                brand=nome_marca,
            )

            modelos = obter_modelos(cod_marca)
            for modelo in modelos:
                cod_modelo = modelo["codigo"]
                nome_modelo = modelo["nome"]

                anos = obter_anos(cod_marca, cod_modelo)
                if not anos:
                    continue

                for ano in anos:
                    cod_ano = ano["codigo"] if isinstance(ano, dict) else ano
                    futures.append(
                        executor.submit(
                            _coletar_detalhe,
                            cod_marca,
                            nome_marca,
                            cod_modelo,
                            nome_modelo,
                            cod_ano
                        )
                    )

                    if len(futures) >= _MAX_WORKERS * 4:
                        limite_atingido = _drain_futures(
                            futures,
                            registros,
                            limite_registros,
                            progress_callback,
                        )
                        if limite_atingido:
                            _emit(
                                progress_callback,
                                "collect_limit",
                                f"Limite de {limite_registros} registros atingido",
                                current=len(registros),
                                total=limite_registros,
                            )
                            _save_cache()
                            return pd.DataFrame(registros)

        while futures:
            limite_atingido = _drain_futures(
                futures,
                registros,
                limite_registros,
                progress_callback,
            )
            if limite_atingido:
                _emit(
                    progress_callback,
                    "collect_limit",
                    f"Limite de {limite_registros} registros atingido",
                    current=len(registros),
                    total=limite_registros,
                )
                _save_cache()
                return pd.DataFrame(registros)

    _save_cache()
    df = pd.DataFrame(registros)
    _emit(
        progress_callback,
        "collect_done",
        f"Total de registros coletados: {len(df)}",
        current=len(df),
        total=limite_registros,
    )
    return df



def _limpar_valor(valor):
    if not valor:
        return None
    try:
        limpo = valor.replace("R$", "").replace(".", "").replace(",", ".").strip()
        return float(limpo)
    except (ValueError, AttributeError):
        return None


def salvar_no_banco(df, progress_callback=None):
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
            _emit(progress_callback, "save_empty", "Nenhum dado coletado. Tabela garantida.")
            return {
                "collected": 0,
                "valid": 0,
                "inserted": 0,
                "existing": 0,
            }

        collected_count = len(df)
        df = df.copy()
        df["ano_modelo"] = df["ano_modelo"].apply(
            lambda x: int(x) if pd.notna(x) else None
        )
        df["valor"] = df["valor"].where(pd.notna(df["valor"]), None)

        df = df[
            df["codigo_fipe"].notna() &
            df["ano_modelo"].notna() &
            df["valor"].notna()
        ]

        if df.empty:
            _emit(progress_callback, "save_empty", "Nenhum dado valido apos filtros.")
            return {
                "collected": collected_count,
                "valid": 0,
                "inserted": 0,
                "existing": 0,
            }

        batch_size = 100
        total_inserido = 0
        total_validos = len(df)
        total_batches = (len(df) + batch_size - 1) // batch_size

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

        _emit(
            progress_callback,
            "save_start",
            f"Salvando {len(df)} registros em {total_batches} batches",
            current=0,
            total=total_batches,
        )

        for i in range(0, len(df), batch_size):
            batch = df.iloc[i:i + batch_size]
            batch_number = i // batch_size + 1
            try:
                result = conn.execute(insert_sql, batch.to_dict(orient="records"))
                inserted_batch = result.rowcount or 0
                total_inserido += inserted_batch
                print(f" Batch {batch_number}: {len(batch)} registros processados", end="\r")
                if callable(progress_callback):
                    progress_callback({
                        "event": "save_batch",
                        "message": (
                            f"Batch {batch_number}/{total_batches}: "
                            f"{inserted_batch} novos, {len(batch) - inserted_batch} ja existentes"
                        ),
                        "current": batch_number,
                        "total": total_batches,
                        "inserted": total_inserido,
                        "existing": (i + len(batch)) - total_inserido,
                    })
            except Exception as e:
                _emit(
                    progress_callback,
                    "save_error",
                    f"Erro no batch {batch_number}: {e}",
                    current=batch_number,
                    total=total_batches,
                )
                continue

        _emit(
            progress_callback,
            "save_done",
            (
                f"Insercao finalizada: {total_inserido} novos, "
                f"{total_validos - total_inserido} ja existentes"
            ),
            current=total_batches,
            total=total_batches,
            collected=collected_count,
            valid=total_validos,
            inserted=total_inserido,
            existing=total_validos - total_inserido,
        )
        return {
            "collected": collected_count,
            "valid": total_validos,
            "inserted": total_inserido,
            "existing": total_validos - total_inserido,
        }


def importar_dados_fipe(limite_registros=None, progress_callback=None):
    """Funcao principal: coleta e salva dados da FIPE."""
    if limite_registros is None:
        limite_registros = int(os.getenv("RECORDS_LIMIT", "600"))
    _emit(progress_callback, "start", "Pipeline FIPE iniciado")
    df = coletar_dados_fipe(limite_registros, progress_callback)
    summary = salvar_no_banco(df, progress_callback)
    _emit(
        progress_callback,
        "done",
        "Pipeline FIPE concluido com sucesso",
        current=limite_registros,
        total=limite_registros,
        summary=summary,
    )
    return summary


if __name__ == "__main__":
    importar_dados_fipe()
