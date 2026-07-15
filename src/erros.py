import os
from sqlmodel import select, Session, Optional
from src.models import *
from src.banco_dados import iniciar_banco_dados

def ler_rotas_erradas(caminho_arquivo: str) -> list[str]:
    """Lê o arquivo TXT e retorna uma lista de nomes de rotas."""
    if not os.path.exists(caminho_arquivo):
        print(f"Erro: Arquivo '{caminho_arquivo}' não encontrado.")
        return []
    
    with open(caminho_arquivo, 'r', encoding='utf-8') as f:
        # Remove espaços e linhas vazias
        rotas = [line.strip() for line in f.readlines() if line.strip()]
    
    return rotas

def obter_bairros_existentes(engine: Engine) -> list[Bairros]: #type: ignore
    """Retorna todos os bairros do banco para exibição."""
    with Session(engine) as session:
        bairros = session.exec(select(Bairros)).all() 
        return bairros

def selecionar_bairro_usuario(bairros: list[Bairros]) -> Optional[Bairros]:
    """Interface para o usuário selecionar um bairro pelo ID."""
    if not bairros:
        print("Nenhum bairro encontrado no banco.")
        return None

    print("\n--- Seleção de Bairro ---")
    for bairro in bairros:
        print(f"[ID: {bairro.id}] {bairro.nome}")
    
    while True:
        try:
            escolha_id = input("Digite o ID do bairro desejado: ").strip()
            id_selecionado = int(escolha_id)
            
            # Busca o objeto bairro correspondente ao ID
            bairro_selecionado = next((b for b in bairros if b.id == id_selecionado), None)
            
            if bairro_selecionado:
                return bairro_selecionado
            else:
                print("ID inválido. Tente novamente.")
        except ValueError:
            print("Por favor, insira um número inteiro válido.")


def salvar_rotas_erradas(engine: Engine) -> None: #type: ignore
    """
    Lê as rotas do arquivo, associa ao bairro selecionado pelo usuário
    e salva no banco de dados.
    """
    # 1. Ler as rotas do arquivo
    caminho_arquivo = "rotas_erradas.txt"
    nomes_rotas = ler_rotas_erradas(caminho_arquivo)

    if not nomes_rotas:
        print("Nenhuma rota para processar.")
        return

    # 2. Obter bairros e selecionar um
    bairros = obter_bairros_existentes(engine)
    bairro_escolhido = selecionar_bairro_usuario(bairros)

    if not bairro_escolhido:
        print("Operação cancelada: Nenhum bairro válido selecionado.")
        return

    # 3. Preparar os novos registros de Rotas
    # Criamos uma lista de objetos Rotas para o session.add_all
    novas_rotas_objetos = []
    for nome_rota in nomes_rotas:
        nova_rota = Rotas(
            nome=nome_rota,
            id_bairros=bairro_escolhido.id
        )
        novas_rotas_objetos.append(nova_rota)

    with Session(engine) as session:
        try:
            session.add_all(novas_rotas_objetos)
            session.commit()
            print(f"\nSucesso! {len(novas_rotas_objetos)} rotas associadas ao bairro '{bairro_escolhido.nome}' foram salvas.")
        except Exception as e:
            session.rollback()
            print(f"Erro ao salvar rotas: {e}")

if __name__ == "__main__":
    engine_db = iniciar_banco_dados()
    
    salvar_rotas_erradas(engine_db)
