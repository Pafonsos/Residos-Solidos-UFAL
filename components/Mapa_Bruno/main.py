import geopandas as gpd
import dash
from dash import html
#Para rodar o código, é necessário instalar as bibliotecas geopandas e dash utilizando o pip:
#pip install geopandas dash
#em rode: pip install 'folium>=0.12.0' para evitar erros de compatibilidade.
#em seguida no terminal rode: python Mapa_Bruno/main.py

#READ FILE WITH GEOPANDAS AND SHOW HEADS
bairros = gpd.read_file("Mapa_Bruno/AL_bairros_CD2022/AL_bairros_CD2022.shp")
bairros.head()


#DATA PROCESSING
filter_maceio = bairros.loc[bairros['NM_MUN'] == 'Maceió']
filter_maceio = filter_maceio.drop(['CD_REGIAO', 'NM_REGIAO', 'CD_UF', 'CD_DIST', 'NM_DIST', 'CD_SUBDIST', 'CD_BAIRRO', 'CD_RGINT', 'CD_RGI', 'NM_RGI', 'CD_CONCURB', 'NM_CONCURB'], axis=1)
new_bairros = filter_maceio.explore(tiles="CartoDB positron", min_zoom=5, max_zoom=20,)
mapa_html = new_bairros._repr_html_()


#SHOW DASH
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Mapa de Bairros - Maceió"),
    html.Iframe(
        srcDoc=mapa_html,
        width='100%',
        height='600'
    )
])

if __name__ == '__main__':
    app.run(debug=False)