from sqlmodel import Field, SQLModel # type: ignore
from datetime import date, time, datetime
from decimal import Decimal

class EtiquetaArquivo(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    extension: str
    size: int
    crete_date: datetime
    modified_date: datetime
    last_access: datetime
class Dataframes(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    id_gerador: int | None = Field(default=None, foreign_key="etiquetaarquivo.id")
    id_rota: int | None = Field(default=None, foreign_key="rotas.id")
    ticket_pessagem: str | None = Field(default=None)
    placa: str | None = Field(default=None)
    data_de_saida: date  | None = Field(default=None)
    hora_de_saida: time  | None = Field(default=None)
    nome_gerador: str | None = Field(default=None)
    nome_produto: str | None = Field(default=None)
    quantidade_a_faturar: Decimal | None = Field(default=0, max_digits=9, decimal_places=2) 
    transportadora: str | None = Field(default=None)
    modelo_caminhao: str | None = Field(default=None)
    status_rota: str | None = Field(default=None)
class Bairros(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    nome: str | None = Field(default=None)
    regiao_administrativa: int | None = Field(default=None)
    populacao: int | None = Field(default=None)
class Rotas(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    id_bairros: int | None = Field(default=None)
    nome: str | None = Field(default=None)