import plotly.express as px
import pandas as pd

df = pd.read_excel('graficos/Rel_Pesagem_Maceio_20251002.xlsx', skiprows=3, parse_dates=["DATA DE SAÍDA"])

df_RE_BAIRRO = df.groupby('ROTA', as_index=False)['QUANTIDADE A FATURAR'].sum()

grafico = px.bar(
    df_RE_BAIRRO,
    x="ROTA",
    y="QUANTIDADE A FATURAR",
    title="Resíduos totais por bairro",
    labels={"ROTA": "Rota", "QUANTIDADE A FATURAR": "Resíduos totais"}
)

grafico.write_html("graficos/grafico_residuos.html")