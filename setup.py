#Conexão com o banco de dados e com o arquivo "functions"

import functions
from conexao import get_conexao

conexao = get_conexao()
cursor = conexao.cursor()
if conexao.is_connected():
    print("Conexão bem sucedida")
else:
    print("Erro")

#Menús

opcao = 0
while opcao == 0: 
    print("\n=== URNA ELETRÔNICA ===")
    print("1 - Gerenciamento")
    print("2 - Votação")

    opcao = int(input("Selecione uma opção: "))

    while opcao == 1:
        #Menu gerenciamento
        print("=== OPÇÕES DE GERENCIAMENTO ===")
        print("1 - Candidato.")
        print("2 - Eleitor")
        print("3 - Voltar")

        gerenciamento = int(input("Selecione uma opção: "))
        if gerenciamento == 3:
            opcao = 0
            
        while gerenciamento == 1:
            #menu candidato
            print("=== OPÇÕES DO CANDIDATO ===")
            print("1 - Listar Candidato")
            print("2 - voltar") 

            opc_candidato = int(input("Selecione uma opção: "))
            match opc_candidato:
                case 1:
                    pass
                case 2: 
                    gerenciamento = 0
                    opcao = 1
        

        while gerenciamento == 2:
            #menu eleitor
            print("=== OPÇÕES DO ELEITOR ===")
            print("1 - Lista de eleitores")
            print("2 - Cadastro(Novo eleitor)")
            print("3 - voltar")

            eleitor = int(input("Selecione uma opção: "))

            match eleitor:
                case 1:
                    #menu lista de eleitores
                    print("1 - listar Eleitores")
                    print("2 - Buscar Eleitor por CPF ou Titulo")

                    lista_e = int(input("Selecione uma opção: "))
                    match lista_e:
                        case 1:
                            #Listar
                            cursor.execute("SELECT nome_Completo FROM Eleitor")
                            for i in cursor.fetchall():
                                print(i[0])

                        case 2:
                            #Buscar
                            print("1- Buscar por CPF")
                            print("2- Buscar por Título")
                            busca = int(input("Selelcione uma opção: "))
                            match busca:

                                case 1:
                                    query = "SELECT nome_Completo FROM Eleitor WHERE CPF = %s"
                                    CPF_input = input("Digite o CPF: ")
                                    cursor.execute(query,(CPF_input,))
                                    for i in cursor.fetchall():
                                        print(i[0])

                                case 2: 
                                    query = "SELECT nome_Completo FROM Eleitor WHERE titulo = %s"
                                    titulo_input = input("Digite o título de eleitor: ")
                                    cursor.execute(query,(titulo_input,))
                                    for i in cursor.fetchall():
                                        print(i[0])
            
                case 2:

                    #menu Cadastro(eleitor)
                    
                    print("=== Cadastro De Eleitor ===")
                    cpf = input("Digite o CPF do eleitor: ")

                    #Chama a função que valida CPF
                    while not functions.validar_cpf(cpf):
                        print("CPF inválido! Insira novamente um CPF válido para dar continuidade.")
                        cpf = input("Digite o CPF do eleitor: ")

                    titulo = input("Digite o título: ")

                    #Chama a função que valida titulo
                    while not functions.validar_titulo(titulo):
                        print("Titulo INVÁLIDO! Insira novamente um TÍTULO válido para dar continuidade.")
                        titulo = input("Digite o título: ")

                        if functions.validar_titulo(titulo):
                            nome = input("Digite o nome do eleitor: ")
                            chave_Acesso = input("Digite a chave de acesso: ")
                            tipo_Mesario = bool(input("Mesário: "))
                        else:
                            print("Título Inválido")
                    else:
                        print("CPF inválido.")

                    #Envia os inputs para o BD
                    try:
                        cursor.execute("INSERT INTO eleitor (CPF, nome_Completo, titulo, chave_Acesso, tipo_Mesario) VALUES (%s, %s, %s, %s, %s)", (cpf, nome, titulo, chave_Acesso, tipo_Mesario))
                        conexao.commit()
                        print("Candidato cadastrado com sucesso!")
                    except Exception as erro:
                        print("Erro ao cadastrar:", erro)
                    
                case 3:
                    #Voltar para menu eleitor
                    gerenciamento = 0
                    opcao = 1


    while opcao == 2:
        
        #Menu Votação

        votacao_aberta = False
        auditoria = []

        print("=== OPÇÕES DE VOTAÇÃO ===")
        print("1 - Sistema de votação")
        print("2 - Voltar")

        votacao = int(input("Selecione uma opção: "))

        while votacao == 1:
            #Sistema de votação
            print ("1 - Abertura Votação") 
            print ("2 - Encerramento Votação ")
            print ("3 - Auditoria")
            print ("4 - Resultado")
            print ("5 - voltar")

            sist_votacao = int(input("Selecione uma opção: "))

            match sist_votacao:
                case 1:
                    if votacao_aberta:
                        ocorrencia = print("⚠️ Tentativa de abrir votação já aberta")
                        auditoria.append(ocorrencia)
                    else:
                        ocorrencia = print (" ✅ Votação ABERTA! Votos podem ser registrados")
                        auditoria.append(ocorrencia)
                case 2: 
                    if not votacao_aberta:
                        ocorrencia = print(" ⚠️ Tentativa de encerrar votação ainda não aberta!")
                        auditoria.append(ocorrencia)
                    else:
                        ocorrencia = print ("🔒 A votação foi ENCERRADA! Nnehum voto a mais será aceita!")
                        auditoria.append(ocorrencia)
                case 3:
                    if not votacao_aberta:
                        ocorrencia = print ("Para adutitar, a votação precisa estar aberta!")
                        auditoria.append(ocorrencia)
                    else: 
                        print("\n=== AUDITORIA - OCORRÊNCIAS ===")
                        if not auditoria:
                            print("Nenhuma ocorrência registrada.")
                        else:
                            for i, ocorrencia in enumerate(auditoria, start=1):
                                print(f"{i}. {ocorrencia}")
                            print("\n=="*30)
                case 4:
                    ocorrencia = print("Resultado")
                    auditoria.append(ocorrencia)

                case 5:
                    votacao = 0
                    opcao = 2

        