import os
import contas
import createDb as cdb
import psycopg2
class conectar_banco:
    def __init__(self):
        self.conection = cdb.connect_db()
    def connect_db():
    # Connect to your postgres DB
        conn = psycopg2.connect("host=localhost dbname=Linkado user=aplicacao password=senha123")
        return conn

def clear_terminal():
    # Check if the operating system is Windows ('nt')
    if os.name == 'nt':
        _ = os.system('cls')  # Use 'cls' for Windows
    else:
        _ = os.system('clear') # Use 'clear' for macOS/Linux

# Call the function to clear the terminal

Query_map = {
    'nome_query1': '''Insira a query aqui'''
}

def login():
    email =  input("digite o email \n")
    senha =  input("digite a senha \n")
    contas.Gerenciamento_Contas().login(email, senha)

def register():
    nome  =  input("digite o nome\n")
    email =  input("digite o email \n")
    senha =  input("digite a senha \n")
    desc  = input("insira uma breve descricao sua \n")

    


def main():
   stop  = False
   while not stop:
    inp =  int(input("escolha um tipo \n 1.Log-in \n 2.Criar Conta\n-1.Stop \n"))
    match  inp:
        case 1:
            login()
        case 2:
            register()
        case -1:
            stop = True

main()