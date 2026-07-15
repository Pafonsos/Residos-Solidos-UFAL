from src.execucao_dashboard import *
from src.banco_dados import get_session
from dash import Input, Output, dcc

def registrar_grafico(app):
    @app.callback(
        Output('card-grande-1', 'children'),
        Input('radio-visualizacao', 'value'),
        Input('radio-bairro-regiao', 'value'),
        Input('dropdown-selecionar', 'value'),
        Input('inicial', 'value'),
        Input('final', 'value'),
    )
    def atualizar_grafico(visualizacao, tipo_localizacao, local, data_inicial, data_final):
        # Carrega os dados
        df = carregar_dados(get_session())
        # Filtra pelo período
        df = filtrar_periodo(df, data_inicial, data_final)
        # Prepara os dados conforme as opções escolhidas
        df = preparar_visualizacao(df, tipo_localizacao, local, visualizacao)
        # Cria o gráfico
        fig = criar_grafico(df, tipo_localizacao, local, visualizacao)
        return dcc.Graph(figure=fig, config={"displayModeBar": False},)
    
    @app.callback(
        Output("dropdown-selecionar", "options"),
        Output("dropdown-selecionar", "value"),
        Input("radio-bairro-regiao", "value"),
    )
    def atualizar_dropdown(tipo):
        if tipo == "Bairro":
            df = carregar_opcoes_bairros(get_session())

            options = [
                {"label": bairro, "value": bairro}
                for bairro in df["bairro"]
            ]

            options.append({"label": "Maceió", "value": "Maceió"})

        else:
            df = carregar_opcoes_regioes(get_session())  # função semelhante

            options = [
                {"label": regiao, "value": regiao}
                for regiao in df["regiao_administrativa"]
            ]

            options.append({"label": "Maceió", "value": "Maceió"})

        return options, "Maceió"
