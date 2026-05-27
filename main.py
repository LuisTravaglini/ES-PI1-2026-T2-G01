"""
Sistema principal da Urna Eletrônica.

Este módulo é responsável pelo controle do menu principal,
gerenciamento de candidatos e eleitores, além do sistema
de votação da aplicação.
"""
from utils.cripto.cpf import criptografar_prefixo4_cpf
from utils.cripto.cpf import criptografar_cpf, descriptografar_cpf
from utils.cripto.acesso import criptografar_chave, descriptografar_chave
from utils.cripto.protocolo import criptografar_protocolo, descriptografar_protocolo

from database.conexao import get_conexao
from utils.ui import ler_opcao, limpar_menu
import models.candidato as candidato
import models.eleitor as eleitor
import models.votacao as votacao
from datetime import datetime

LOG = "logs/auditoria.log"

conexao = get_conexao()
cursor = conexao.cursor()

if conexao.is_connected():
    print("Conexão bem sucedida")
else:
    print("Erro ao conectar")




votacao_aberta = False
opcao = 0

# LOOP PRINCIPAL DO SISTEMA
while opcao == 0:
    limpar_menu()

    # MENU PRINCIPAL
    print("\n=== URNA ELETRÔNICA ===")
    print("1 - Gerenciamento")
    print("2 - Votação")

    opcao = ler_opcao([1, 2])

    # ── GERENCIAMENTO ──────────────────────────────────
    while opcao == 1:
        limpar_menu()

        # MENU DE GERENCIAMENTO
        print("=== OPÇÕES DE GERENCIAMENTO ===")
        print("1 - Candidato")
        print("2 - Eleitor")
        print("3 - Voltar")

        gerenciamento = ler_opcao([1, 2, 3])

        # RETORNA AO MENU PRINCIPAL
        if gerenciamento == 3:
            opcao = 0

        # -- Candidato --
        while gerenciamento == 1:
            limpar_menu()
            # MENU DE CANDIDATOS
            print("=== OPÇÕES DO CANDIDATO ===")
            print("1 - Listar Candidatos")
            print("2 - Voltar")

            opc = ler_opcao([1, 2])

            match opc:

                # LISTA TODOS OS CANDIDATOS
                case 1:
                    limpar_menu()
                    candidato.listar_candidatos(cursor)

                # RETORNA AO MENU ANTERIOR
                case 2:
                    gerenciamento = 0
                    opcao = 1

        # -- Eleitor --
        while gerenciamento == 2:
            limpar_menu()
            # MENU DE ELEITORES
            print("=== OPÇÕES DO ELEITOR ===")
            print("1 - Lista de eleitores")
            print("2 - Cadastro (Novo eleitor)")
            print("3 - Editar eleitor")
            print("4 - Remover eleitor")
            print("5 - Voltar")
            opc = ler_opcao([1, 2, 3, 4, 5])

            match opc:

                # MENU DE CONSULTAS DE ELEITORES
                case 1:
                    limpar_menu()
                    print("1 - Listar todos")
                    print("2 - Buscar por CPF")
                    print("3 - Buscar por Título")

                    busca = ler_opcao([1, 2, 3])

                    match busca:

                        # LISTA TODOS OS ELEITORES
                        case 1:
                            limpar_menu()
                            eleitor.listar_eleitores(cursor)

                        # BUSCA ELEITOR PELO CPF
                        case 2:
                            limpar_menu()
                            cpf_input = input("Digite o CPF: ")
                            eleitor.buscar_por_cpf(cursor, cpf_input)

                        # BUSCA ELEITOR PELO TÍTULO
                        case 3:
                            limpar_menu()
                            titulo_input = input("Digite o título: ")
                            eleitor.buscar_por_titulo(cursor, titulo_input)

                 # CADASTRA UM NOVO ELEITOR
                case 2:
                    limpar_menu()
                    eleitor.cadastrar_eleitor(cursor, conexao)
                
                case 3:
                    limpar_menu()
                    eleitor.editar_eleitor(cursor, conexao)

                case 4:
                    limpar_menu()
                    eleitor.remover_eleitor(cursor, conexao)

                case 5:
                    gerenciamento = 0
                    opcao = 1

    # - SISTEMA DE VOTAÇÃO 
    while opcao == 2:

        limpar_menu()

        # MENU DA VOTAÇÃO
        print("=== SISTEMA DE VOTAÇÃO ===")
        print("1 - Abrir votação")
        print("2 - Auditoria da votação")
        print("3 - Resultado da votação")
        print("4 - Estatística de Comparecimento")
        print("5 - Validação de Integridade")
        print("6 - Voltar")
        opc = ler_opcao([1, 2, 3, 4, 5, 6])

        match opc:

            # ABRE O SISTEMA DE VOTAÇÃO
            case 1:
                limpar_menu()
                votacao_aberta = votacao.abrir_votacao(cursor, conexao, votacao_aberta)

            # - VOTAÇÃO

                while votacao_aberta:
                    limpar_menu()
                    print("=== VOTAÇÃO ===")
                    print("1 - Votar")
                    print("2 - Encerrar Votação")

                    vot = ler_opcao([1, 2])

                    match vot:

                        # REGISTRO DE VOTO
                        case 1:

                            titulo = input("Digite seu titulo: ")
                            cpf = input("Digite os 4 primeiros dígitos do CPF: ")
                            chave = input("Digite sua chave de acesso: ")

                            cpf_criptografado4 = criptografar_prefixo4_cpf(cpf)
                            chave_criptografado = criptografar_chave(chave)

                            # CONSULTA DADOS DO ELEITOR
                            query = """
                            SELECT id_eleitor, votou
                            FROM eleitor
                            WHERE titulo = %s
                            AND LEFT(CPF,4) = %s
                            AND chave_Acesso = %s;
                            """
                            
                            cursor.execute(query, (titulo, cpf_criptografado4, chave_criptografado))
                            result = cursor.fetchone()

                            # VERIFICA SE O ELEITOR EXISTE
                            if result:

                                id_eleitor = result[0]
                                ja_votou = result[1]

                                # VERIFICA SE O ELEITOR JÁ VOTOU
                                if ja_votou:
                                    
                                    # REGISTRA TENTATIVA DE VOTO DUPLO
                                    if ja_votou == result[1]:
                                        with open(LOG, "a", encoding="utf-8") as f:
                                            horario = datetime.now().strftime('%y/%m/%d %H:%M:%S')
                                            f.write(f"\n\t {horario} - ALERTA: Tentativa de voto duplo")

                                    print("ALERTA: Tentativa de voto duplo.")
                                    input("\nPressione Enter para voltar...")

                                else:
                                    
                                    # REALIZA O VOTO
                                    votacao.realizar_voto(cursor, conexao, id_eleitor)
                                    print("SUCESSO: Voto realizado com sucesso.")
                                    input("\nPressione Enter para voltar...")

                            else:
                                print("ALERTA: Tentativa de acesso negado.(Dados inválidos)")
                                input("\nPressione Enter para voltar...")

                        # ENCERRAMENTO DA VOTAÇÃO
                        case 2:
                            limpar_menu()

                            titulo = input("Digite seu titulo: ")
                            cpf = input("Digite os 4 primeiros dígitos do CPF: ")
                            chave = input("Digite sua chave de acesso: ")
                            
                            cpf_criptografado4 = criptografar_prefixo4_cpf(cpf)
                            chave_criptografado = criptografar_chave(chave)

                            # CONSULTA DADOS DO MESÁRIO
                            query = """
                            SELECT id_eleitor, votou, tipo_mesario
                            FROM eleitor
                            WHERE titulo = %s
                            AND LEFT(CPF,4) = %s
                            AND chave_Acesso = %s;
                            """

                            cursor.execute(query, (titulo, cpf_criptografado4, chave_criptografado))
                            result = cursor.fetchone()

                            # VERIFICA SE O MESÁRIO EXISTE
                            if result:
                                
                                tipo_mesario = result[2]

                                # VERIFICA SE O USUÁRIO É MESÁRIO
                                if tipo_mesario == 1:
                                    votacao_aberta = votacao.encerrar_votacao(votacao_aberta, cursor)
                                    print("ENCERRAMENTO: Votação encerrada com sucesso.")

                                    # ENCERRA O LOOP DA VOTAÇÃO
                                    if not votacao_aberta:
                                        break
                                    
                            else:
                                print("ALERTA: Tentativa de acesso negado.(Dados inválidos)")
                                input("\nPressione Enter para voltar...")    
                                
            # AUDITORIA DA VOTAÇÃO  
            case 2:
                limpar_menu()
                votacao.auditoria(votacao_aberta)

            # RESULTADO DA ELEIÇÃO
            case 3:
                limpar_menu()
                votacao.resultado(cursor)
            # ESTATÍSTICAS DE COMPARECIMENTO
            case 4:
                limpar_menu()
                votacao.estatistica_comparecimento(cursor)

            # VALIDAÇÃO DE INTEGRIDADE
            case 5:
                limpar_menu()
                votacao.validacao_integridade(cursor)

            # RETORNA AO MENU PRINCIPAL
            case 6:
                opcao = 0
                break
 