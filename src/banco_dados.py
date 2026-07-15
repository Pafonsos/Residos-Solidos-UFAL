from sqlmodel import SQLModel, create_engine, Session, select
import sqlalchemy
from datetime import datetime
from src.models import *
import pandas as pd
from src.dados_ibge import dados_bairros

"""
Bando de Dados.
"""
def iniciar_banco_dados() -> sqlalchemy.engine.Engine: # type: ignore
  engine = create_engine("sqlite:///banco.db", echo=True)
  return engine

def criar_banco_dados(engine: sqlalchemy.engine.Engine) -> sqlalchemy.engine.Engine: # type: ignore
  SQLModel.metadata.create_all(engine)

def get_session():
    """Retorna uma sessão do banco de dados."""
    engine = iniciar_banco_dados()
    session = Session(engine)
    return session

def salvar_bairros() -> None: # type: ignore
    registros = dados_bairros()
    with get_session() as session:
        existentes = session.exec(select(Bairros.nome)).all()
        existentes = set(existentes)

        novos = [
            Bairros(**registro)
            for registro in registros
            if registro['nome'] not in existentes
        ]

        if not novos:
            return

        session.add_all(novos)
        session.commit()

def salvar_rotas() -> None: # type: ignore ---> REFERENCIAR MELHOR O ARQUIVO EXCEL
    arquivo_excel = 'rotas_referencia.xlsx'
    
    df = pd.read_excel(arquivo_excel)

    with get_session() as session:
        try:
            bairros = session.exec(select(Bairros)).all()
            rotas_existentes = session.exec(select(Rotas.nome)).all()

            mapa_bairros = {
                bairro.nome.strip(): bairro.id
                for bairro in bairros
            }

            rotas_existentes = set(rotas_existentes)

            for _, row in df.iterrows():
                nome_rota = str(row["ROTA"]).strip()
                nome_bairro = str(row["BAIRRO_CHAVE_ESTRANGEIRA"]).strip()

                id_bairro = mapa_bairros.get(nome_bairro)

                if not id_bairro or nome_rota in rotas_existentes:
                    continue

                session.add(
                    Rotas(
                        nome=nome_rota,
                        id_bairros=id_bairro
                    )
                )

                rotas_existentes.add(nome_rota)

            session.commit()

        except Exception as erro:
            session.rollback()

def salvar_arquivo(arquivo: str) -> int: # type: ignore
    with get_session() as session:

        registro = EtiquetaArquivo(
            name=arquivo.name,
            extension=arquivo.suffix,
            size=arquivo.stat().st_size,
            crete_date=datetime.fromtimestamp(
                arquivo.stat().st_birthtime
            ),
            modified_date=datetime.fromtimestamp(
                arquivo.stat().st_mtime
            ),
            last_access=datetime.fromtimestamp(arquivo.stat().st_atime),
        )

        session.add(registro)
        session.flush()
        session.commit()
        return registro.id

def salvar_dados_brutos(df_bruto: pd.DataFrame, id_gerador: int) -> None: # type: ignore
    if df_bruto.empty:
        return

    df = df_bruto.copy()
    mapeamento = {
        'TICKET DE PESSAGEM': 'ticket_pessagem',
        'PLACA': 'placa',
        'DATA DE SAÍDA': 'data_de_saida',
        'HORA DE SAÍDA': 'hora_de_saida',
        'NOME GERADOR': 'nome_gerador',
        'NOME PRODUTO': 'nome_produto',
        'QUANTIDADE A FATURAR': 'quantidade_a_faturar',
        'TRANSPORTADORA': 'transportadora',
        'MODELO DO CAMINHÃO': 'modelo_caminhao',
        'status_rota': 'status_rota',
        'id_rota': 'id_rota'
    }

    cols = [c for c in mapeamento.keys() if c in df.columns]
    if not cols:
        return
    
    df.rename(columns={c: mapeamento[c] for c in cols}, inplace=True)
    lista_linhas = []

    for _, row in df.iterrows():
        linha = row.to_dict()
        linha['id_gerador'] = id_gerador
        
        # if 'quantidade_a_faturar' in linha:
        #     val = linha['quantidade_a_faturar']
        #     if pd.isna(val):
        #         linha['quantidade_a_faturar'] = None

        if linha.get("id_rota") is not None and not pd.isna(linha["id_rota"]):
            linha["id_rota"] = int(linha["id_rota"])

        if "data_de_saida" in linha and "hora_de_saida" in linha:
            d = linha["data_de_saida"]
            h = linha["hora_de_saida"]

            if pd.notna(d) and pd.notna(h):
                texto = f"{d} {h}"

                dt = pd.to_datetime(
                    texto,
                    dayfirst=True,
                    errors="coerce"
                )

                if pd.isna(dt):
                    linha["data_de_saida"] = None
                    linha["hora_de_saida"] = None
                else:
                    dt = dt.to_pydatetime()
                    linha["data_de_saida"] = dt.date()  
                    linha["hora_de_saida"] = dt.time()  
                    
            else:
                linha["data_de_saida"] = None
                linha["hora_de_saida"] = None
        
        lista_linhas.append(linha)
    with get_session() as session:
        session.bulk_insert_mappings(Dataframes, lista_linhas)
        session.commit()
        

"""
Área de testes
"""

# salvar_arquivo(path, iniciar_banco_dados())
#salvar_bairros_rotas(iniciar_banco_dados())
# arquivo = Path("Rel_Pesagem_Maceio_20251002.xlsx")
# nome = arquivo.name
# criado = datetime.fromtimestamp(
#     arquivo.stat().st_birthtime
# )
# modificado = datetime.fromtimestamp(
#     arquivo.stat().st_mtime
# )
# extensao = arquivo.suffix
# tamanho = arquivo.stat().st_size
# def limpar_tabela(engine) -> int:
#     with Session(engine) as session:
#         resultado = session.exec(delete(Bairros))
#         session.commit()
#         return resultado.rowcount
# # limpar_tabela(iniciar_banco_dados())
# salvar_rotas(iniciar_banco_dados())
