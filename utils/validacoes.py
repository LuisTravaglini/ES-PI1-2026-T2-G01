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

    numeros = "".join(
        ch for ch in titulo if ch.isdigit()
    )

    return (
        len(numeros) == 12
        and numeros != numeros[0] * 12
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