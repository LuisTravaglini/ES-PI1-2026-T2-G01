from database.conexao import get_conexao
from utils.ui import ler_opcao, limpar_menu
import models.candidato as candidato
import models.eleitor as eleitor
import models.votacao as votacao

conexao = get_conexao()
cursor = conexao.cursor()

if conexao.is_connected():
    print("Conexão bem sucedida")
else:
    print("Erro ao conectar")

votacao_aberta = False
opcao = 0

while opcao == 0:
    limpar_menu()
    print("\n=== URNA ELETRÔNICA ===")
    print("1 - Gerenciamento")
    print("2 - Votação")

    opcao = ler_opcao([1, 2])

    # ── GERENCIAMENTO ──────────────────────────────────
    while opcao == 1:
        limpar_menu()
        print("=== OPÇÕES DE GERENCIAMENTO ===")
        print("1 - Candidato")
        print("2 - Eleitor")
        print("3 - Voltar")

        gerenciamento = ler_opcao([1, 2, 3])

        if gerenciamento == 3:
            opcao = 0

        # -- Candidato --
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
                    opcao = 1

        # -- Eleitor --
        while gerenciamento == 2:
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
                            eleitor.buscar_por_titulo(cursor, titulo_input)

                case 2:
                    limpar_menu()
                    eleitor.cadastrar_eleitor(cursor, conexao)

                case 3:
                    gerenciamento = 0
                    opcao = 1

    # ── VOTAÇÃO ────────────────────────────────────────
    while opcao == 2:
        limpar_menu()
        print("=== SISTEMA DE VOTAÇÃO ===")
        print("1 - Abrir votação")
        print("2 - Encerrar votação")
        print("3 - Auditoria")
        print("4 - Resultado")
        print("5 - Voltar")

        opc = ler_opcao([1, 2, 3, 4, 5])

        match opc:
            case 1:
                limpar_menu()
                votacao_aberta = votacao.abrir_votacao(cursor, conexao, votacao_aberta)
            case 2:
                limpar_menu()
                votacao_aberta = votacao.encerrar_votacao(votacao_aberta)
            case 3:
                limpar_menu()
                votacao.auditoria(votacao_aberta)
            case 4:
                limpar_menu()
                votacao.resultado(cursor)
            case 5:
                opcao = 0
                break