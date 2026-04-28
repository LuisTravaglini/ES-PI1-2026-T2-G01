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






#Validar título de eleitor
def validar_titulo(titulo: str) -> bool:
    #Junta os digitos sem deixar espaços 
    numeros = "".join(ch for ch in titulo if ch.isdigit())

    # Verifica se tem 12 dígitos
    if len(numeros) != 12:
        return False

    # Evita títulos com todos os dígitos iguais
    if numeros == numeros[0] * 12:
        return False

    # Calcula dígitos verificadores
    soma1 = 0
    for i in range(8):
        soma1 += int(numeros[i]) * (9 - i)
    digito1 = (soma1 % 11) % 10

    soma2 = 0
    for i in range(9):
        soma2 += int(numeros[i]) * (10 - i)
    digito2 = (soma2 % 11) % 10

    # Confere se os dígitos calculados batem com os informados
    return digito1 == int(numeros[10]) and digito2 == int(numeros[11])