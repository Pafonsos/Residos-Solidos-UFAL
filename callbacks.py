from dash import callback, Input, Output, State
import dash


BAIRROS = ['Antares', 'Barro Duro', 'Bebedouro', 'Benedito Bentes', 'Bom Parto', 'Canaã','Centro',
'Chã da Jaqueira',
'Chã de Bebedouro',
'Cidade Universitária',
'Clima Bom',
'Cruz das Almas',
'Farol',
'Feitosa',
'Fernão Velho',
'Garça Torta',
'Gruta de Lourdes',
'Guaxuma',
'Ipioca',
'Jacarecica',
'Jacintinho',
'Jaraguá',
'Jardim Petrópolis',
'Jatiúca',
'Levada',
'Mangabeiras',
'Mutange',
'Ouro Preto',
'Pajuçara',
'Pescaria',
'Petrópolis',
'Pinheiro',
'Pitanguinha',
'Poço',
'Ponta da Terra',
'Ponta Grossa',
'Ponta Verde',
'Pontal da Barra',
'Prado',
'Riacho Doce',
'Rio Novo',
'Santa Amélia',
'Santa Lúcia',
'Santo Amaro',
'Santos Dumont',
'São Jorge',
'Serraria',
'Tabuleiro do Martins',
'Trapiche da Barra',
'Vergel do Lago']
REGIOES_ADM = ['Região 1', 'Região 2', 'Região 3', 'Região 4', 'Região 5', 'Região 6', 'Região 7', 'Região 8']

def callbacks(app):
    
    
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
    def MAPA(viz, bairro_regiao, local):
        """
        Atualiza o MAPA baseado nas seleções
        """
        return f"MAPA: {viz} - {bairro_regiao}: {local}"
    
    
    @callback(
        Output('card-grande-2', 'children'),
        Input('radio-visualizacao', 'value'),
        Input('radio-bairro-regiao', 'value'),
        Input('dropdown-selecionar', 'value'),
    )
    def grafico(viz, bairro_regiao, local):
        """
        Atualiza O gráfico baseado nas seleções
        """
        return f"Gráfico: {viz} - {bairro_regiao}: {local}"
