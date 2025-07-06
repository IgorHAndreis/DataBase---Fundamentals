import os
import createDb as cdb
def clear_terminal():
    # Check if the operating system is Windows ('nt')
    if os.name == 'nt':
        _ = os.system('cls')  # Use 'cls' for Windows
    else:
        _ = os.system('clear') # Use 'clear' for macOS/Linux

# Call the function to clear the terminal

def searchMenu():
    print()

def insertMenu():
    print("xabilson")
stop  = False


def main():
   conn = cdb.connect_db()
   while not stop:
    inp =  int(input("escolha um tipo \n 1.Consultar \n 2.Inserir\n-1.Stop \n"))
    match  inp:
        case 1:
            searchMenu()
        case 2:
            insertMenu()
        case -1:
            stop = True

if __name__ == "main":
    main()