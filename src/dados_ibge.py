import geopandas as gpd
import pandas as pd
import requests
from pathlib import Path

def dados_bairros():
    url = "https://ftp.ibge.gov.br/Censos/Censo_Demografico_2022/Agregados_por_Setores_Censitarios/malha_com_atributos/bairros/shp/UF/AL/AL_bairros_CD2022.zip"
    pasta = Path("dados_ibge")
    pasta.mkdir(exist_ok=True)
    arquivo_saida = pasta / "AL_bairros_CD2022.zip"

    if arquivo_saida.exists():
        print("Arquivo já existe!")
    else:
        response = requests.get(url, stream=True)

        print(response.headers.get("Last-Modified"))

        with open(arquivo_saida, "wb") as f:
            for chunk in response.iter_content(chunk_size=1024 * 1024):
                if chunk:
                    f.write(chunk)

        print("Download concluído:", arquivo_saida)

    gdf = gpd.read_file(arquivo_saida)

    gdf = gdf.loc[
        gdf["NM_MUN"] == "Maceió"
    ].copy()
    gdf = gdf.reset_index(drop=True)

    numeros = pd.to_numeric(gdf['v0001'], errors='coerce')

    print("Valores problemáticos:")
    print(gdf.loc[numeros.isna(), ['NM_BAIRRO', 'v0001']])

    gdf['v0001'] = numeros.fillna(0)

    gdf = gdf[['NM_BAIRRO', 'v0001', 'NM_SUBDIST']].copy()
    gdf = gdf.rename(columns={
            'NM_BAIRRO': 'nome',
            'v0001': 'populacao',
            'NM_SUBDIST': 'regiao_administrativa'
        })

    gdf = gdf.where(pd.notnull(gdf), None)

    return gdf.to_dict('records')
