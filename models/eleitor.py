"""
Módulo responsável pelo gerenciamento de eleitores.

Este módulo contém funções para cadastro, consulta, edição, remoção
e listagem de eleitores do sistema.
"""

from utils.cripto.cpf import criptografar_cpf
from utils.cripto.chave import criptografar_chave, descriptografar_chave
from utils.cripto.protocolo import criptografar_protocolo, descriptografar_protocolo
from utils.validacoes import (
    validar_cpf,
    validar_titulo,
    gerar_chave
)


def _so_digitos(s: str) -> str:
    """
    Remove qualquer caractere que não seja dígito.

    Args:
        s (str): Texto de entrada.

    Returns:
        str: Apenas os dígitos contidos em s.
    """
    return "".join(ch for ch in str(s) if ch.isdigit())


def listar_eleitores(cursor) -> None:
    """
    Lista todos os eleitores cadastrados no sistema.

    Args:
        cursor: Cursor responsável pelas consultas SQL.

    Returns:
        None
    """
    cursor.execute("SELECT nome_Completo FROM Eleitor")
    for i in cursor.fetchall():
        print(i[0])
    input("\nPressione Enter para voltar...")


def buscar_por_cpf(cursor, cpf: str) -> None:
    """
    Busca um eleitor utilizando o CPF informado.

    Args:
        cursor: Cursor responsável pelas consultas SQL.
        cpf (str): CPF do eleitor (com ou sem máscara).

    Returns:
        None
    """
    cpf_criptografado = criptografar_cpf(cpf)
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


def buscar_por_titulo(cursor, titulo: str) -> None:
    """
    Busca um eleitor utilizando o título eleitoral informado.

    Args:
        cursor: Cursor responsável pelas consultas SQL.
        titulo (str): Título eleitoral do eleitor.

    Returns:
        None
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


def cadastrar_eleitor(cursor, conexao) -> None:
    """
    Realiza o cadastro de um novo eleitor no sistema.

    Fluxo:
    - Solicita CPF e valida matematicamente
    - Solicita título e valida matematicamente
    - Solicita nome completo
    - Gera chave de acesso automaticamente e exibe ao usuário
    - Pergunta se é mesário
    - Armazena CPF criptografado, chave criptografada e cpf_prefixo4 em claro

    Args:
        cursor: Cursor responsável pelas consultas SQL.
        conexao: Conexão ativa com o banco de dados.

    Returns:
        None
    """
    print("=== Cadastro De Eleitor ===")

    cpf = input("Digite o CPF do eleitor: ")
    while not validar_cpf(cpf):
        print("CPF inválido! Insira novamente um CPF válido para dar continuidade.")
        cpf = input("Digite o CPF do eleitor: ")

    cpf_digits = _so_digitos(cpf)
    cpf_prefixo4 = cpf_digits[:4]

    cpf_criptografado = criptografar_cpf(cpf_digits)

    titulo = input("Digite o título: ")
    while not validar_titulo(titulo):
        print("Título inválido! Insira novamente um TÍTULO válido para dar continuidade.")
        titulo = input("Digite o título: ")

    nome = input("Digite o nome do eleitor: ")

    chave_Acesso = gerar_chave(nome)
    chave_criptografada = criptografar_chave(chave_Acesso)
    print(f"Sua chave de acesso é: {chave_Acesso}")

    resp = input("Mesário (s/n): ").strip().lower()
    tipo_Mesario = 1 if resp == "s" else 0

    votou = 0

    try:
        cursor.execute(
            """
            INSERT INTO eleitor (
                CPF,
                cpf_prefixo4,
                nome_Completo,
                titulo,
                chave_Acesso,
                tipo_mesario,
                votou
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """,
            (
                cpf_criptografado,
                cpf_prefixo4,
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


def editar_eleitor(cursor, conexao) -> None:
    """
    Edita os dados de um eleitor identificado pelo CPF.

    Fluxo:
    - Solicita CPF
    - Localiza o eleitor pelo CPF criptografado
    - Exibe dados atuais (inclui descriptografia da chave)
    - Solicita novo nome e novo título
    - Gera uma nova chave automaticamente a partir do novo nome e salva criptografada
    - Atualiza os campos no banco

    Args:
        cursor: Cursor responsável pelas consultas SQL.
        conexao: Conexão ativa com o banco de dados.

    Returns:
        None
    """
    cpf = input("Digite o CPF do eleitor que deseja editar: ")
    cpf_critografado = criptografar_cpf(cpf)

    query_busca = """
    SELECT nome_Completo,
           titulo,
           chave_Acesso,
           tipo_mesario
    FROM eleitor
    WHERE CPF = %s
    """

    cursor.execute(query_busca, (cpf_critografado,))
    eleitor_encontrado = cursor.fetchone()

    if not eleitor_encontrado:
        print("\n❌ Eleitor não encontrado.")
        input("\nPressione Enter para voltar...")
        return

    chave_descriptografada = descriptografar_chave(eleitor_encontrado[2])

    print("\n=== DADOS ATUAIS ===")
    print(f"Nome: {eleitor_encontrado[0]}")
    print(f"Título: {eleitor_encontrado[1]}")
    print(f"Chave: {chave_descriptografada}")
    print(f"Mesário: {'Sim' if eleitor_encontrado[3] else 'Não'}")

    print("\n=== NOVOS DADOS ===")
    novo_nome = input("Novo nome: ")
    novo_titulo = input("Novo título: ")

    nova_chave = gerar_chave(novo_nome)
    print(f"\nNova chave: {nova_chave}")

    nova_chave_criptografada = criptografar_chave(nova_chave)

    tipo_mesario = input("É mesário? (s/n): ").lower()
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


def remover_eleitor(cursor, conexao) -> None:
    """
    Remove um eleitor do banco de dados, identificado pelo CPF.

    Args:
        cursor: Cursor responsável pelas consultas SQL.
        conexao: Conexão ativa com o banco de dados.

    Returns:
        None
    """
    cpf = input("Digite o CPF do eleitor que deseja remover: ")
    cpf_criptografado = criptografar_cpf(cpf)

    query_busca = """
    SELECT nome_Completo
    FROM eleitor
    WHERE CPF = %s
    """

    cursor.execute(query_busca, (cpf_criptografado,))
    eleitor_encontrado = cursor.fetchone()

    if not eleitor_encontrado:
        print("\n❌ Eleitor não encontrado.")
        input("\nPressione Enter para voltar...")
        return

    print("\n=== ELEITOR ENCONTRADO ===")
    print(f"Nome: {eleitor_encontrado[0]}")

    confirmar = input("\nDeseja realmente remover? (s/n): ").lower()

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