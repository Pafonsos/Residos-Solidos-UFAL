import geopandas as gpd
import plotly.graph_objects as go

from dash import Dash, dcc, html

bairros = gpd.read_file(
    "AL_bairros_CD2022.shp",
    engine="pyogrio"
)

bairros_maceio = bairros.loc[
    bairros["NM_MUN"] == "Maceió"
].copy()

bairros_maceio = bairros_maceio.drop(columns=[
    "CD_REGIAO",
    "NM_REGIAO",
    "CD_UF",
    "CD_DIST",
    "NM_DIST",
    "CD_SUBDIST",
    "CD_BAIRRO",
    "CD_RGINT",
    "CD_RGI",
    "NM_RGI",
    "CD_CONCURB",
    "NM_CONCURB"
])

bairros_maceio = bairros_maceio.to_crs(epsg=4326)

bairros_maceio["id"] = bairros_maceio.index.astype(str)

geojson_bairros = bairros_maceio.__geo_interface__

centro = bairros_maceio.geometry.union_all().centroid

figura_mapa = go.Figure(
    go.Choroplethmap(
        geojson=geojson_bairros,
        locations=bairros_maceio["id"],
        z=list(range(len(bairros_maceio))),
        featureidkey="id",
        text=bairros_maceio["NM_BAIRRO"],
        hovertemplate="<b>%{text}</b><extra></extra>",
        marker_line_width=1,
        marker_opacity=0.45
    )
)

figura_mapa.update_layout(
    map_style="carto-positron",

    map_center={
        "lat": centro.y,
        "lon": centro.x
    },

    map_zoom=10,

    margin=dict(
        l=0,
        r=0,
        t=0,
        b=0
    )
)

app = Dash(__name__)

app.layout = html.Div([
    dcc.Graph(
        figure=figura_mapa,
        style={
            "height": "100vh"
        }
    )
])

if __name__ == "__main__":
    app.run(debug=True)

#"open-street-map"
#"white-bg"
#"carto-positron"
#"carto-darkmatter"
#"basic"
#"streets"
#"outdoors"
#"light"
#"dark"
#"satellite"
#"satellite-streets"