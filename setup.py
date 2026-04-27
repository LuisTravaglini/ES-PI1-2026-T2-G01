import functions
from conexao import get_conexao

conexao = get_conexao()
cursor = conexao.cursor()

opcao = 0
while opcao == 0: 
    print("\n=== URNA ELETRÔNICA ===")
    print("1 - Gerenciamento")
    print("2 - Votação")

    opcao = int(input("Selecione uma opção: "))

while opcao == 1:
    print("=== OPÇÕES DE GERENCIAMENTO ===")
    print("1 - Candidato.")
    print("2 - Eleitor")
    print("3 - Voltar")

    gerenciamento = int(input("Selecione uma opção: "))
    if gerenciamento == 3:
        opcao = 0
        
    while gerenciamento == 1:

        print("=== OPÇÕES DO CANDIDATO ===")
        print("1 - Cadastrar Candidato")
        print("2 - Editar informações")
        print("3 - Excluir Candidato")
        print("4 - voltar") 

        opc_candidato = int(input("Selecione uma opção: "))

        match opc_candidato:
            case 1:
                print("=== Cadastro De candidato ===")
                cpf = input("Digite o CPF do candidato: ")
                if functions.validar_cpf(cpf):
                nome = input("Digite o nome do candidato: ")
                try:
                    cursor.execute("INSERT INTO candidatos (cpf, nome) VALUES (%s, %s)", (cpf, nome))
                    conexao.commit()
                    print("Candidato cadastrado com sucesso!")
                except Exception as e:
                    print("Erro ao cadastrar:", e)
                else:
                    print("CPF inválido.")
            case 2:
                print("...")
            case 3:
                print("...")
            case 4: 
                gerenciamento = 0
                opcao = 1
    

    while gerenciamento == 2:

        print("=== OPÇÕES DO ELEITOR ===")
        print("1 - lista de eleitores")
        print("2 - Cadastro(Novo eleitor)")
        print("3 - voltar")

        eleitor = int(input("Selecione uma opção: "))

        match eleitor:
            case 1:
                print("1 - Editar Eleitores")
                print("2 - Buscar Eleitor por CPF ou Titulo")
            case 2:
                Cpf = input("DIgite seu CPF: ")
            case 3:
                gerenciamento = 0
                opcao = 1


while opcao == 2:

    print("=== OPÇÕES DE VOTAÇÃO ===")
    print("1 - Listar candidatos")
    print("2 - Sistema de votação")
    print("3 - Voltar")

    votacao = int(input("Selecione uma opção: "))

    while votacao == 1:
        print ("Kaiky - 13")
        print ("Luis - 25")
        print ("Jõao - 17")
        votacao = 0
        opcao = 2

    while votacao == 2:
            
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