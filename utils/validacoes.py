import random

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


def validar_titulo(titulo: str) -> bool:
    numeros = "".join(ch for ch in titulo if ch.isdigit())
    return len(numeros) == 12 and numeros != numeros[0] * 12


def gerar_chave(nome: str) -> str:
    lista_nome = nome.split()
    primeiro = lista_nome[0]
    parte_nome = primeiro[:2].lower()

    sobrenome = lista_nome[1]
    parte_sobrenome = sobrenome[0].lower()

    numeros = ''.join(str(random.randint(0, 9)) for _ in range(4))

    return parte_nome + parte_sobrenome + numeros