"""
Módulo responsável pelas funções de interface do sistema.

Este módulo contém funções auxiliares para limpeza
da tela do terminal e leitura segura de opções
digitadas pelo usuário.
"""

import os


def limpar_menu():
    """
    Limpa o terminal do sistema operacional.

    A função identifica automaticamente o sistema
    operacional utilizado e executa o comando
    apropriado para limpar a tela.

    Returns:
        None: Esta função não possui retorno.
    """

    os.system('cls' if os.name == 'nt' else 'clear')


def ler_opcao(opcoes_validas):
    """
    Lê e valida a opção digitada pelo usuário.

    A função garante que apenas números presentes
    na lista de opções válidas sejam aceitos.

    Args:
        opcoes_validas (list): Lista contendo
        as opções permitidas no menu.

    Returns:
        int: Opção válida escolhida pelo usuário.
    """

    while True:

        try:

            opcao = int(input("Digite uma das opções: "))

            if opcao in opcoes_validas:

                return opcao

            else:

                print("Opção inválida.")

        except ValueError:

            print("Digite apenas números.")