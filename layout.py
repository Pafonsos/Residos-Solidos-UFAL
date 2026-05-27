from dash import html, dcc

layout = html.Div([
    html.Div([

        html.Div([

            html.Div([
                html.Button('Diário', className="botão-visualização"),
                html.Button('Semanal', className="botão-visualização"),
                html.Button('Mensal', className="botão-visualização"),
            ], className="card-filtros-conteudo-esquerda"),

            html.Div([
                html.Button('Bairro', className="botão"),
                html.Button('Região Administrativa', className="botão"),
            ], className="card-filtros-conteudo-centro"),

            html.Div([
                dcc.Dropdown(
                    options=[
                        {'label': 'grafico1', 'value': 'xxxxxxxxxxx'},
                        {'label': 'grafico2', 'value': 'xxxxxxxxxx'},
                    ],
                    value='xxxxxxxxxxx',
                    clearable=False,
                    searchable=False,
                    className="dropdown"
                )
            ], className="card-filtros-conteudo-direita"),

        ], className="card-filtros"),

        html.Div([
            html.Div(className="card-grande"),
            html.Div(className="card-grande"),
        ], className="cards")

    ], className="espaçamento")
], className="m-container")