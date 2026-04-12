import geopandas as gpd
import dash
from dash import html

#READ FILE WITH GEOPANDAS AND SHOW HEADS
bairros = gpd.read_file("AL_bairros_CD2022.dbf")
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