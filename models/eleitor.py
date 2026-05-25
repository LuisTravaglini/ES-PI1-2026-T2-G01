"""
Módulo responsável pelo gerenciamento de eleitores.

Este módulo contém funções para cadastro,
consulta e listagem de eleitores do sistema.
"""
from utils.criptografia import (
    criptografar,
    descriptografar
)

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
    cpf_criptografado = criptografar(cpf)

    cursor.execute(
        """
        SELECT nome_Completo
        FROM Eleitor
        WHERE CPF = %s
        """,
        (cpf_criptografado,)
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

    cpf_criptografado = criptografar(cpf)
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
    chave_criptografada = criptografar(chave_Acesso)
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
                cpf_criptografado,
                nome,
                titulo,
                chave_criptografada,
                tipo_Mesario,
                votou
            )
        )

        conexao.commit()

        print("Eleitor cadastrado com sucesso!")

    except Exception as erro:

        print("Erro ao cadastrar:", erro)

    input("\nPressione Enter para voltar...")


def editar_eleitor(cursor, conexao):
    """
    Permiti a edição do eleitor
    Busca o eleitor pelo cpf, e permiti inserir novos dados para esse eleitor

    Args:
        cursor (MySQLCursor): Cursor responsável pelas consultas SQL.
        conexao (MySQLConnection): Conexão ativa com o banco de dados.
    Returns:
        None: Esta função não possui retorno.
    """

    cpf = input("Digite o CPF do eleitor que deseja editar: ")
    cpf_critografado = criptografar(cpf)
    query_busca = """
    SELECT nome_Completo,
           titulo,
           chave_Acesso,
           tipo_mesario
    FROM eleitor
    WHERE CPF = %s
    """

    cursor.execute(query_busca, (cpf_critografado,))

    eleitor = cursor.fetchone()

    if not eleitor:

        print("\n❌ Eleitor não encontrado.")
        input("\nPressione Enter para voltar...")
        return

    chave_descriptografada = descriptografar(eleitor[2])
    
    print("\n=== DADOS ATUAIS ===")
    print(f"Nome: {eleitor[0]}")
    print(f"Título: {eleitor[1]}")
    print(f"Chave: {chave_descriptografada}")
    print(f"Mesário: {'Sim' if eleitor[3] else 'Não'}")

    print("\n=== NOVOS DADOS ===")

    novo_nome = input("Novo nome: ")
    novo_titulo = input("Novo título: ")
    nova_chave = input("Nova chave de acesso: ")

    nova_chave_criptografada = criptografar(nova_chave)

    tipo_mesario = input(
        "É mesário? (s/n): "
    ).lower()

    mesario_bool = tipo_mesario == "s"

    query_update = """
    UPDATE eleitor
    SET nome_Completo = %s,
        titulo = %s,
        chave_Acesso = %s,
        tipo_mesario = %s
    WHERE CPF = %s
    """

    cursor.execute(
        query_update,
        (
            novo_nome,
            novo_titulo,
            nova_chave_criptografada,
            mesario_bool,
            cpf_critografado
        )
    )

    conexao.commit()

    print("\n✅ Eleitor atualizado com sucesso!")

    input("\nPressione Enter para voltar...")





def remover_eleitor(cursor, conexao):
    """
    Permite a remoção de um eleitor pelo cpf

    Args:
        cursor (MySQLCursor): Cursor responsável pelas consultas SQL.
        conexao (MySQLConnection): Conexão ativa com o banco de dados.
    Returns:
        None: Esta função não possui retorno.
    """
    cpf = input(
        "Digite o CPF do eleitor que deseja remover: "
    )

    cpf_criptografado = criptografar(cpf)

    query_busca = """
    SELECT nome_Completo
    FROM eleitor
    WHERE CPF = %s
    """

    cursor.execute(query_busca, (cpf_criptografado,))

    eleitor = cursor.fetchone()

    if not eleitor:

        print("\n❌ Eleitor não encontrado.")
        input("\nPressione Enter para voltar...")
        return

    print("\n=== ELEITOR ENCONTRADO ===")
    print(f"Nome: {eleitor[0]}")

    confirmar = input(
        "\nDeseja realmente remover? (s/n): "
    ).lower()

    if confirmar == "s":

        query_delete = """
        DELETE FROM eleitor
        WHERE CPF = %s
        """

        cursor.execute(query_delete, (cpf_criptografado,))

        conexao.commit()

        print("\n✅ Eleitor removido com sucesso!")

    else:

        print("\n⚠️ Remoção cancelada.")

    input("\nPressione Enter para voltar...")