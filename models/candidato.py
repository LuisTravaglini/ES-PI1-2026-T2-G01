"""
Módulo responsável pelo gerenciamento de candidatos.

Este módulo contém funções relacionadas
à listagem de candidatos cadastrados
no sistema eleitoral.
"""


def listar_candidatos(cursor):
    """
    Lista todos os candidatos cadastrados no sistema.

    A função realiza uma consulta no banco de dados
    para exibir o nome completo e o número eleitoral
    de cada candidato.

    Args:
        cursor (MySQLCursor): Cursor responsável pelas consultas SQL.

    Returns:
        None: Esta função não possui retorno.
    """

    cursor.execute(
        """
        SELECT nome_Completo,
               numero_Candidato
        FROM candidato
        """
    )

    candidatos = cursor.fetchall()

    for c in candidatos:

        print(
            f"Candidato: {c[0]} "
            f"(Nº {c[1]})"
        )

    input("\nPressione Enter para voltar...")