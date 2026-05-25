"""
Módulo responsável pelas validações do sistema.

Este módulo contém funções para validação
de CPF, título eleitoral e geração de
chaves de acesso dos eleitores.
"""

import random


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


def validar_titulo(titulo: str) -> bool:
    """
    Valida se um título eleitoral é válido.

    A função verifica se o título possui
    exatamente 12 dígitos e se não é composto
    apenas por números repetidos.

    Args:
        titulo (str): Título eleitoral informado.

    Returns:
        bool: Retorna True caso o título seja válido
        ou False caso seja inválido.
    """
    # REMOVE QUALQUER COISA QUE NÃO FOR NÚMERO
    numeros = "".join(
        ch for ch in titulo if ch.isdigit()
    )

    # PRECISA TER 12 DÍGITOS
    if len(numeros) != 12:
        return False

    # NÃO PODE SER REPETIDO
    if numeros == numeros[0] * 12:
        return False

    # PARTES DO TÍTULO
    sequencial = numeros[:8]
    uf = numeros[8:10]

    dv1_informado = int(numeros[10])
    dv2_informado = int(numeros[11])

    # -------------------------
    # CÁLCULO DO PRIMEIRO DV
    # -------------------------

    soma1 = 0

    multiplicadores1 = [2, 3, 4, 5, 6, 7, 8, 9]

    for i in range(8):

        soma1 += (
            int(sequencial[i])
            * multiplicadores1[i]
        )

    resto1 = soma1 % 11

    # REGRA:
    # resto 10 -> DV = 0
    if resto1 == 10:
        dv1 = 0

    # REGRA ESPECIAL SP/MG
    elif resto1 == 0 and uf in ["01", "02"]:
        dv1 = 1

    else:
        dv1 = resto1

    # -------------------------
    # CÁLCULO DO SEGUNDO DV
    # -------------------------

    soma2 = (
        int(uf[0]) * 7
        + int(uf[1]) * 8
        + dv1 * 9
    )

    resto2 = soma2 % 11

    # REGRA:
    # resto 10 -> DV = 0
    if resto2 == 10:
        dv2 = 0

    # REGRA ESPECIAL SP/MG
    elif resto2 == 0 and uf in ["01", "02"]:
        dv2 = 1

    else:
        dv2 = resto2

    # COMPARA COM O TÍTULO INFORMADO
    return (
        dv1 == dv1_informado
        and dv2 == dv2_informado
    )


def gerar_chave(nome: str) -> str:
    """
    Gera uma chave de acesso personalizada.

    A chave é composta pelas primeiras letras
    do nome e sobrenome do eleitor, seguidas
    por quatro números aleatórios.

    Args:
        nome (str): Nome completo do eleitor.

    Returns:
        str: Chave de acesso gerada automaticamente.
    """

    lista_nome = nome.split()

    primeiro = lista_nome[0]

    parte_nome = primeiro[:2].lower()

    sobrenome = lista_nome[1]

    parte_sobrenome = sobrenome[0].lower()

    numeros = ''.join(
        str(random.randint(0, 9))
        for _ in range(4)
    )

    return (
        parte_nome
        + parte_sobrenome
        + numeros
    )