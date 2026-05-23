"""
Sistema principal da Urna Eletrônica.

Este módulo é responsável pelo controle do menu principal,
gerenciamento de candidatos e eleitores, além do sistema
de votação da aplicação.
"""

from database.conexao import get_conexao
from utils.ui import ler_opcao, limpar_menu
import models.candidato as candidato
import models.eleitor as eleitor
import models.votacao as votacao
from datetime import datetime


def conectar_banco():
    """
    Realiza a conexão com o banco de dados do sistema.

    Returns:
        tuple: Retorna a conexão com o banco de dados e o cursor SQL.
    """

    conexao = get_conexao()
    cursor = conexao.cursor()

    if conexao.is_connected():
        print("Conexão bem sucedida")
    else:
        print("Erro ao conectar")

    return conexao, cursor


def autenticar_eleitor(cursor, titulo, cpf, chave):
    """
    Verifica se os dados informados pelo eleitor são válidos.

    Args:
        cursor (MySQLCursor): Cursor responsável pelas consultas SQL.
        titulo (str): Título de eleitor informado.
        cpf (str): Quatro primeiros dígitos do CPF.
        chave (str): Chave de acesso do eleitor.

    Returns:
        tuple | None: Retorna os dados do eleitor caso encontrados.
    """

    query = """
    SELECT id_eleitor, votou
    FROM eleitor
    WHERE titulo = %s
    AND LEFT(CPF,4) = %s
    AND chave_Acesso = %s;
    """

    cursor.execute(query, (titulo, cpf, chave))

    return cursor.fetchone()


def autenticar_mesario(cursor, titulo, cpf, chave):
    """
    Verifica se o usuário possui permissão de mesário.

    Args:
        cursor (MySQLCursor): Cursor responsável pelas consultas SQL.
        titulo (str): Título de eleitor informado.
        cpf (str): Quatro primeiros dígitos do CPF.
        chave (str): Chave de acesso do usuário.

    Returns:
        tuple | None: Retorna os dados do mesário caso encontrados.
    """

    query = """
    SELECT id_eleitor, votou, tipo_mesario
    FROM eleitor
    WHERE titulo = %s
    AND LEFT(CPF,4) = %s
    AND chave_Acesso = %s;
    """

    cursor.execute(query, (titulo, cpf, chave))

    return cursor.fetchone()


def registrar_tentativa_voto_duplo():
    """
    Registra no arquivo de auditoria uma tentativa de voto duplo.

    Returns:
        None: Esta função não possui retorno.
    """

    with open('auditoria.log', "a", encoding="utf-8") as f:
        horario = datetime.now().strftime('%d/%m/%y %H:%M:%S')

        f.write(
            f"\n\t {horario} - ⚠️ ALERTA: Tentativa de voto duplo"
        )


def menu_candidato(cursor):
    """
    Exibe o menu relacionado ao gerenciamento de candidatos.

    Args:
        cursor (MySQLCursor): Cursor responsável pelas consultas SQL.

    Returns:
        None: Esta função não possui retorno.
    """

    gerenciamento = 1

    while gerenciamento == 1:
        limpar_menu()

        print("=== OPÇÕES DO CANDIDATO ===")
        print("1 - Listar Candidatos")
        print("2 - Voltar")

        opc = ler_opcao([1, 2])

        match opc:
            case 1:
                limpar_menu()
                candidato.listar_candidatos(cursor)

            case 2:
                gerenciamento = 0


def menu_eleitor(cursor, conexao):
    """
    Exibe o menu relacionado ao gerenciamento de eleitores.

    Args:
        cursor (MySQLCursor): Cursor responsável pelas consultas SQL.
        conexao (MySQLConnection): Conexão ativa com o banco de dados.

    Returns:
        None: Esta função não possui retorno.
    """

    gerenciamento = 1

    while gerenciamento == 1:
        limpar_menu()

        print("=== OPÇÕES DO ELEITOR ===")
        print("1 - Lista de eleitores")
        print("2 - Cadastro (Novo eleitor)")
        print("3 - Voltar")

        opc = ler_opcao([1, 2, 3])

        match opc:

            case 1:
                limpar_menu()

                print("1 - Listar todos")
                print("2 - Buscar por CPF")
                print("3 - Buscar por Título")

                busca = ler_opcao([1, 2, 3])

                match busca:

                    case 1:
                        limpar_menu()
                        eleitor.listar_eleitores(cursor)

                    case 2:
                        limpar_menu()

                        cpf_input = input("Digite o CPF: ")

                        eleitor.buscar_por_cpf(cursor, cpf_input)

                    case 3:
                        limpar_menu()

                        titulo_input = input("Digite o título: ")

                        eleitor.buscar_por_titulo(
                            cursor,
                            titulo_input
                        )

            case 2:
                limpar_menu()

                eleitor.cadastrar_eleitor(
                    cursor,
                    conexao
                )

            case 3:
                gerenciamento = 0


def sistema_votacao(cursor, conexao):
    """
    Controla todas as funcionalidades do sistema de votação.

    Args:
        cursor (MySQLCursor): Cursor responsável pelas consultas SQL.
        conexao (MySQLConnection): Conexão ativa com o banco de dados.

    Returns:
        None: Esta função não possui retorno.
    """

    votacao_aberta = False

    while True:
        limpar_menu()

        print("=== SISTEMA DE VOTAÇÃO ===")
        print("1 - Abrir votação")
        print("2 - Auditoria da votação")
        print("3 - Resultado da votação")
        print("4 - Estatística de Comparecimento")
        print("5 - Validação de Integridade")
        print("6 - Voltar")

        opc = ler_opcao([1, 2, 3, 4, 5, 6])

        match opc:

            case 1:
                limpar_menu()

                votacao_aberta = votacao.abrir_votacao(
                    cursor,
                    conexao,
                    votacao_aberta
                )

                while votacao_aberta:
                    limpar_menu()

                    print("=== VOTAÇÃO ===")
                    print("1 - Votar")
                    print("2 - Encerrar Votação")

                    vot = ler_opcao([1, 2])

                    match vot:

                        case 1:
                            titulo = input("Digite seu titulo: ")
                            cpf = input(
                                "Digite os 4 primeiros dígitos do CPF: "
                            )
                            chave = input(
                                "Digite sua chave de acesso: "
                            )

                            result = autenticar_eleitor(
                                cursor,
                                titulo,
                                cpf,
                                chave
                            )

                            if result:

                                id_eleitor = result[0]
                                ja_votou = result[1]

                                if ja_votou:

                                    registrar_tentativa_voto_duplo()

                                    print(
                                        "❌ Você já votou nesta eleição."
                                    )

                                    input(
                                        "\nPressione Enter para voltar..."
                                    )

                                else:
                                    print("Apto a votar")

                                    votacao.realizar_voto(
                                        cursor,
                                        conexao,
                                        id_eleitor
                                    )

                                    input(
                                        "\nPressione Enter para voltar..."
                                    )

                            else:
                                print("❌ Dados inválidos.")

                                input(
                                    "\nPressione Enter para voltar..."
                                )

                        case 2:
                            limpar_menu()

                            titulo = input("Digite seu titulo: ")

                            cpf = input(
                                "Digite os 4 primeiros dígitos do CPF: "
                            )

                            chave = input(
                                "Digite sua chave de acesso: "
                            )

                            result = autenticar_mesario(
                                cursor,
                                titulo,
                                cpf,
                                chave
                            )

                            if result:

                                tipo_mesario = result[2]

                                if tipo_mesario == 1:

                                    votacao_aberta = (
                                        votacao.encerrar_votacao(
                                            votacao_aberta,
                                            cursor
                                        )
                                    )

                                    if not votacao_aberta:
                                        break

                            else:
                                print("Dados inválidos.")

                                input(
                                    "\nPressione Enter para voltar..."
                                )

            case 2:
                limpar_menu()
                votacao.auditoria(votacao_aberta)

            case 3:
                limpar_menu()
                votacao.resultado(cursor)

            case 4:
                limpar_menu()
                votacao.estatistica_comparecimento(cursor)

            case 5:
                limpar_menu()
                votacao.validacao_integridade(cursor)

            case 6:
                break


def menu_principal():
    """
    Exibe e controla o menu principal da aplicação.

    Returns:
        None: Esta função não possui retorno.
    """

    conexao, cursor = conectar_banco()

    opcao = 0

    while opcao == 0:
        limpar_menu()

        print("\n=== URNA ELETRÔNICA ===")
        print("1 - Gerenciamento")
        print("2 - Votação")

        opcao = ler_opcao([1, 2])

        while opcao == 1:
            limpar_menu()

            print("=== OPÇÕES DE GERENCIAMENTO ===")
            print("1 - Candidato")
            print("2 - Eleitor")
            print("3 - Voltar")

            gerenciamento = ler_opcao([1, 2, 3])

            match gerenciamento:

                case 1:
                    menu_candidato(cursor)

                case 2:
                    menu_eleitor(cursor, conexao)

                case 3:
                    opcao = 0

        while opcao == 2:
            sistema_votacao(cursor, conexao)
            opcao = 0
