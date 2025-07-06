import psycopg2
from datetime import datetime

class Publicacao:

    def __init__(self, id: int, id_autor: int, texto_conteudo: str, anexo: str = None):
        self.id = id
        self.id_autor = id_autor
        self.texto_conteudo = texto_conteudo
        self.anexo = anexo
        self.data_hora = datetime.now()

    def set_db_generated_attrs(self, novo_id: int):
        self.id = novo_id

    def to_dict(self) -> dict:
        return {
            'id': str(self.id),
            'idAutor': str(self.id_autor),
            'texto': self.texto_conteudo,
            'anexo': self.anexo,
            'dataHora': self.data_hora
        }

class Gerenciamento_Publicacoes:
    
    def __init__(self, conexao):
        
        self.conexao = conexao

    def criar_publicacao(self, data: dict):

        nova_publicacao = self.gerar_publicacao(data)

        if nova_publicacao is None:
            print("Falha ao gerar o objeto da publicação. Verifique os dados de entrada.")
            return None

        try:
            self.insert_publicacao_banco(nova_publicacao)
            self.conexao.commit()
            print(f"Publicação do autor ID {nova_publicacao.id_autor} criada com sucesso.")
            return nova_publicacao
        except (Exception, psycopg2.DatabaseError) as e:
            self.conexao.rollback()
            print(f"Falha ao inserir publicação no banco de dados: {e}")
            return None

    def insert_publicacao_banco(self, publicacao: Publicacao):
        
        pass

    def gerar_publicacao(self, data: dict) -> Publicacao:
    
        try:
            nova_publicacao = Publicacao(
                id=0,  
                id_autor=data['id_autor'],
                texto_conteudo=data['texto_conteudo'],
                anexo=data.get('anexo')
            )
            return nova_publicacao
        except KeyError as e:
            print(f"Campo obrigatório ausente nos dados da publicação: {e}")
            return None
