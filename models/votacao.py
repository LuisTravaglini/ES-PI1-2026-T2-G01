"""
Módulo responsável pelo gerenciamento da votação da urna eletrônica.

Este módulo controla a abertura e encerramento da votação,
registro de votos, auditoria, validação de integridade
e exibição de resultados da eleição.
"""

from datetime import datetime
import random
import string

from utils.cripto.chave import criptografar_chave
from utils.cripto.protocolo import criptografar_protocolo

LOG = "logs/auditoria.log"
LOG_1 = "logs/protocolo.log"


def _so_digitos(s: str) -> str:
    """Mantém apenas dígitos."""
    return "".join(ch for ch in str(s) if ch.isdigit())


def abrir_votacao(cursor, conexao, votacao_aberta: bool) -> bool:
    """
    Realiza a abertura oficial da votação.

    Solicita título, 4 primeiros dígitos do CPF e chave de acesso.
    Valida se é mesário e realiza a Zerézima (limpa votos e imprime total zerado).

    Args:
        cursor: Cursor do MySQL.
        conexao: Conexão MySQL.
        votacao_aberta (bool): Indica se a votação está aberta.

    Returns:
        bool: True se a votação foi aberta, False caso contrário.
    """

    if votacao_aberta:
        with open(LOG, "a", encoding="utf-8") as f:
            horario = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            f.write(f"\n[{horario}] ALERTA: Tentativa de abrir votação já aberta.\n")

    titulo = input("Digite seu titulo: ")
    cpf4 = input("Digite os 4 primeiros dígitos do CPF: ")
    chave = input("Digite sua chave de acesso: ")

    cpf4 = _so_digitos(cpf4)
    if len(cpf4) != 4:
        print("Dados inválidos (CPF precisa ter 4 dígitos).")
        input("\nPressione Enter para voltar...")
        return False

    chave_criptografada = criptografar_chave(chave)

    query = """
    SELECT tipo_mesario
    FROM eleitor
    WHERE titulo = %s
      AND cpf_prefixo4 = %s
      AND chave_Acesso = %s;
    """

    cursor.execute(query, (titulo, cpf4, chave_criptografada))
    result = cursor.fetchone()

    if not result:
        with open(LOG, "a", encoding="utf-8") as f:
            horario = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            f.write(f"\n[{horario}] ALERTA: Tentativa de acesso negado.\n")

        print("Dados inválidos.")
        input("\nPressione Enter para voltar...")
        return False

    tipo_mesario = result[0]
    if not tipo_mesario:
        with open(LOG, "a", encoding="utf-8") as f:
            horario = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            f.write(f"\n[{horario}] ALERTA: Tentativa de acesso negado (não é mesário).\n")

        print("Você não possui permissão de mesário.")
        input("\nPressione Enter para voltar...")
        return False

    # Zerézima
    zerar_votos(cursor, conexao)

    with open(LOG, "a", encoding="utf-8") as f:
        horario = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        f.write(f"\n[{horario}] ABERTURA: Votação iniciada com sucesso. Total de votos zerado.\n")

    input("\nPressione Enter para prosseguir...")
    return True


def encerrar_votacao(votacao_aberta: bool, cursor) -> bool:
    """
    Realiza o encerramento oficial da votação.

    Args:
        votacao_aberta (bool): Indica se a votação está aberta.
        cursor: Cursor do MySQL.

    Returns:
        bool: False se encerrou (urna fechada), True se continua aberta.
    """

    resp = input("Deseja realmente encerrar a votação?(sim/não): ").strip().lower()
    if resp != "sim":
        print("Encerramento cancelado.")
        return True

    if not votacao_aberta:
        print("Votação já está encerrada.")
        return False

    chave = input("Digite sua chave de acesso (confirmação): ")
    chave_criptografada = criptografar_chave(chave)

    query = """
    SELECT id_eleitor
    FROM eleitor
    WHERE chave_Acesso = %s AND tipo_mesario = 1;
    """
    cursor.execute(query, (chave_criptografada,))
    resultado = cursor.fetchone()

    if not resultado:
        print("Chave de acesso inválida.")
        input("\nPressione Enter para voltar...")
        return True

    with open(LOG, "a", encoding="utf-8") as f:
        horario = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        f.write(f"\n[{horario}] ENCERRAMENTO: Votação finalizada com sucesso.\n")

    print("Votação encerrada.")
    return False


def auditoria(votacao_aberta: bool):
    """
    Realiza a auditoria do sistema eleitoral (mensagem + leitura de logs, se existir).

    Args:
        votacao_aberta (bool): Indica se a votação está aberta.

    Returns:
        None
    """
    if not votacao_aberta:
        print("A votação precisa estar aberta para auditar.")
    input("\nPressione Enter para voltar...")


def resultado(cursor):
    """
    Exibe o resultado da eleição e os votos por partido.

    Args:
        cursor: Cursor do MySQL.

    Returns:
        None
    """
    cursor.execute("""
    SELECT candidato.nome_Completo,
           candidato.numero_Candidato,
           candidato.partido,
           COUNT(registro_voto.id) AS total_votos
    FROM candidato
    LEFT JOIN registro_voto
           ON candidato.numero_Candidato = registro_voto.numero_Candidato
    GROUP BY candidato.nome_Completo, candidato.numero_Candidato, candidato.partido
    ORDER BY total_votos DESC
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
    print("\nVENCEDOR DA ELEIÇÃO")
    print(f"Nome: {vencedor[0]}")
    print(f"Número: {vencedor[1]}")
    print(f"Partido: {vencedor[2]}")
    print(f"Votos: {vencedor[3]}")

    input("\nPressione Enter para voltar...")


def zerar_votos(cursor, conexao):
    """
    Zerézima: remove votos anteriores e imprime candidatos com 0 votos.

    Args:
        cursor: Cursor do MySQL.
        conexao: Conexão MySQL.

    Returns:
        None
    """

    # limpa votos
    cursor.execute("DELETE FROM registro_voto")
    conexao.commit()

    # imprime contagem zerada
    cursor.execute("""
        SELECT c.nome_Completo,
               COUNT(r.id) AS total_votos
        FROM candidato c
        LEFT JOIN registro_voto r
               ON c.numero_Candidato = r.numero_Candidato
        GROUP BY c.nome_Completo
        ORDER BY c.nome_Completo ASC
    """)

    candidatos = cursor.fetchall()

    print("\n=== ZERÉZIMA ===")
    for c in candidatos:
        print(f"{c[0]} - {c[1]} votos")
    print("=" * 40)


def chave_ordemalfa(linha: str) -> str:
    partes = linha.strip().split("-")
    if len(partes) >= 2:
        return partes[-1].lower()
    return linha.strip().lower()


def ordem_alfa_protocolo(protocolo: str):
    """
    Registra protocolo em arquivo e mantém o arquivo ordenado alfabeticamente.

    Args:
        protocolo (str): Protocolo em claro.

    Returns:
        None
    """
    with open(LOG_1, "a", encoding="utf-8") as f:
        horario = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        f.write(f"{horario} - {protocolo}\n")

    with open(LOG_1, "r", encoding="utf-8") as f:
        linhas = f.readlines()

    with open(LOG_1, "w", encoding="utf-8") as f:
        f.writelines(sorted(linhas, key=chave_ordemalfa))


def protocolo_votacao(numero_candidato: int) -> str:
    """
    Gera um protocolo único para o voto registrado.

    Padrão: "V" + 2 letras + "26" + número do candidato (2 dígitos) + 5 dígitos aleatórios.

    Args:
        numero_candidato (int): Número do candidato votado.

    Returns:
        str: Protocolo (12 caracteres).
    """
    letras_aleatorias = ''.join(random.sample(string.ascii_uppercase, k=2))
    numeros_aleatorios = ''.join(str(random.randint(0, 9)) for _ in range(5))
    return f"V{letras_aleatorias}26{int(numero_candidato):02d}{numeros_aleatorios}"


def realizar_voto(cursor, conexao, id_eleitor):
    """
    Registra o voto do eleitor no sistema.
    """

    confirmar = ""

    while confirmar != "s":

        print("=" * 30)
        print("SEU VOTO PARA PRESIDENTE")
        print("=" * 30)

        try:
            input_num_candidato = int(input("\nNúmero: "))
        except ValueError:
            print("❌ Número inválido.")
            continue

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

        # VOTO NULO
        if not nome_associado:

            print("=" * 30)
            print("⚠️ VOTO NULO")
            print("=" * 30)

            confirmar_nulo = input(
                "\nConfirmar voto nulo? (s/n): "
            ).lower()

            if confirmar_nulo != "s":
                print("\nRetornando para seleção do candidato...\n")
                continue

            protocolo = protocolo_votacao(0)

            ordem_alfa_protocolo(protocolo)

            protocolo_criptografado = (
                criptografar_protocolo(protocolo)
            )

            cursor.execute(
                """
                INSERT INTO registro_voto
                (
                    numero_Candidato,
                    protocolo
                )
                VALUES (%s, %s)
                """,
                (
                    None,
                    protocolo_criptografado
                )
            )

            cursor.execute(
                """
                UPDATE eleitor
                SET votou = TRUE
                WHERE id_eleitor = %s
                """,
                (id_eleitor,)
            )

            conexao.commit()

            print("\n✅ Voto nulo registrado!")
            print(
                f"\nPROTOCOLO DE VOTAÇÃO: "
                f"{protocolo}"
            )

            return True

        # CANDIDATO ENCONTRADO

        print("=" * 30)
        print(f"\nNome: {nome_associado[0]}")
        print(f"Partido: {nome_associado[1]}")
        print(f"Número: {nome_associado[2]}")

        confirmar = input(
            "\nConfirmar voto? (s/n): "
        ).lower()

        if confirmar != "s":

            print("\n⚠️ Voto não confirmado.")
            print(
                "Retornando para seleção "
                "do candidato...\n"
            )

    protocolo = protocolo_votacao(
        input_num_candidato
    )

    ordem_alfa_protocolo(protocolo)

    protocolo_criptografado = (
        criptografar_protocolo(protocolo)
    )

    cursor.execute(
        """
        INSERT INTO registro_voto
        (
            numero_Candidato,
            protocolo
        )
        VALUES (%s, %s)
        """,
        (
            input_num_candidato,
            protocolo_criptografado
        )
    )

    cursor.execute(
        """
        UPDATE eleitor
        SET votou = TRUE
        WHERE id_eleitor = %s
        """,
        (id_eleitor,)
    )

    conexao.commit()

    with open(LOG, "a", encoding="utf-8") as f:

        horario = datetime.now().strftime(
            '%Y-%m-%d %H:%M:%S'
        )

        f.write(
            f"\n[{horario}] "
            f"SUCESSO: Voto realizado com sucesso.\n"
        )

    print("\n✅ Voto registrado com sucesso!")
    print(
        f"\nPROTOCOLO DE VOTAÇÃO: "
        f"{protocolo}"
    )

    return True
    




def estatistica_comparecimento(cursor):
    """
    Exibe estatísticas de comparecimento dos eleitores.

    Args:
        cursor: Cursor do MySQL.

    Returns:
        None
    """

    cursor.execute("SELECT COUNT(*) FROM eleitor")
    total_eleitores = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM eleitor WHERE votou = TRUE")
    total_votaram = cursor.fetchone()[0]

    porcentagem = (total_votaram / total_eleitores * 100) if total_eleitores else 0

    print("=" * 40)
    print("ESTATÍSTICA DE COMPARECIMENTO")
    print("=" * 40)
    print(f"Total de eleitores aptos: {total_eleitores}")
    print(f"Total de comparecimento: {total_votaram}")
    print(f"Percentual de comparecimento: {porcentagem:.2f}%")
    input("\nPressione Enter para voltar...")


def validacao_integridade(cursor):
    """
    Valida a integridade dos votos registrados.

    Args:
        cursor: Cursor do MySQL.

    Returns:
        None
    """

    cursor.execute("SELECT COUNT(*) FROM registro_voto")
    total_votos = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM eleitor WHERE votou = TRUE")
    total_eleitores = cursor.fetchone()[0]

    print("=" * 40)
    print("VALIDAÇÃO DE INTEGRIDADE")
    print("=" * 40)
    print(f"Votos registrados na urna: {total_votos}")
    print(f"Eleitores com voto registrado: {total_eleitores}")

    if total_votos == total_eleitores:
        print("\n✅ INTEGRIDADE VALIDADA\nNenhuma inconsistência encontrada.")
    else:
        print("\n❌ ALERTA DE INCONSISTÊNCIA\nOs totais não coincidem.")

    input("\nPressione Enter para voltar...")