import os
import contas
import createDb as cdb
import psycopg2
import globals


def clear_terminal():
    # Check if the operating system is Windows ('nt')
    if os.name == 'nt':
        _ = os.system('cls')  # Use 'cls' for Windows
    else:
        _ = os.system('clear') # Use 'clear' for macOS/Linux

# Call the function to clear the terminal
def  Consultas_menu(conn: psycopg2.extensions.connection ):
    inp =  int(input( "selecione qual consulta deseja fazer"))
    Query_map =  globals.Query_map
    match inp:
        case 1:
            args = []
            clear_terminal()
            res = cdb.select_handler(conn, Query_map[inp], args)
            print(res)
        case 2:
            args = []
            clear_terminal()
            res = cdb.select_handler(conn, Query_map[inp], args)
            print(res)
        case 3:
            args = []
            clear_terminal()
            res = cdb.select_handler(conn, Query_map[inp], args)
            print(res)
        case 4:
            args = []
            clear_terminal()
            res = cdb.select_handler(conn, Query_map[inp], args)
            print(res)
        case 5:
            args = []
            clear_terminal()
            res = cdb.select_handler(conn, Query_map[inp], args)
            print(res)
        case 6:
            args = []
            clear_terminal()
            res = cdb.select_handler(conn, Query_map[inp], args)
            print(res)
        case 7:
            args = []
            clear_terminal()
            res = cdb.select_handler(conn, Query_map[inp], args)
            print(res)
        case 8:
            args = []
            clear_terminal()
            res = cdb.select_handler(conn, Query_map[inp], args)
            print(res)
        case 9:
            args = []
            clear_terminal()
            res = cdb.select_handler(conn, Query_map[inp], args)
            print(res)
        case 10:
            args = []
            clear_terminal()
            res = cdb.select_handler(conn, Query_map[inp], args)
            print(res)

def insertMenu(conn:psycopg2.extensions.connection):
    clear_terminal()
    inp =  int(input("selecione uma opção"))
    match inp:
        case 1: #grupo
            clear_terminal()
            print("criar publi")
        case 2:
            clear_terminal()
            print("criar grupo")
            pass


def login():
    email =  input("digite o email \n")
    senha =  input("digite a senha \n")
    contas.Gerenciamento_Contas().login(email, senha)

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
        return conta
    
    return None
    

def select_or_insert(conn):
    inp =  input("o que deseja fazer? \n 1.Consultar \n 2.Criar \n")
    match  inp:
        case '1': Consultas_menu(conn)
        case '2': insertMenu(conn)


def main():
   stop  = False
   conn =  globals.connect_db()
   while not stop:
    inp =  int(input("escolha um tipo \n 1.Log-in \n 2.Criar Conta\n-1.Stop \n"))
    match  inp:
        case 1:
            select_or_insert(conn)
        case 2:
            register(conn)
        case -1:
            stop = True

main()