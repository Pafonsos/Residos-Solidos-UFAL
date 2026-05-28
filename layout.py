from dash import html, dcc

layout = html.Div([
    html.Div([

        html.Div([
            html.Div([

            html.Div([
                html.Span('Visualização:', className="Texto-dropdown"),
                html.Button('Diário', className="botão-visualização"),
                html.Button('Semanal', className="botão-visualização"),
                html.Button('Mensal', className="botão-visualização"),
            ], className="card-filtros-conteudo-cima"),

            html.Div([
                html.Span('Periodo:', className="Texto-dropdown"),
                dcc.Input(type='text', className="input-pesquisa",id='inicial'),
                dcc.Input(type='text', className="input-pesquisa",id='final')
            ], className="card-filtros-conteudo-baixo"),]
            ,className="card-filtros-conteudo-esquerda"),

            html.Div([
                html.Button('Bairro', className="botão"),
                html.Button('Região Administrativa', className="botão"),
                html.Span('Selecionar:', className="Texto-dropdown"),
                dcc.Dropdown(
                    options=[
                        {'label': 'Maceio', 'value': 'xxxxxxxxxxx'},
                        {'label': 'biu', 'value': 'xxxxxxxxxx'},
                    ],
                    value='xxxxxxxxxxx',
                    clearable=False,
                    searchable=False,
                    className="dropdown"
                )
            ], className="card-filtros-conteudo-centro"),

            html.Div([
                html.Span('Escopo:', className="Texto-dropdown"),
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