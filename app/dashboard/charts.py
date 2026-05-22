import plotly.express as px


COLOR_SEQUENCE = ["#2563eb", "#16a34a", "#f97316", "#7c3aed", "#dc2626", "#0891b2"]


def price_by_brand(df, limit=15):
    grouped = (
        df.groupby("marca", as_index=False)["valor"]
        .mean()
        .sort_values("valor", ascending=False)
        .head(limit)
    )
    fig = px.bar(
        grouped,
        x="valor",
        y="marca",
        orientation="h",
        labels={"valor": "Preco medio (R$)", "marca": "Marca"},
        color_discrete_sequence=[COLOR_SEQUENCE[0]],
    )
    fig.update_layout(yaxis={"categoryorder": "total ascending"}, height=440)
    return fig


def price_by_year(df):
    grouped = (
        df.groupby("ano_modelo", as_index=False)["valor"]
        .mean()
        .sort_values("ano_modelo")
    )
    fig = px.line(
        grouped,
        x="ano_modelo",
        y="valor",
        markers=True,
        labels={"ano_modelo": "Ano modelo", "valor": "Preco medio (R$)"},
        color_discrete_sequence=[COLOR_SEQUENCE[1]],
    )
    fig.update_layout(height=380)
    return fig


def price_by_fuel(df):
    grouped = (
        df.groupby("combustivel", as_index=False)["valor"]
        .mean()
        .sort_values("valor", ascending=False)
    )
    fig = px.bar(
        grouped,
        x="combustivel",
        y="valor",
        labels={"combustivel": "Combustivel", "valor": "Preco medio (R$)"},
        color="combustivel",
        color_discrete_sequence=COLOR_SEQUENCE,
    )
    fig.update_layout(showlegend=False, height=360)
    return fig


def price_distribution(df):
    fig = px.histogram(
        df,
        x="valor",
        nbins=40,
        labels={"valor": "Preco FIPE (R$)"},
        color_discrete_sequence=[COLOR_SEQUENCE[5]],
    )
    fig.update_layout(height=360)
    return fig
