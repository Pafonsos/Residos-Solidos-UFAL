import dash
from dash import html

app = dash.Dash(__name__)

app.layout = html.Div([
    html.Div([
        html.Div([html.Div([
            html.Button('Bairro', className="botão"),
            html.Button('Região Administrativa', className="botão")], className="card-filtros-conteudo")], className="card-filtros"),
        html.Div([
            html.Div(className="card-grande"),
            html.Div(className="card-grande"),
        ], className="cards")
    ], className="espaçamento")
], className="m-container")

if __name__ == "__main__":
    app.run(debug=True)