from dash import callback, Input, Output, State
import dash


BAIRROS = ['Centro', 'Prado', 'Pajuçara', 'Mangabeiras']
REGIOES_ADM = ['Região 1', 'Região 2', 'Região 3']

def callbacks(app):
    """
    Registra todos os callbacks da aplicação
    """
    
    
    @callback(
        Output('dropdown-selecionar', 'options'),
        Output('dropdown-selecionar', 'value'),
        Input('radio-bairro-regiao', 'value'),
    )
    def dropdown(selecionar):
        """
        Atualiza as opções do dropdown baseado na seleção (Bairro ou Região Adm)
        """
        if selecionar == 'Bairro':
            options = [{'label': bairro, 'value': bairro} for bairro in BAIRROS]
            value = BAIRROS[0] if BAIRROS else None
        else:  # Região Administrativa
            options = [{'label': regiao, 'value': regiao} for regiao in REGIOES_ADM]
            value = REGIOES_ADM[0] if REGIOES_ADM else None
        
        return options, value
    
    
    @callback(
        Output('card-grande-1', 'children'),
        Input('radio-visualizacao', 'value'),
        Input('radio-bairro-regiao', 'value'),
        Input('dropdown-selecionar', 'value'),
    )
    def grafico_1(viz, bairro_regiao, local):
        """
        Atualiza o primeiro gráfico baseado nas seleções
        """
        return f"Gráfico 1: {viz} - {bairro_regiao}: {local}"
    
    
    @callback(
        Output('card-grande-2', 'children'),
        Input('radio-visualizacao', 'value'),
        Input('radio-bairro-regiao', 'value'),
        Input('dropdown-selecionar', 'value'),
    )
    def grafico_2(viz, bairro_regiao, local):
        """
        Atualiza o segundo gráfico baseado nas seleções
        """
        return f"Gráfico 2: {viz} - {bairro_regiao}: {local}"
