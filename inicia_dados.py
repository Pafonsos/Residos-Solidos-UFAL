from src.tratamento_de_dados import *
from src.banco_dados import *
from pathlib import Path

def montar_dados(arquivo):
    df = leitura_dados_brutos(arquivo)  
    print("--------LEU OS BRUTOS--------")
    print(df.head())
    df = validar_dados(df)
    print("--------VALIDAR--------")
    print(df.head())
    df = criacao_status_rota(df)
    print("--------STATUS_ROTASD--------")
    print(df.head())
    salvar_bairros()
    print("--------SALVAR_BAIRROS--------")
    print(df.head())
    salvar_rotas()
    print("--------SALVAR_ROTAS--------")
    print(df.head())
    df_ref = ler_tabela_de_referencia()
    print("--------TABELA_REF--------")
    print(df.head())
    df = mapeamento_rotas(df, df_ref)
    print("--------MAPEAMENTOS_ROTAS--------")
    print(df.head())
    salvar_dados_brutos(df, salvar_arquivo(Path(arquivo))) 
    print("--------SALVAR_BRUTOS--------")
    print(df.head())

#criar_banco_dados(iniciar_banco_dados())
arquivo1 = "Rel_Pesagem_Maceio_2025_Out_Dez.xlsx"
arquivo2 = "Rel_Pesagem_Maceio_20251002.xlsx"
arquivo3 = "Rel_Pesagem_Maceio_Maio_Setembro_25 (1).xlsx"
montar_dados(arquivo1)
montar_dados(arquivo2)
# montar_dados(arquivo3)