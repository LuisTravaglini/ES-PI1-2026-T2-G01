def validar_cpf(cpf: str) -> bool:
    """
    Valida se um CPF informado é válido.

    A função remove caracteres não numéricos,
    verifica o tamanho do CPF, impede sequências
    repetidas e calcula os dígitos verificadores.

    Args:
        cpf (str): CPF informado pelo usuário.

    Returns:
        bool: Retorna True caso o CPF seja válido
        ou False caso seja inválido.
    """

    # REMOVE CARACTERES NÃO NUMÉRICOS
    numeros = "".join(
        ch for ch in cpf if ch.isdigit()
    )

    # VERIFICA SE POSSUI 11 DÍGITOS
    if len(numeros) != 11:

        return False

    # VERIFICA SE TODOS OS NÚMEROS SÃO IGUAIS
    if numeros == numeros[0] * 11:

        return False

    # CÁLCULO DO PRIMEIRO DÍGITO VERIFICADOR
    soma = 0

    for i in range(9):

        soma += int(numeros[i]) * (10 - i)

    digito1 = (soma * 10 % 11) % 10

    # CÁLCULO DO SEGUNDO DÍGITO VERIFICADOR
    soma = 0

    for i in range(10):

        soma += int(numeros[i]) * (11 - i)

    digito2 = (soma * 10 % 11) % 10

    return (
        digito1 == int(numeros[9])
        and digito2 == int(numeros[10])
    )