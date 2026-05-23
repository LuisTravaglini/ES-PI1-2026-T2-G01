"""
Módulo responsável pelo gerenciamento de eleitores.

Este módulo contém funções para cadastro,
consulta e listagem de eleitores do sistema.
"""

from utils.validacoes import (
    validar_cpf,
    validar_titulo,
    gerar_chave
)


def listar_eleitores(cursor):
    """
    Lista todos os eleitores cadastrados no sistema.

    Args:
        cursor (MySQLCursor): Cursor responsável pelas consultas SQL.

    Returns:
        None: Esta função não possui retorno.
    """

    cursor.execute(
        "SELECT nome_Completo FROM Eleitor"
    )

    for i in cursor.fetchall():

        print(i[0])

    input("\nPressione Enter para voltar...")


def buscar_por_cpf(cursor, cpf):
    """
    Busca um eleitor utilizando o CPF informado.

    Args:
        cursor (MySQLCursor): Cursor responsável pelas consultas SQL.
        cpf (str): CPF do eleitor.

    Returns:
        None: Esta função não possui retorno.
    """

    cursor.execute(
        """
        SELECT nome_Completo
        FROM Eleitor
        WHERE CPF = %s
        """,
        (cpf,)
    )

    for i in cursor.fetchall():

        print(i[0])

    input("\nPressione Enter para voltar...")


def buscar_por_titulo(cursor, titulo):
    """
    Busca um eleitor utilizando o título eleitoral.

    Args:
        cursor (MySQLCursor): Cursor responsável pelas consultas SQL.
        titulo (str): Título eleitoral do eleitor.

    Returns:
        None: Esta função não possui retorno.
    """

    cursor.execute(
        """
        SELECT nome_Completo
        FROM Eleitor
        WHERE titulo = %s
        """,
        (titulo,)
    )

    for i in cursor.fetchall():

        print(i[0])

    input("\nPressione Enter para voltar...")


def cadastrar_eleitor(cursor, conexao):
    """
    Realiza o cadastro de um novo eleitor no sistema.

    A função valida CPF e título eleitoral,
    gera automaticamente uma chave de acesso
    e salva os dados no banco de dados.

    Args:
        cursor (MySQLCursor): Cursor responsável pelas consultas SQL.
        conexao (MySQLConnection): Conexão ativa com o banco de dados.

    Returns:
        None: Esta função não possui retorno.
    """

    print("=== Cadastro De Eleitor ===")

    cpf = input("Digite o CPF do eleitor: ")

    while not validar_cpf(cpf):

        print(
            "CPF inválido! "
            "Insira novamente um CPF válido "
            "para dar continuidade."
        )

        cpf = input("Digite o CPF do eleitor: ")

    titulo = input("Digite o título: ")

    while not validar_titulo(titulo):

        print(
            "Título inválido! "
            "Insira novamente um TÍTULO válido "
            "para dar continuidade."
        )

        titulo = input("Digite o título: ")

    nome = input("Digite o nome do eleitor: ")

    chave_Acesso = gerar_chave(nome)

    print(f"Sua chave de acesso é: {chave_Acesso}")

    resp = input("Mesário (s/n): ").strip().lower()

    if resp == 's':

        tipo_Mesario = 1

    else:

        tipo_Mesario = 0

    votou = 0

    try:

        cursor.execute(
            """
            INSERT INTO eleitor (
                CPF,
                nome_Completo,
                titulo,
                chave_Acesso,
                tipo_mesario,
                votou
            )
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (
                cpf,
                nome,
                titulo,
                chave_Acesso,
                tipo_Mesario,
                votou
            )
        )

        conexao.commit()

        print("Eleitor cadastrado com sucesso!")

    except Exception as erro:

        print("Erro ao cadastrar:", erro)

    input("\nPressione Enter para voltar...")