"""
Módulo responsável pela criptografia Hill Cipher.

Este módulo contém funções para tratamento
de texto, conversão de letras para números
e criptografia utilizando a cifra de Hill.
"""

# MATRIZ CHAVE UTILIZADA NA CIFRAGEM
CHAVE = [
    [4, 3],
    [1, 2]
]

# VALOR UTILIZADO PARA OPERAÇÕES MODULARES
MOD = 26


def letras_az(texto):
    """
    Remove caracteres inválidos e mantém apenas letras de A a Z.

    A função converte todas as letras para maiúsculas
    e remove espaços, números e caracteres especiais.

    Args:
        texto (str): Texto original informado pelo usuário.

    Returns:
        str: Texto contendo apenas letras maiúsculas.
    """

    texto = texto.upper()

    saida = ""

    for c in texto:

        if "A" <= c <= "Z":

            saida += c

    return saida


def _ajustar_impar(texto):
    """
    Ajusta textos com quantidade ímpar de caracteres.

    Caso o texto tenha tamanho ímpar, a função duplica
    a penúltima letra para completar o bloco da cifra.

    Args:
        texto (str): Texto que será ajustado.

    Returns:
        str: Texto ajustado para possuir tamanho par.
    """

    if len(texto) % 2 == 1:

        if len(texto) == 1:

            texto = texto + texto

        else:

            texto = texto + texto[-2]

    return texto


def letra_para_num(letra):
    """
    Converte uma letra em valor numérico.

    Regras:
    - A até Y correspondem aos números 1 até 25.
    - Z corresponde ao valor 0.

    Args:
        letra (str): Letra que será convertida.

    Returns:
        int: Valor numérico correspondente à letra.
    """

    if letra == "Z":

        return 0

    return ord(letra) - ord("A") + 1


def num_para_letra(n):
    """
    Converte um valor numérico em letra.

    Regras:
    - 0 corresponde à letra Z.
    - 1 até 25 correspondem às letras A até Y.

    Args:
        n (int): Valor numérico a ser convertido.

    Returns:
        str: Letra correspondente ao número informado.
    """

    n = n % MOD

    if n == 0:

        return "Z"

    return chr(ord("A") + n - 1)


def cifrar_hill(texto):
    """
    Realiza a criptografia do texto utilizando Hill Cipher.

    O texto é dividido em pares de letras e multiplicado
    pela matriz chave definida no sistema.

    Args:
        texto (str): Texto original que será criptografado.

    Returns:
        str: Texto criptografado utilizando a cifra de Hill.
    """

    texto = letras_az(texto)

    texto = _ajustar_impar(texto)

    saida = ""

    i = 0

    while i < len(texto):

        x1 = letra_para_num(texto[i])

        x2 = letra_para_num(texto[i + 1])

        y1 = (
            CHAVE[0][0] * x1
            + CHAVE[0][1] * x2
        ) % MOD

        y2 = (
            CHAVE[1][0] * x1
            + CHAVE[1][1] * x2
        ) % MOD

        saida += num_para_letra(y1)

        saida += num_para_letra(y2)

        i += 2

    return saida