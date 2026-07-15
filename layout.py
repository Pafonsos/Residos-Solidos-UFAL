from dash import html, dcc
from datetime import date

layout = html.Div([
    html.H1('Geração de resíduos sólidos de Maceió-AL', style={'color': 'white'}),
    html.Div([

        html.Div([
            html.Div([
                html.Div([
                    html.Span('Visualização:', className="Texto-dropdown"),
                    dcc.RadioItems(
                        options=[
                            {'label': html.Span('Diario', className="botão-visualização"), 'value': 'Diario'},
                            {'label': html.Span('Mensal', className="botão-visualização"), 'value': 'Mensal'},
                            {'label': html.Span('Anual', className="botão-visualização"), 'value': 'Anual'},
                        ],
                        value='Anual',
                        inline=True,
                        labelClassName="opcao-radio",
                        inputClassName="radio-input",
                        id='radio-visualizacao'
                    )
                ], className="card-filtros-conteudo-cima"),

                html.Div([
                    html.Span('Periodo:', className="Texto-dropdown"),
                    html.Div([
                        dcc.DatePickerSingle(
                            id='inicial',
                            display_format='DD/MM/YYYY',
                            month_format='MMMM YYYY',
                            placeholder='DD/MM/AAAA'
                        ),
                        dcc.DatePickerSingle(
                            id='final',
                            display_format='DD/MM/YYYY',
                            month_format='MMMM YYYY',
                            placeholder='DD/MM/AAAA'
                        )
                    ], className='Date'
                    ),
                    html.Div(id='output-periodo')
                ], className="card-filtros-conteudo-baixo"),
            ]
            ,className="card-filtros-conteudo-esquerda"),

            html.Div([
                dcc.RadioItems(
                    options=[
                        {'label': html.Span('Bairro', className="botão"), 'value': 'Bairro'},
                        {'label': html.Span('Região Administrativa', className="botão"), 'value': 'Região Administrativa'},
                    ],
                    value='Região Administrativa',
                    inline=True,
                    labelClassName="opcao-radio",
                    inputClassName="radio-input",
                    id='radio-bairro-regiao'
                )
            ], className="card-filtros-conteudo-centro"),

            html.Div([
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
            ], className="card-filtros-conteudo-direita"),

        ], className="card-filtros"),

        html.Div([
            html.Div(className="card-grande", id='card-grande-1'),
            html.Div(className="card-grande", id='card-grande-2'),
        ], className="cards")

    ], className="espaçamento")
], className="m-container")
