import sys
from pathlib import Path

import pandas as pd
import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.dashboard.charts import (
    price_by_brand,
    price_by_fuel,
    price_by_year,
    price_distribution,
)
from app.dashboard.queries import get_engine, load_fipe_data, table_exists


st.set_page_config(
    page_title="Dashboard FIPE",
    layout="wide",
)


@st.cache_resource(show_spinner=False)
def cached_engine():
    return get_engine()


@st.cache_data(ttl=300, show_spinner="Carregando dados da FIPE...")
def cached_data():
    engine = cached_engine()
    if not table_exists(engine):
        return pd.DataFrame()
    return load_fipe_data(engine)


def format_currency(value):
    if pd.isna(value):
        return "-"
    return f"R$ {value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def apply_filters(df):
    with st.sidebar:
        st.header("Filtros")

        brands = sorted(df["marca"].dropna().unique())
        selected_brands = st.multiselect("Marca", brands, default=brands)

        base = df[df["marca"].isin(selected_brands)] if selected_brands else df

        fuels = sorted(base["combustivel"].dropna().unique())
        selected_fuels = st.multiselect("Combustivel", fuels, default=fuels)

        min_year = int(base["ano_modelo"].min())
        max_year = int(base["ano_modelo"].max())
        selected_years = st.slider("Ano modelo", min_year, max_year, (min_year, max_year))

        max_rows = st.number_input("Linhas na tabela", min_value=10, max_value=500, value=100, step=10)

    filtered = base[
        base["combustivel"].isin(selected_fuels)
        & base["ano_modelo"].between(selected_years[0], selected_years[1])
    ]
    return filtered, max_rows


def render_pipeline_action():
    with st.sidebar:
        st.divider()
        st.header("Pipeline")
        limit = st.number_input("Limite de registros", min_value=10, max_value=5000, value=370, step=10)
        if st.button("Importar dados FIPE", type="primary"):
            with st.spinner("Executando pipeline..."):
                from app.pipeline.fipe_import import importar_dados_fipe

                importar_dados_fipe(limite_registros=int(limit))
                st.cache_data.clear()
            st.success("Importacao concluida.")
            st.rerun()


def render_empty_state():
    st.info(
        "A tabela fipe_carros ainda nao existe ou nao possui dados. "
        "Execute o pipeline pelo terminal com `python run.py` ou use o botao de importacao na barra lateral."
    )
    render_pipeline_action()


def main():
    st.title("Dashboard FIPE")
    st.caption("Consulta e analise dos dados coletados da API FIPE e armazenados no PostgreSQL.")

    try:
        df = cached_data()
    except Exception as exc:
        st.error(f"Nao foi possivel carregar os dados: {exc}")
        return

    if df.empty:
        render_empty_state()
        return

    df = df.dropna(subset=["valor", "ano_modelo"]).copy()
    df["ano_modelo"] = df["ano_modelo"].astype(int)

    render_pipeline_action()
    filtered, max_rows = apply_filters(df)

    total_records = len(filtered)
    avg_price = filtered["valor"].mean()
    max_price = filtered["valor"].max()
    brands_count = filtered["marca"].nunique()

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Registros", f"{total_records:,}".replace(",", "."))
    col2.metric("Marcas", f"{brands_count:,}".replace(",", "."))
    col3.metric("Preco medio", format_currency(avg_price))
    col4.metric("Maior preco", format_currency(max_price))

    if filtered.empty:
        st.warning("Nenhum registro encontrado para os filtros selecionados.")
        return

    tab_overview, tab_distribution, tab_table = st.tabs(["Visao geral", "Distribuicao", "Dados"])

    with tab_overview:
        left, right = st.columns([1.25, 1])
        with left:
            st.subheader("Preco medio por marca")
            st.plotly_chart(price_by_brand(filtered), use_container_width=True)
        with right:
            st.subheader("Preco medio por combustivel")
            st.plotly_chart(price_by_fuel(filtered), use_container_width=True)

        st.subheader("Evolucao do preco medio por ano")
        st.plotly_chart(price_by_year(filtered), use_container_width=True)

    with tab_distribution:
        st.subheader("Distribuicao de precos")
        st.plotly_chart(price_distribution(filtered), use_container_width=True)

    with tab_table:
        st.subheader("Registros")
        visible_columns = [
            "marca",
            "modelo",
            "ano_modelo",
            "combustivel",
            "valor_str",
            "codigo_fipe",
            "data_consulta",
        ]
        st.dataframe(
            filtered[visible_columns].head(int(max_rows)),
            use_container_width=True,
            hide_index=True,
        )


if __name__ == "__main__":
    main()
