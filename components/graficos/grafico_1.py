import plotly.express as px
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
ARQUIVO_PESAGEM = BASE_DIR / 'dados' / 'Rel_Pesagem_Maceio_20251002.xlsx'
SAIDA_GRAFICO = BASE_DIR / 'components' / 'graficos' / 'grafico_residuos.html'

df = pd.read_excel(ARQUIVO_PESAGEM, skiprows=3, parse_dates=["DATA DE SAÍDA"])

df_RE_BAIRRO = df.groupby('ROTA', as_index=False)['QUANTIDADE A FATURAR'].sum()

grafico = px.bar(
    df_RE_BAIRRO,
    x="ROTA",
    y="QUANTIDADE A FATURAR",
    title="Resíduos totais por bairro",
    labels={"ROTA": "Rota", "QUANTIDADE A FATURAR": "Resíduos totais"}
)

grafico.write_html(SAIDA_GRAFICO)
