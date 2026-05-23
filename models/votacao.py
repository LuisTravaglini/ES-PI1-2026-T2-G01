"""
Módulo responsável pelo gerenciamento da votação da urna eletrônica.

Este módulo controla a abertura e encerramento da votação,
registro de votos, auditoria, validação de integridade
e exibição de resultados da eleição.
"""

LOG = "logs/auditoria.log"

import random
import string
from datetime import datetime


def abrir_votacao(cursor, conexao, votacao_aberta):
    """
    Realiza a abertura oficial da votação.

    A função valida se o usuário possui permissão de mesário
    antes de iniciar o processo eleitoral e zerar os votos.

    Args:
        cursor (MySQLCursor): Cursor responsável pelas consultas SQL.
        conexao (MySQLConnection): Conexão ativa com o banco de dados.
        votacao_aberta (bool): Indica se a votação já está aberta.

    Returns:
        bool: Retorna True caso a votação seja iniciada com sucesso,
        ou False caso a autenticação falhe.
    """

    if votacao_aberta:

        with open(LOG, "a", encoding="utf-8") as f:

            horario = datetime.now().strftime('%d/%m/%y %H:%M:%S')

            f.write(
                f"\n\t ⚠️ {horario} - ALERTA: "
                "Tentativa de abrir votação já aberta"
            )

    else:

        with open(LOG, "a", encoding="utf-8") as f:

            horario = datetime.now().strftime('%d/%m/%y %H:%M:%S')

            f.write(
                f"\n\t {horario} - ✅ ABERTURA: "
                "Votação iniciada com sucesso. "
                "Total de votos zerado"
            )

    titulo = input("Digite seu titulo: ")
    cpf = input("Digite os 4 primeiros dígitos do CPF: ")
    chave = input("Digite sua chave de acesso: ")

    query = """
    SELECT tipo_mesario
    FROM eleitor
    WHERE titulo = %s
    AND LEFT(CPF,4) = %s
    AND chave_Acesso = %s;
    """

    cursor.execute(query, (titulo, cpf, chave))

    result = cursor.fetchone()

    if result:

        tipo_mesario = result[0]

        if tipo_mesario:

            print("É mesário, iniciando votação...")

        else:

            with open(LOG, "a", encoding="utf-8") as f:

                horario = datetime.now().strftime('%d/%m/%y %H:%M:%S')

                f.write(
                    f"\n\t {horario} - ⚠️ ALERTA: "
                    "Tentativa de acesso negado"
                )

            print("Você não possui permissão de mesário.")

            input("\nPressione Enter para voltar...")

            return False

    else:

        print("Dados inválidos.")

        input("\nPressione Enter para voltar...")

        return False

    zerar_votos(cursor, conexao)

    print("\n=== Zerézima ===\n")

    input("\nPressione Enter para voltar...")

    return True


def encerrar_votacao(votacao_aberta, cursor):
    """
    Realiza o encerramento oficial da votação.

    Args:
        votacao_aberta (bool): Indica se a votação está aberta.
        cursor (MySQLCursor): Cursor responsável pelas consultas SQL.

    Returns:
        bool: Retorna False caso a votação seja encerrada
        ou True caso continue aberta.
    """

    resp = input("Deseja realmente encerrar a votação?(sim/não): ")

    if resp.lower() == "sim":

        if votacao_aberta:

            chave = input("Digite sua chave de acesso: ")

            query = """
            SELECT id_eleitor
            FROM eleitor
            WHERE chave_Acesso = %s;
            """

            cursor.execute(query, (chave,))

            resultado = cursor.fetchone()

            if resultado:

                print("=" * 30)
                print("Encerrando votação...")
                print("=" * 30)

                with open(LOG, "a", encoding="utf-8") as f:

                    horario = datetime.now().strftime('%d/%m/%y %H:%M:%S')

                    f.write(
                        f"\n\t {horario} -🔒 "
                        "A votação foi ENCERRADA!"
                    )

                print("Votação encerrada.")

                return False

            else:

                print("Chave de acesso inválida.")

                input("\nPressione Enter para voltar...")

                return True

    else:

        print("\nVocê não tem permissão para encerrar a votação.")

        return True


def auditoria(votacao_aberta):
    """
    Realiza a auditoria do sistema eleitoral.

    Args:
        votacao_aberta (bool): Indica se a votação está aberta.

    Returns:
        None: Esta função não possui retorno.
    """

    if not votacao_aberta:

        with open(LOG, "a", encoding="utf-8") as f:

            horario = datetime.now().strftime('%d/%m/%y %H:%M:%S')

            f.write(
                f"\n\t {horario} - ⚠️ ALERTA: "
                "Para auditar, a votação precisa estar aberta!"
            )

        print("A votação precisa estar aberta para auditar.")

    input("\nPressione Enter para voltar...")


def ordem_alfabetica(candidato):
    """
    Retorna o nome do candidato em letras minúsculas
    para auxiliar na ordenação alfabética.

    Args:
        candidato (tuple): Dados do candidato.

    Returns:
        str: Nome do candidato em letras minúsculas.
    """

    return candidato[0].lower()


def resultado(cursor):
    """
    Exibe o resultado da eleição e os votos por partido.

    Args:
        cursor (MySQLCursor): Cursor responsável pelas consultas SQL.

    Returns:
        None: Esta função não possui retorno.
    """

    cursor.execute("""
    SELECT nome_Completo,
           numero_Candidato,
           partido,
           votos
    FROM candidato
    ORDER BY votos DESC
    """)

    candidatos = cursor.fetchall()

    if not candidatos:

        print("Nenhum candidato encontrado.")

        input("\nPressione Enter para voltar...")

        return

    print("=" * 40)
    print("RESULTADO DA ELEIÇÃO")
    print("=" * 40)

    vencedor = candidatos[0]

    print("\n🏆 VENCEDOR DA ELEIÇÃO")
    print(f"Nome: {vencedor[0]}")
    print(f"Número: {vencedor[1]}")
    print(f"Partido: {vencedor[2]}")
    print(f"Votos: {vencedor[3]}")

    print("\n" + "=" * 40)

    opcao = input(
        "Deseja ver os demais candidatos? (s/n): "
    ).lower()

    if opcao == "s":

        print("\n📊 TODOS OS RESULTADOS\n")

        for candidato in sorted(
            candidatos,
            key=ordem_alfabetica
        ):

            print("=" * 30)
            print(f"Nome: {candidato[0]}")
            print(f"Número: {candidato[1]}")
            print(f"Partido: {candidato[2]}")
            print(f"Total de votos: {candidato[3]}")
            print("=" * 30)

    opc1 = input(
        "Deseja ver os votos por partido (s/n): "
    ).lower()

    if opc1 == "s":

        print("\n" + "=" * 40)
        print("VOTOS POR PARTIDO")
        print("=" * 40)

        query_partidos = """
        SELECT partido,
               SUM(votos) AS total_votos
        FROM candidato
        GROUP BY partido
        ORDER BY total_votos DESC
        """

        cursor.execute(query_partidos)

        partidos = cursor.fetchall()

        for partido in partidos:

            print("=" * 30)
            print(f"Partido: {partido[0]}")
            print(f"Total de votos: {partido[1]}")
            print("=" * 30)

    input("\nPressione Enter para voltar...")


def zerar_votos(cursor, conexao):
    """
    Reinicia todos os votos da eleição.

    A função remove registros de votos anteriores,
    zera os votos dos candidatos e redefine os eleitores
    como não votantes.

    Args:
        cursor (MySQLCursor): Cursor responsável pelas consultas SQL.
        conexao (MySQLConnection): Conexão ativa com o banco de dados.

    Returns:
        None: Esta função não possui retorno.
    """

    cursor.execute("DELETE FROM registro_voto;")

    cursor.execute("""
    UPDATE candidato
    SET votos = 0
    """)

    cursor.execute("""
    UPDATE eleitor
    SET votou = FALSE
    """)

    conexao.commit()

    print("\n=== ZERÉSIMA ===")
    print("Todos os candidatos iniciam com 0 votos.\n")

    cursor.execute("""
    SELECT nome_Completo,
           numero_Candidato,
           votos
    FROM candidato
    ORDER BY nome_Completo
    """)

    candidatos = cursor.fetchall()

    for candidato in candidatos:

        print("=" * 30)
        print(f"Nome: {candidato[0]}")
        print(f"Número: {candidato[1]}")
        print(f"Votos: {candidato[2]}")


def protocolo_votacao(numero_candidato):
    """
    Gera um protocolo único para o voto registrado.

    Args:
        numero_candidato (int): Número do candidato votado.

    Returns:
        str: Código único de protocolo da votação.
    """

    letras_aleatorias = ''.join(
        random.sample(string.ascii_uppercase, k=2)
    )

    numeros_aleatorios = ''.join(
        map(str, random.sample(range(1, 9), k=5))
    )

    return (
        f'V{letras_aleatorias}'
        f'26{str(numero_candidato)}'
        f'{numeros_aleatorios}'
    )


def realizar_voto(cursor, conexao, id_eleitor):
    """
    Registra o voto do eleitor no sistema.

    Args:
        cursor (MySQLCursor): Cursor responsável pelas consultas SQL.
        conexao (MySQLConnection): Conexão ativa com o banco de dados.
        id_eleitor (int): Identificador único do eleitor.

    Returns:
        None: Esta função não possui retorno.
    """

    print("=" * 30)
    print("SEU VOTO PARA PRESIDENTE")
    print("=" * 30)

    input_num_candidato = int(input("\nNúmero: "))

    cursor.execute(
        """
        SELECT nome_Completo,
               partido,
               numero_Candidato
        FROM candidato
        WHERE numero_Candidato = %s
        """,
        (input_num_candidato,)
    )

    nome_associado = cursor.fetchone()

    if nome_associado:

        print("=" * 30)

        print(f"\nNome: {nome_associado[0]}")
        print(f"Partido: {nome_associado[1]}")
        print(f"Número: {nome_associado[2]}")

        confirmar = input(
            "\nConfirmar voto? (s/n): "
        ).lower()

        if confirmar == "s":

            protocolo = protocolo_votacao(
                input_num_candidato
            )

            with open(
                'protocolo.log',
                "a",
                encoding="utf-8"
            ) as f:

                horario = datetime.now().strftime(
                    '%d/%m/%y %H:%M:%S'
                )

                f.write(
                    f"\n\t {horario} - {protocolo}"
                )

            query_voto = """
            INSERT INTO registro_voto(
                numero_Candidato,
                nome_Completo,
                protocolo
            )
            VALUES (%s, %s, %s)
            """

            cursor.execute(
                query_voto,
                (
                    input_num_candidato,
                    nome_associado[0],
                    protocolo
                )
            )

            query_update_candidato = """
            UPDATE candidato
            SET votos = COALESCE(votos, 0) + 1
            WHERE numero_Candidato = %s
            """

            cursor.execute(
                query_update_candidato,
                (input_num_candidato,)
            )

            query_update = """
            UPDATE eleitor
            SET votou = TRUE
            WHERE id_eleitor = %s
            """

            cursor.execute(
                query_update,
                (id_eleitor,)
            )

            conexao.commit()

            print("\n✅ Voto registrado com sucesso!")

            print(
                f"\nPROTOCOLO DE VOTAÇÃO: {protocolo}"
            )

        else:

            print("\n⚠️ Voto não confirmado.")

            print(
                "Retornando para seleção "
                "do candidato...\n"
            )

            realizar_voto(
                cursor,
                conexao,
                id_eleitor
            )

    else:

        print(
            "❌ Nenhum candidato associado "
            "ao número escolhido!"
        )

        print("Tente novamente.\n")

        realizar_voto(
            cursor,
            conexao,
            id_eleitor
        )


def estatistica_comparecimento(cursor):
    """
    Exibe estatísticas de comparecimento dos eleitores.

    Args:
        cursor (MySQLCursor): Cursor responsável pelas consultas SQL.

    Returns:
        None: Esta função não possui retorno.
    """

    query_total = """
    SELECT COUNT(*)
    FROM eleitor
    """

    cursor.execute(query_total)

    total_eleitores = cursor.fetchone()[0]

    query_votaram = """
    SELECT COUNT(*)
    FROM eleitor
    WHERE votou = TRUE
    """

    cursor.execute(query_votaram)

    total_votaram = cursor.fetchone()[0]

    porcentagem = (
        total_votaram / total_eleitores
    ) * 100

    print("=" * 40)
    print("ESTATÍSTICA DE COMPARECIMENTO")
    print("=" * 40)

    print(
        f"Total de eleitores aptos: "
        f"{total_eleitores}"
    )

    print(
        f"Total de comparecimento: "
        f"{total_votaram}"
    )

    print(
        f"Percentual de comparecimento: "
        f"{porcentagem:.2f}%"
    )

    input("\nPressione Enter para voltar...")


def validacao_integridade(cursor):
    """
    Valida a integridade dos votos registrados.

    A função compara o total de votos registrados
    com o total de eleitores marcados como votantes.

    Args:
        cursor (MySQLCursor): Cursor responsável pelas consultas SQL.

    Returns:
        None: Esta função não possui retorno.
    """

    query_votos = """
    SELECT COUNT(*)
    FROM registro_voto
    """

    cursor.execute(query_votos)

    total_votos = cursor.fetchone()[0]

    query_eleitores = """
    SELECT COUNT(*)
    FROM eleitor
    WHERE votou = TRUE
    """

    cursor.execute(query_eleitores)

    total_eleitores = cursor.fetchone()[0]

    print("=" * 40)
    print("VALIDAÇÃO DE INTEGRIDADE")
    print("=" * 40)

    print(
        f"Votos registrados na urna: "
        f"{total_votos}"
    )

    print(
        f"Eleitores com voto registrado: "
        f"{total_eleitores}"
    )

    print("\n" + "=" * 40)

    if total_votos == total_eleitores:

        print("✅ INTEGRIDADE VALIDADA")

        print(
            "Nenhuma inconsistência encontrada."
        )

    else:

        print("❌ ALERTA DE INCONSISTÊNCIA")

        print("Os totais não coincidem.")

    input("\nPressione Enter para voltar...")