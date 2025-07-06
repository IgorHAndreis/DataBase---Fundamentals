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

def register():
    nome  =  input("digite o nome\n")
    email =  input("digite o email \n")
    senha =  input("digite a senha \n")
    desc  = input("insira uma breve descricao sua \n")
    foto =  "link foto"

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
            register()
        case -1:
            stop = True

main()