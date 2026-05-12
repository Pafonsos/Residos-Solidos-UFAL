import dash
from dash import html

app = dash.Dash(__name__)

app.layout = html.Div([
    html.Div([
        html.Div(className="card-filtros", children=[html.H1("Filtros")]),
        html.Div([
            html.Div(className="card-grande"),
            html.Div(className="card-grande"),
        ], className="cards")
    ], className="espaçamento")
], className="m-container")

if __name__ == "__main__":
    app.run(debug=True)