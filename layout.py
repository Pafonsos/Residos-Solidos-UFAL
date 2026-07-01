from dash import html, dcc

layout = html.Div([
    html.H1('Geração de resíduos sólidos de Maceió-AL', style={'color': 'white'}),
    html.Div([

        html.Div([
            html.Div([
                html.Div([
                    html.Span('Visualização:', className="Texto-dropdown"),
                    dcc.RadioItems(['Diario', 'Mensal', 'Anual'], 'Anual', inline=True, labelClassName="botão-visualização", id='radio-visualizacao')
                ], className="card-filtros-conteudo-cima"),

                html.Div([
                    html.Span('Periodo:', className="Texto-dropdown"),
                    dcc.Input(type='text', className="input-pesquisa",id='inicial',placeholder="DD/MM/AAAA"),
                    dcc.Input(type='text', className="input-pesquisa",id='final', placeholder="DD/MM/AAAA")
                ], className="card-filtros-conteudo-baixo"),
            ]
            ,className="card-filtros-conteudo-esquerda"),

            html.Div([
                dcc.RadioItems(['Bairro', 'Região Administrativa'], 'Região Administrativa', inline=True, labelClassName="botão", id='radio-bairro-regiao'),
                html.Span('Selecionar:', className="Texto-dropdown"),
                dcc.Dropdown(
                    options=[
                        {'label': 'Maceio', 'value': 'xxxxxxxxxxx'},
                        {'label': 'biu', 'value': 'xxxxxxxxxx'},
                    ],
                    value='xxxxxxxxxxx',
                    clearable=False,
                    searchable=False,
                    className="dropdown",
                    id='dropdown-selecionar'
                )
            ], className="card-filtros-conteudo-centro"),

        ], className="card-filtros"),

        html.Div([
            html.Div(className="card-grande", id='card-grande-1'),
            html.Div(className="card-grande", id='card-grande-2'),
        ], className="cards")

    ], className="espaçamento")
], className="m-container")