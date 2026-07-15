import pandas as pd
from sqlmodel import select
from src.models import Dataframes, Rotas, Bairros  # Importe sua Session corretamente
import plotly.express as px

def carregar_dados(sessao_atual) -> pd.DataFrame:
    """
    Consulta os dados tratados e as informações complementares armazenadas no banco de dados,
    e retorna um DataFrame contendo as colunas:
    'Data da Saída', 'nome_produto', 'quantidade faturar', 'ROTAS', 'bairro',
    'região_administrativa', 'status_rota', 'população'.
    """
    
    stmt = (
        select(
            Dataframes.data_de_saida,
            Dataframes.nome_produto,
            Dataframes.quantidade_a_faturar,
            Rotas.nome.label("ROTAS"),  # Alias para 'ROTAS'
            Bairros.nome.label("bairro"),
            Bairros.regiao_administrativa.label("região_administrativa"),
            Dataframes.status_rota,
            Bairros.populacao
        )
        .join(Rotas, Dataframes.id_rota == Rotas.id)          # JOIN com Rotas
        .join(Bairros, Rotas.id_bairros == Bairros.id)        # JOIN com Bairros
    )

    with sessao_atual as session:
        resultados = session.exec(stmt)
        rows = resultados.fetchall()

    if not resultados:
        return pd.DataFrame()

    df = pd.DataFrame(
        rows,
        columns=[
            "Data da Saída",
            "nome_produto",
            "quantidade faturar",
            "ROTAS",
            "bairro",
            "região_administrativa",
            "status_rota",
            "população"
        ]
    )

    return df

def carregar_opcoes_bairros(sessao_atual):
    stmt = select(Bairros.nome)

    with sessao_atual as session:
        resultados = session.exec(stmt).all()

    df = pd.DataFrame(resultados, columns=["bairro"])
    return df

def carregar_opcoes_regioes(sessao_atual):
    stmt = select(Bairros.regiao_administrativa).distinct()

    with sessao_atual as session:
        resultados = session.exec(stmt).all()

    df = pd.DataFrame(resultados, columns=["regiao_administrativa"])
    print(df)
    return df

def filtrar_periodo(df, inicio, fim):

  df = df.copy()
  print(df)
  # Converte a coluna para datetime usando dayfirst=True
  df["Data da Saída"] = pd.to_datetime(df["Data da Saída"], dayfirst=True)

  if inicio:
    inicio = pd.to_datetime(inicio, dayfirst=True)
    df = df[df["Data da Saída"] >= inicio]

  if fim:
    fim = pd.to_datetime(fim, dayfirst=True)
    df = df[df["Data da Saída"] <= fim]

  return df

def agregar_visualizacao(df, visualizacao):

  df = df.copy()
  # Garante que a data esteja no formato datetime
  df["Data da Saída"] = pd.to_datetime(df["Data da Saída"], dayfirst=True)

  if visualizacao == "Diario":
      return (df.groupby(["Data da Saída", "bairro"], as_index=False)["quantidade faturar"].sum())

  elif visualizacao == "Mensal":
    df["Periodo"] = df["Data da Saída"].dt.to_period("M")
    return (df.groupby(["Periodo", "bairro"], as_index=False)["quantidade faturar"].sum())

  elif visualizacao == "Anual":
    df["Periodo"] = df["Data da Saída"].dt.year
    return (df.groupby(["Periodo", "bairro"], as_index=False)["quantidade faturar"].sum())


def preparar_visualizacao(df, tipo_local, local, visualizacao):

  df = df.copy()

  # Garante que a coluna de data esteja no formato datetime
  df["Data da Saída"] = pd.to_datetime(df["Data da Saída"], dayfirst=True)

  # Define qual coluna será utilizada
  if tipo_local == "Bairro":
    coluna = "bairro"
  else:
    coluna = "região_administrativa"

  # CASO 1 -> TODOS (MACEIÓ)

  if local == "Maceió":

    if tipo_local == "Bairro":
      df = (df.groupby("bairro", as_index=False).agg({"quantidade faturar": "sum", "população": "first"}))
      # Adicione esta linha para criar a coluna que o gráfico espera:
      df["percapita"] = (df["quantidade faturar"] / df["população"])

    else:

      df = (df.groupby("região_administrativa", as_index=False).agg({"quantidade faturar": "sum", "população": "sum"}))
      # Calcula o resíduo por habitante
      df["percapita"] = (df["quantidade faturar"] / df["população"])

    return df

  # CASO 2 -> BAIRRO OU REGIÃO ESPECÍFICA

    # Mantém apenas o bairro/região escolhido
  df = df[df[coluna] == local]

    #--------------------- DIÁRIO --------------------------#

  if visualizacao == "Diario":

    df = (df.groupby("Data da Saída", as_index=False).agg({"quantidade faturar": "sum"}))

    # Formata a data para não aparecer a hora
    df["Data da Saída"] = df["Data da Saída"].dt.strftime("%d/%m/%Y")

    return df

    #--------------------- MENSAL --------------------------#

  elif visualizacao == "Mensal":

    df["Periodo"] = (df["Data da Saída"].dt.to_period("M").astype(str))
    return (df.groupby("Periodo", as_index=False).agg({"quantidade faturar": "sum"}))

    #--------------------- ANUAL ---------------------------#

  elif visualizacao == "Anual":

    df["Periodo"] = df["Data da Saída"].dt.year
    return (df.groupby("Periodo", as_index=False).agg({"quantidade faturar": "sum"}))

  return df
#----------------------------------------------------------------------------------------#
def criar_grafico(df, tipo_local, local, visualizacao):

    # MACEIÓ (todos os bairros ou regiões)

    if local == "Maceió":

        if tipo_local == "Bairro":
            eixo_x = "bairro"
        else:
            eixo_x = "região_administrativa"

        fig = px.bar(df, x=eixo_x, y="quantidade faturar", hover_data={"quantidade faturar": ":,.2f", "população": True, "percapita": ":.4f"}, labels={eixo_x: tipo_local, "quantidade faturar": "Resíduo (kg)"})

    # BAIRRO OU REGIÃO ESPECÍFICA

    else:

        if visualizacao == "Diario":
            eixo_x = "Data da Saída"

        else:
            eixo_x = "Periodo"

        fig = px.bar(df, x=eixo_x, y="quantidade faturar", labels={eixo_x: visualizacao, "quantidade faturar": "Resíduo (kg)"})

    fig.update_layout(template="plotly_white", xaxis_title=None, yaxis_title="Quantidade de Resíduo", hovermode="x unified")

    return fig
