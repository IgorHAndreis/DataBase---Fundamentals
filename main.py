import os
import createDb as cdb
import psycopg2
<<<<<<< HEAD

=======
class conectar_banco:
    
    def __init__(self):
        self.conection = cdb.connect_db()
    def connect_db():
    # Connect to your postgres DB
        conn = psycopg2.connect("host=localhost dbname=Linkado user=aplicacao password=senha123")
        return conn
>>>>>>> e08725faedfaa7cd9eed45579142783ad9eab484

def clear_terminal():
    # Check if the operating system is Windows ('nt')
    if os.name == 'nt':
        _ = os.system('cls')  # Use 'cls' for Windows
    else:
        _ = os.system('clear') # Use 'clear' for macOS/Linux

# Call the function to clear the terminal

def login():
    clear_terminal()
    email =  input("digite o email \n")
    senha =  input("digite a senha \n")
    query =  "select * from contas where email = %s and senha = %s"
    conn =  cdb.connect_db()
    res =  cdb.select_handler(conn, query, [email, senha])
    print(res)

def register():
    print("xabilson")


def main():
   stop  = False
   conn = cdb.connect_db()
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