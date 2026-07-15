"""
#tratamento de dados
"""
import pandas as pd
from src.banco_dados import *
from sqlmodel import select

def leitura_dados_brutos(caminho_arquivo):
    df_raw = pd.read_excel(caminho_arquivo, header=None)

    linha_cabecalho = None
    coluna_inicio = None

    for i, linha in df_raw.iterrows():
        for j, valor in enumerate(linha):
            if isinstance(valor, str) and valor.strip().upper() == "TICKET DE PESSAGEM":
                linha_cabecalho = i
                coluna_inicio = j
                break
        if linha_cabecalho is not None:
            break

    if linha_cabecalho is None:
        raise ValueError("Não foi possível localizar a coluna 'TICKET DE PESSAGEM' no arquivo.")

    df_bruto = df_raw.iloc[linha_cabecalho:, coluna_inicio:].reset_index(drop=True)

    df_bruto.columns = df_bruto.iloc[0]
    df_bruto = df_bruto[1:].reset_index(drop=True)

    df_bruto = df_bruto.loc[:, df_bruto.columns.notna()]
    df_bruto.columns = df_bruto.columns.astype(str)
    df_bruto = df_bruto.loc[:, ~df_bruto.columns.str.contains("Unnamed")]

    return df_bruto

def validar_dados(df_bruto):
    colunas_obrigatorias = ["TICKET DE PESSAGEM", "PLACA", "DATA DE SAÍDA", "HORA DE SAÍDA", "NOME GERADOR", "NOME PRODUTO", "QUANTIDADE A FATURAR", "TRANSPORTADORA", "MODELO DO CAMINHÃO","ROTA"]

    colunas_faltantes = [coluna for coluna in colunas_obrigatorias
                         if coluna not in df_bruto.columns]

    if colunas_faltantes:
        raise ValueError(f"Colunas obrigatórias ausentes: {colunas_faltantes}")
    return df_bruto

def criacao_status_rota(df_lido):
  df_lido["status_rota"] = "MAPEADA"
  return df_lido

def ler_tabela_de_referencia() -> pd.DataFrame: # type: ignore
    """
    Conecta ao banco de dados via engine, seleciona as rotas e retorna um DataFrame.
    Colunas retornadas: 'ROTA' (nome da rota) e 'id_rota' (id da rota no banco).
    """
    with get_session() as session:
        stmt = select(Rotas.id, Rotas.nome)
        result = session.exec(stmt).all()

        df_referencia = pd.DataFrame(result, columns=['id_rota', 'ROTA'])
        df_referencia['ROTA'] = df_referencia['ROTA'].astype(str).str.strip().str.upper()

        return df_referencia

def mapeamento_rotas(df_lido: pd.DataFrame,df_referencia: pd.DataFrame,txt_erro_path: str = "rotas_nao_encontradas.txt") -> pd.DataFrame:

    df_lido['ROTA'] = (df_lido['ROTA'].fillna('').astype(str).str.strip().str.upper())
    rota_original = df_lido['ROTA']

    df_referencia['ROTA'] = (df_referencia['ROTA'].astype(str).str.strip().str.upper())

    df_merged = pd.merge(df_lido, df_referencia[['ROTA', 'id_rota']], on='ROTA', how='left')
    df_merged['status_rota'] = 'MAPEADA'

    rota_nao_informada = (rota_original.isna() | (df_merged['ROTA'] == ''))

    rota_nao_identificada = (~rota_nao_informada & df_merged['id_rota'].isna())

    df_merged.loc[rota_nao_informada, 'status_rota'] = 'ROTA_NAO_INFORMADA'

    df_merged.loc[rota_nao_identificada, 'status_rota'] = 'ROTA_NAO_IDENTIFICADA'

    falhas = df_merged[rota_nao_identificada]

    if not falhas.empty:
        with open(txt_erro_path, 'w', encoding='utf-8') as f:
            for rota in falhas['ROTA'].dropna().unique():
                f.write(f"{rota}\n")

    return df_merged.drop(columns=['ROTA'])

#O que devo fazer igonarar linhas sem rota?
# def mapeamento_rotas(df_lido: pd.DataFrame, df_referencia: pd.DataFrame, txt_erro_path: str = "rotas_nao_encontradas.txt") -> pd.DataFrame:
    
#     df_lido['ROTA'] = df_lido['ROTA'].astype(str).str.strip().str.upper()
#     df_merged = pd.merge(df_lido, df_referencia[['ROTA', 'id_rota']], on='ROTA', how='left')
#     falhas = df_merged[df_merged['id_rota'].isna()]
    
#     if not falhas.empty:
#         rotas_falhas = falhas['nome'].unique()
        
#         with open(txt_erro_path, 'w', encoding='utf-8') as f:
#             for rota in rotas_falhas:
#                 f.write(f"- {rota}\n")
        
#     return df_merged.drop(columns=['ROTA'])


############# chamando as funções para testar ##################
# motor = iniciar_banco_dados()
# salvar_bairros(motor)
# salvar_rotas(motor)
# df_bruto = leitura_dados_brutos()
# df_lido = validar_dados(df_bruto)
# df_lido = criacao_status_rota(df_lido)
# df_referencia = ler_tabela_de_referencia(motor)
# df_pronto = mapeamento_rotas(df_lido, df_referencia)
# salvar_dados_brutos(df_pronto, salvar_arquivo(Path("Rel_Pesagem_Maceio_20251002.xlsx"), motor), motor)