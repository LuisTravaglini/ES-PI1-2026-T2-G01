import os

def limpar_menu():
    os.system('cls' if os.name == 'nt' else 'clear')

def ler_opcao(opcoes_validas):
    while True:
        try:
            opcao = int(input("Digite uma das opções: "))
            if opcao in opcoes_validas:
                return opcao
            else:
                print("Opção inválida.")
        except ValueError:
            print("Digite apenas números.")