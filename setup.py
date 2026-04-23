def menu():
    print("\n=== URNA ELETRÔNICA ===")
    print("1 - Gerenciamento")
    print("2 - Votação")

while True:
    menu()
    opcao = input("Escolha uma opção: ")

    match opcao:
        case "1":
            print("=== OPÇÕES DE GERENCIAMENTO ===")
            print("1 - Candidato.")
            print("2 - Eleitor")

            gerenciamento = input("Sua opção de gerenciamento : ")

            match gerenciamento:
                case "1":
                    print("=== OPÇÕES DO CANDIDATO ===")
                    print("1 - Cadastrar Candidato")
                    print("2 - Editar informações")
                    print("3 - Excluir Candidato")
                    print("4 - voltar") 

                    candidato = input("Selecione uma opção: ")

                    match candidato:
                        case 1:
                            print("")
                        case 2:
                            print("")
                        case 3:
                            print("")
                        case 4: 
                            menu()

                case "2":
                    print("=== OPÇÕES DO ELEITOR ===")
                    print("1 - lista de eleitores")
                    print("2 - Cadastro(Novo eleitor)")
                    print("3 - voltar")

                    eleitor = input("Selecione uma opção: ")

                    match eleitor:
                        case "1":
                            print("1 - Editar Eleitores")
                            print("2 - Buscar Eleitor por CPF ou Titulo")
                        case "2":
                            Cpf = input("DIgite seu CPF: ")




        case "2":
            print("1 - Listar candidatos")
            print("2 - Buscar Candidatos")
            print("3 - Sistema de votação")

            votacao = input("Selecione uma opção: ")
            match votacao:
                case "1": 
                    pass
                    #lista de candidatos (?)
                case "2": 
                    pass
                    #Pesquisa de candidatos (?)
                case "3":
                    pass
                    

        case "3":
            print("Encerrando...")
            break

        case _:
            print("opção inválida!")