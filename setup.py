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
                if functions.validar_cpf(cpf):
                    titulo = input("Digite o título: ")
                    #Chama a função que valida titulo
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
                    cursor.execute("INSERT INTO eleitor (CPF, nome_Completo, titulo, chave_Acesso, tipo_Mesario) VALUES (%s, %s)", (cpf, nome, titulo, chave_Acesso, tipo_Mesario))
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
    print("=== OPÇÕES DE VOTAÇÃO ===")
    print("1 - Listar candidatos")
    print("2 - Sistema de votação")
    print("3 - Voltar")

    votacao = int(input("Selecione uma opção: "))

    while votacao == 1:
        #Lista de candidatos
        print ("Kaiky - 13")
        print ("Luis - 25")
        print ("Jõao - 17")
        votacao = 0
        opcao = 2

    while votacao == 2:
        #Sistema de votação
        print ("1 - Iniciar Votação") 
        print ("2 - Auditoria")
        print ("3 - Resultado")

        sist_votacao = int(input("Selecione uma opção: "))

        match sist_votacao:
            case 1:
                print ("Iniciando Votação...")
            case 2: 
                print ("Iniciando Auditoria...")
            case 3:
                print ("Resultados...")
            case 4:
                votacao = 0
                opcao = 2