
import random
import os

#Validação do CPF
def validar_cpf(cpf: str) -> bool:
    #Junta os digitos sem deixar espaços
    numeros = "".join(ch for ch in cpf if ch.isdigit())
    
    #Verifica se o CPF é diferente de 11 digítos, se sim, retorna FALSE
    if len(numeros) != 11:
        return False
    #Verifica se o CPF tem os 11 números iguais, se sim, retorna FALSE
    if numeros == numeros[0] * 11:
        return False
    #Conta para descobrir o primeiro dígito verificador
    soma = 0
    for i in range(9):
        soma += int(numeros[i]) * (10 - i)
    digito1 = (soma * 10 % 11) % 10

    #Conta para descobrir o segundo dígito verificador
    soma = 0
    for i in range(10):
        soma += int(numeros[i]) * (11 - i)
    digito2 = (soma * 10 % 11) % 10
    return digito1 == int(numeros[9]) and digito2 == int(numeros[10])



def val_cpf_parcial(cursor, cpf_parcial):

    query = """
    SELECT nome_Completo, CPF
    FROM eleitor
    WHERE CPF LIKE %s
    """

    cursor.execute(query, (cpf_parcial + "%",))

    return cursor.fetchall()


#validação do titulo do usuario.
def validar_titulo(titulo: str) -> bool:
    numeros = "".join(ch for ch in titulo if ch.isdigit())
    return len(numeros) == 12 and numeros != numeros[0] * 12



#validação da opção escolhida pelo usuario.
def ler_opcao(opcao_valida):

    entrada_valida = False


    while entrada_valida == False:

        #tentar converter input.
        try:
            opcao = int(input("Digite uma das opções: "))

            #verifica se é uma das opções validas.
            if opcao in opcao_valida:
                entrada_valida = True
                return opcao
            
            else:
                print("Opção inválida.")
        
        except ValueError:
            print("Digite apenas números.")



#função de gerar chave de acessoo
def gerar_chave(nome: str) -> str:
    
    # Pega as duas primeiras letras do nome
    lista_nome = nome.split()
    nome = lista_nome[0]
    parte_nome = nome[:2].lower()

    # Pega a primeira letra do sobrenome
    sobrenome = lista_nome[1]
    parte_sobrenome = sobrenome[0].lower()

    # Gera 4 números aleatórios
    numeros = ''.join(str(random.randint(0, 9)) for _ in range(4))
    
    # Monta a chave final
    chave = parte_nome + parte_sobrenome + numeros
    return chave

def limpar_menu():
    os.system('cls' if os.name == 'nt' else 'clear')


def zerar_votos(conn):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM registro_voto;")
    conn.commit()

def mostrar_candidatos(conn):
    cursor = conn.cursor()

    cursor.execute("""
    SELECT candidato.id_candidato,
           candidato.nome_Completo,
           candidato.numero_Candidato,
           COUNT(registro_voto.id) AS total_votos
    FROM candidato
    LEFT JOIN registro_voto
        ON candidato.numero_Candidato = registro_voto.numero_Candidato
    GROUP BY candidato.id_candidato,
             candidato.nome_Completo,
             candidato.numero_Candidato;
    """)

    candidatos = cursor.fetchall()

    for i in candidatos:
        print(f"Candidato: {i[1]} (Nº {i[2]}) | Votos: {i[3]}")