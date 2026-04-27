def validar_cpf(cpf: str) -> bool:
    numeros = ""
    for ch in cpf:
        if ch.isdigit():
            numeros += ch
    if len(numeros) != 11:
        return False
    if numeros == numeros[0] * 11:
        return False
    soma = 0
    for i in range(9):
        soma += int(numeros[i]) * (10 - i)
    digito1 = (soma * 10 % 11) % 10
    soma = 0
    for i in range(10):
        soma += int(numeros[i]) * (11 - i)
    digito2 = (soma * 10 % 11) % 10
    return digito1 == int(numeros[9]) and digito2 == int(numeros[10])
