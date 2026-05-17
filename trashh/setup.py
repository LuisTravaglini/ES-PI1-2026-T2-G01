#Conexão com o banco de dados e com o arquivo "functions"

import functions
from database.conexao import get_conexao


conexao = get_conexao()
cursor = conexao.cursor()
if conexao.is_connected():
    print("Conexão bem sucedida")
else:
    print("Erro")

#Menús

opcao = 0
while opcao == 0: 
    functions.limpar_menu()
    print("\n=== URNA ELETRÔNICA ===")
    print("1 - Gerenciamento")
    print("2 - Votação")

    opcao = functions.ler_opcao([1,2])

    while opcao == 1:
        #Menu gerenciamento
        functions.limpar_menu()
        print("=== OPÇÕES DE GERENCIAMENTO ===")
        print("1 - Candidato.")
        print("2 - Eleitor")
        print("3 - Voltar")
        
        
        gerenciamento = functions.ler_opcao([1,2,3])
        if gerenciamento == 3:
            opcao = 0
            
        while gerenciamento == 1:
            #menu candidato
            functions.limpar_menu()
            print("=== OPÇÕES DO CANDIDATO ===")
            print("1 - Listar Candidato")
            print("2 - voltar") 

            opc_candidato = functions.ler_opcao([1,2])

            match opc_candidato:
                case 1:
                    pass
                case 2: 
                    gerenciamento = 0
                    opcao = 1
        

        while gerenciamento == 2:
            #menu eleitor
            functions.limpar_menu()
            print("=== OPÇÕES DO ELEITOR ===")
            print("1 - Lista de eleitores")
            print("2 - Cadastro(Novo eleitor)")
            print("3 - voltar")
            
            eleitor = functions.ler_opcao([1,2,3])

            match eleitor:
                case 1:
                    functions.limpar_menu()
                    #menu lista de eleitores
                    print("1 - listar Eleitores")
                    print("2 - Buscar Eleitor por CPF ou Titulo")

                    lista_e = functions.ler_opcao([1,2])
                    match lista_e:
                        case 1:
                            #Listar
                            functions.limpar_menu()
                            cursor.execute("SELECT nome_Completo FROM Eleitor")
                            for i in cursor.fetchall():
                                print(i[0])

                        case 2:
                            #Buscar
                            functions.limpar_menu()
                            print("1- Buscar por CPF")
                            print("2- Buscar por Título")
                            
                            busca = functions.ler_opcao([1,2])
                            match busca:

                                case 1:
                                    functions.limpar_menu()
                                    query = "SELECT nome_Completo FROM Eleitor WHERE CPF = %s"
                                    CPF_input = input("Digite o CPF: ")
                                    cursor.execute(query,(CPF_input,))
                                    for i in cursor.fetchall():
                                        print(i[0])

                                case 2: 
                                    functions.limpar_menu()
                                    query = "SELECT nome_Completo FROM Eleitor WHERE titulo = %s"
                                    titulo_input = input("Digite o título de eleitor: ")
                                    cursor.execute(query,(titulo_input,))
                                    for i in cursor.fetchall():
                                        print(i[0])
            
                case 2:
                    functions.limpar_menu()
                    #menu Cadastro(eleitor)
                    
                    print("=== Cadastro De Eleitor ===")
                    cpf = input("Digite o CPF do eleitor: ")

                    #Chama a função que valida CPF
                    while not functions.validar_cpf(cpf):
                        functions.limpar_menu()
                        print("CPF inválido! Insira novamente um CPF válido para dar continuidade.")
                        cpf = input("Digite o CPF do eleitor: ")
                
                    #Chama a função que valida titulo
                   
                    titulo = input("Digite o título: ")

                    # Enquanto o título não for válido, pede novamente
            
                    while not functions.validar_titulo(titulo):
                        functions.limpar_menu()
                        print("Título INVÁLIDO! Insira novamente um TÍTULO válido para dar continuidade.")
                        titulo = input("Digite o título: ")

                    # Se chegou aqui, o título é válido
                    nome = input("Digite o nome do eleitor: ")
                    chave_Acesso = functions.gerar_chave(nome)
                    print(f"Sua chave de acesso é: {chave_Acesso}")

                    # Pergunta se é mesário (sim/não)
                    resp = input("Mesário (s/n): ").strip().lower()
                    tipo_Mesario = resp == "s"

                    
                    #Envia os inputs para o BD
                    try:
                        cursor.execute(
                            "INSERT INTO eleitor (CPF, nome_Completo, titulo, chave_Acesso, tipo_Mesario) VALUES (%s, %s, %s, %s, %s)",
                            (cpf, nome, titulo, chave_Acesso, tipo_Mesario)
                        )
                        conexao.commit()
                        print("Eleitor cadastrado com sucesso!")
                    except Exception as erro:
                        print("Erro ao cadastrar:", erro)

                case 3:
                    functions.limpar_menu()
                    #Voltar para menu eleitor
                    gerenciamento = 0
                    opcao = 1


    while opcao == 2:
        
        #Menu Votação

        functions.limpar_menu()

        votacao_aberta = False

        print("=== OPÇÕES DE VOTAÇÃO ===")
        print("1 - Sistema de votação")
        print("2 - Voltar")

        votacao = functions.ler_opcao([1,2])

        while votacao == 1:
           
            #Sistema de votação
            #functions.limpar_menu()
            print ("1 - Abertura Votação") 
            print ("2 - Encerramento Votação ")
            print ("3 - Auditoria")
            print ("4 - Resultado")
            print ("5 - voltar")

            sist_votacao = functions.ler_opcao([1,2,3,4,5])

            match sist_votacao:
                case 1:
                    if votacao_aberta:
                        with open ("arquivo.txt", "a", encoding="utf-8") as arquivo:
                            ocorrencia = arquivo.write ("\n\t ⚠️ Tentativa de abrir votação já aberta")
                        
                    else:
                        with open ("arquivo.txt", "a", encoding="utf-8") as arquivo:
                            ocorrencia = arquivo.write ("\n\t ✅ Votação ABERTA! Votos podem ser registrados")
                    
                    titulo = input("Digite seu titulo: ")
                    cpf = input("Digite os 4 primeiros dígitos do CPF: ")
                    chave = input("Digite sua chave de acesso: ")

                    query = """
                    SELECT tipo_mesario,
                        LEFT(CPF,4) AS primeiros_digitos
                    FROM eleitor
                    WHERE titulo = %s
                    AND LEFT(CPF,4) = %s
                    AND chave_Acesso = %s;
                    """

                    chave_Acesso = ""
                    cursor.execute(query, (titulo, cpf, chave_Acesso))

                    result = cursor.fetchone()  # pega uma linha do resultado

                    if result:
                        tipo_mesario = result[0]          # primeira coluna (tipo_mesario)
                        print("É mesario!")
                    else: 
                        print("Não possui permissão")
                        
                    conn = get_conexao()
                    functions.zerar_votos(conn)

                    print("\n=== Zerézima ===\n")
                    conn = get_conexao()
                    functions.mostrar_candidatos(conn)

                    conn.close()
                    
                    '''else:

                        id_eleitor = eleitor[0]

                        # verifica se já votou
                        query = """
                        SELECT *
                        FROM registro_Voto
                        WHERE id_eleitor = %s
                        """

                        cursor.execute(query, (id_eleitor,))

                        ja_votou = cursor.fetchone()

                        if ja_votou:
                            print("Esse eleitor já votou!")

                        else:

                            numero = int(input("Digite o número do candidato: "))

                            # verifica se candidato existe
                            query = """
                            SELECT *
                            FROM candidato
                            WHERE numero_Candidato = %s
                            """

                            cursor.execute(query, (numero,))

                            candidato = cursor.fetchone()

                            if candidato is None:
                                print("Candidato não encontrado!")

                            else:

                                # REGISTRA O VOTO
                                query = """
                                INSERT INTO registro_Voto
                                (numero_Candidato, id_eleitor)
                                VALUES (%s, %s)
                                """

                                cursor.execute(query, (numero, id_eleitor))

                                # SOMA +1 NO TOTAL DE VOTOS
                                query = """
                                UPDATE candidato
                                SET votos = votos + 1
                                WHERE numero_Candidato = %s
                                """

                                cursor.execute(query, (numero,))

                                conexao.commit()

                                print("Voto computado com sucesso!")'''
                        

                case 2: 
                    if not votacao_aberta:
                        with open ("arquivo.txt", "a", encoding="utf-8") as arquivo:
                            ocorrencia = arquivo.write ("\n\t ⚠️ Tentativa de encerrar votação ainda não aberta!")
                        
                    else:
                        with open ("arquivo.txt", "a", encoding="utf-8") as arquivo:
                            ocorrencia = arquivo.write ("\n\t 🔒 A votação foi ENCERRADA! Nenhum voto a mais será aceita!")
                        
                case 3:
                    if not votacao_aberta:
                        with open ("arquivo.txt", "a", encoding="utf-8") as arquivo:
                            ocorrencia = arquivo.write ("\n\t ⚠️Para adutitar, a votação precisa estar aberta!")
                        
                case 4:
                    #functions.limpar_menu()
                    ocorrencia = print("Resultado")

                case 5:
                    votacao = 0
                    opcao = 2
        opcao = 0
        votacao = 0
    

        