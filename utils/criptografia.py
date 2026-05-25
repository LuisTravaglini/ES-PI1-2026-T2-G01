"""
Módulo responsável por adaptar textos com dígitos para criptografia Hill.

Regra de conversão de dígitos:
0 -> Z
1 -> A
2 -> B
...
9 -> I

"""

from utils.codificar import cifrar_hill
from utils.descriptografar import decifrar_hill


_DIG_PARA_LETRA = {
    "0": "Z",
    "1": "A",
    "2": "B",
    "3": "C",
    "4": "D",
    "5": "E",
    "6": "F",
    "7": "G",
    "8": "H",
    "9": "I",
}

_LETRA_PARA_DIG = {
    "Z": "0",
    "A": "1",
    "B": "2",
    "C": "3",
    "D": "4",
    "E": "5",
    "F": "6",
    "G": "7",
    "H": "8",
    "I": "9",
}


def normalizar_alfa_num(texto: str) -> str:
    """
    Mantém apenas A-Z e 0-9 e converte para maiúsculo.

    Args:
        texto (str): Texto original.

    Returns:
        str: Texto filtrado com A-Z e 0-9 (maiúsculo).
    """
    texto = str(texto).upper()
    saida = ""

    for c in texto:
        if ("A" <= c <= "Z") or ("0" <= c <= "9"):
            saida += c

    return saida


def digitos_para_letras(texto: str) -> str:
    """
    Converte dígitos 0-9 para letras conforme regra do projeto.

    Args:
        texto (str): Texto contendo dígitos/letras.

    Returns:
        str: Texto só com letras A-Z.
    """
    texto = normalizar_alfa_num(texto)

    saida = ""
    for c in texto:
        if "0" <= c <= "9":
            saida += _DIG_PARA_LETRA[c]
        else:
            # já é A-Z
            saida += c

    return saida


def letras_para_digitos(texto: str) -> str:
    """
    Converte letras Z e A-I de volta para dígitos, mantendo outras letras.

    Args:
        texto (str): Texto com letras A-Z.

    Returns:
        str: Texto com dígitos reconstruídos quando aplicável.
    """
    texto = str(texto).upper()

    saida = ""
    for c in texto:
        if c in _LETRA_PARA_DIG:
            saida += _LETRA_PARA_DIG[c]
        else:
            saida += c

    return saida


def criptografar(texto: str) -> str:
    """
    Criptografa texto alfanumérico (A-Z e 0-9) usando Hill.

    Args:
        texto (str): Texto original.

    Returns:
        str: Texto cifrado (A-Z).
    """
    convertido = digitos_para_letras(texto)
    return cifrar_hill(convertido)


def descriptografar(texto_cifrado: str) -> str:
    """
    Descriptografa texto cifrado (A-Z) usando Hill e reconverte dígitos.

    Args:
        texto_cifrado (str): Texto cifrado.

    Returns:
        str: Texto decifrado (com dígitos reconstruídos quando aplicável).
    """
    dec = decifrar_hill(texto_cifrado)
    if dec is None:
        return ""

    return letras_para_digitos(dec)