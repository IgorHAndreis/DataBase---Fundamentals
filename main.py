import os
import contas
import createDb as cdb
import psycopg2
import globals
import pprint
import publicacoes

def clear_terminal():
    # Check if the operating system is Windows ('nt')
    if os.name == 'nt':
        _ = os.system('cls')  # Use 'cls' for Windows
    else:
        _ = os.system('clear') # Use 'clear' for macOS/Linux

# Call the function to clear the terminal
def  Consultas_menu(conn: psycopg2.extensions.connection, userData ):
    inp =  input("""
          1. O maior salário de cada setor
          2. Nome de empresas seguidas por suas conexões
          3. Listar perfis que preenchem uma vaga específica
          4. Listar pessoas que estudaram na universidade x e trabalham na empresa y
          5. listar perfis candidatos a vaga x, mas sem o certificado desejado
          6. listar instituições de ensino que formaram mais de x alunos no ano desejado
          e atualmente contém um título da tua escolha (exemplo: gerente)
          7. Listar as vagas que suas conexões se candidataram.
          8. Instituições de ensino com mais formandos contratados
          9. quantidade de curtidas e comentários feitas por cada integrante de um grupo.
          10. vagas  ou fechadas em uma empresa da sua escolha, com uma modalidade de sua escolha.
          selecione um:
            """)
    Query_map =  globals.Query_map
    clear_terminal()
    match inp:
        case '1':
            res = cdb.select_handler(conn, Query_map[inp])
        case '2':
            args = [str(userData.id), str(userData.id) ]
            res = cdb.select_handler(conn, Query_map[inp], args)
        case '3':
            vaga_id =  input("insira o id de uma vaga (exemplo, 1) \n")
            res = cdb.select_handler(conn, Query_map[inp], vaga_id)
        case '4':
            university =  input("digite o id de uma universidade: ")
            empresa =  input("digite o id de uma empresa: ")
            args = [university, empresa]
            clear_terminal()
            res = cdb.select_handler(conn, Query_map[inp], args)
        case '5':
            vaga_id =  input("insira o id de uma vaga (exemplo, 1):  \n")
            args = [vaga_id]
            clear_terminal()
            res = cdb.select_handler(conn, Query_map[inp], args)
        case '6':
            yr = input("insira um ano: \n")
            title =  input("insira título: \n")
            title = "%" + title + "%"
            counting =  input("quantos deseja saber?  \n")
            clear_terminal()
            args = [yr, title, counting]
            res = cdb.select_handler(conn, Query_map[inp], args)
        case '7':
            args = [userData.id, userData.id]
            res = cdb.select_handler(conn, Query_map[inp], args)
        case '8':
            args = []
            res = cdb.select_handler(conn, Query_map[inp], args)
        case '9':
            group_id = input("insira o id de um grupo válido: ")
            args = [group_id]
            clear_terminal()
            res = cdb.select_handler(conn, Query_map[inp], args)
        case '10':
            status =  input("insira um status (Aberta ou Fechada): ")
            empresa =  input("insira o id de uma empresa: ")
            modalidade =  input("insira uma modalidade (Híbrido, Remoto, ou Presencial): \n")
            args = [empresa, modalidade, status]
            clear_terminal()
            res = cdb.select_handler(conn, Query_map[inp], args)
        case _:
            select_or_insert(conn, userData)
    pprint.pprint(res)
    wait= False
    input("aperte qualquer coisa para sair")
    select_or_insert(conn, userData)
    
def criar_publicacao(conn,conta: contas.Conta, grupo_id: int = None):
    
    gerenciador = publicacoes.Gerenciamento_Publicacoes(conn)
    
    id_autor = conta.id
    texto = input("Texto da publicação (até 500 caracteres): ")
    anexo = input("Anexos (ou deixe vazio): ") or None
    grupo_id = grupo_id
    
    dados_publicacao = {
        "id_autor": id_autor,
        "texto": texto,
        "anexos": anexo,
        "id_grupo": grupo_id
    }
    
    publicacao =gerenciador.criar_publicacao(dados_publicacao)
    
    if publicacao:
        print("Publicação criada com sucesso!")
        print(f"ID da publicação: {publicacao.id}")
        return publicacao
    else:
        print("Erro ao criar publicação.")
        return None


def insertMenu(conn:psycopg2.extensions.connection, userData):
    clear_terminal()
    inp =  (input('''Selecione uma opção:
1. Criar publicacao
2. criar grupo'''))
    match inp:
        case 1: #grupo
            clear_terminal()
            print("criar publi")
        case 2:
            clear_terminal()
            print("criar grupo")
            pass
        case _: return


def login(conn):
    clear_terminal()
    email =  input("digite o email \n")
    senha =  input("digite a senha \n")
    conta =  contas.Gerenciamento_Contas(conn)
    res = conta.login(email, senha)
    select_or_insert(conn, res)

def register(conn):
    
    gerenciador = contas.Gerenciamento_Contas(conn)
    
    tipo_opcao = input("Tipo de conta: 1 - pessoal 2 - empresarial: ")
    
    if tipo_opcao == "1":
        tipo = "pessoal"
    elif tipo_opcao == "2":
        tipo = "empresarial"
    else:
        print("Opção inválida para tipo de conta!")
        return None
    
    data = {"tipo": tipo}
    
    data["name"] = input("Nome: ")
    data["email"] = input("Email: ")
    data["password"] = input("Senha: ")
    data["foto_perfil"] = input("Foto de perfil (ou deixe vazio): ") or None
    data["banner"] = input("Banner (ou deixe vazio): ") or None
    data["sobre"] = input("Sobre: ")
    
    if tipo == "pessoal":
        data["titulo"] = input("Título: ")

    elif tipo == "empresarial":
        
        data["nome_fantasia"] = input("Nome fantasia: ")
        data["localizacao"] = input("Localização: ")
        
        print("\nSetores disponíveis:")
        setores = gerenciador.listar_setores()

        for setor in setores:
            print(f"{setor[0]} - {setor[1]}")

        data["setor"] = int(input("Digite o ID do setor: "))
                
        data["cod_institucional"] = input("Código institucional: ") or None

    conta = gerenciador.criar_conta(data)
    
    if conta:
        print("Conta criada com sucesso!")
        print(conta)
        select_or_insert(conn, conta)
    
    return None
    

def select_or_insert(conn, userData):
    clear_terminal()
    inp =  input("o que deseja fazer? \n 1.Consultar \n 2.Criar \n")
    match  inp:
        case '1': Consultas_menu(conn, userData)
        case '2': insertMenu(conn, userData)


def main():
   stop  = False
   conn =  globals.connect_db()
   while not stop:
    inp =  input("escolha um tipo \n 1.Log-in \n 2.Criar Conta\n- Qualquer outro para sair \n")
    match  inp:
        case '1':
            login(conn)
        case '2':
            register(conn)
        case _:
            stop = True

main()