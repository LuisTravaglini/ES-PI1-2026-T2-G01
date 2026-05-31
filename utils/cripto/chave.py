"""
Criptografia e descriptografia da chave de acesso utilizando Cifra de Hill (mod 26).

Formato esperado da chave em claro:
- 3 letras + 4 dígitos (total 7 caracteres)

Como 7 é ímpar:
- aplica-se padding duplicando o último caractere, cifrando 8 caracteres.
"""

from utils.cripto.aula_de_hill26 import (
    cifrar_pares_numeros,
    decifrar_pares_numeros,
    num_para_letra,
    letra_para_num,
)

TAMANHO_CHAVE = 7


def _so_az09(s: str) -> str:
    """
    Mantém apenas caracteres alfanuméricos (A-Z e 0-9) e converte para maiúsculo.

    Args:
        s (str): Texto de entrada.

    Returns:
        str: Texto filtrado.
    """
    s = str(s).upper()
    out = ""
    for ch in s:
        if ("A" <= ch <= "Z") or ("0" <= ch <= "9"):
            out += ch
    return out


def _pad_ultimo(s: str) -> str:
    """
    Aplica padding se a string tiver tamanho ímpar, duplicando o último caractere.

    Args:
        s (str): Texto de entrada.

    Returns:
        str: Texto com tamanho par.
    """
    if len(s) % 2 == 1:
        s += s[-1]
    return s


def _char_para_num(ch: str) -> int:
    """
    Converte um caractere (letra ou dígito) para número 0..25.

    Args:
        ch (str): Caractere único (A-Z ou 0-9).

    Returns:
        int: Número equivalente no módulo 26.
    """
    if "0" <= ch <= "9":
        return int(ch)
    return letra_para_num(ch)


def _num_para_char(num: int, deve_ser_digito: bool) -> str:
    """
    Converte um número decifrado em caractere, respeitando o tipo esperado.

    Args:
        num (int): Valor 0..25.
        deve_ser_digito (bool): True se a posição original era dígito.

    Returns:
        str: Caractere reconstruído.
    """
    if deve_ser_digito:
        return str(num % 10)
    return num_para_letra(num)


def criptografar_chave(chave: str) -> str:
    """
    Criptografa uma chave de acesso em claro (7 caracteres) e retorna 8 letras.

    Args:
        chave (str): Chave em claro.

    Returns:
        str: Chave criptografada (8 letras) ou "" se inválida.
    """
    chave = _so_az09(chave)
    if len(chave) != 7:
        return ""

    chave8 = _pad_ultimo(chave)

    pares: list[tuple[int, int]] = []
    for i in range(0, len(chave8), 2):
        pares.append((_char_para_num(chave8[i]), _char_para_num(chave8[i + 1])))

    cif = cifrar_pares_numeros(pares)

    out = ""
    for y1, y2 in cif:
        out += num_para_letra(y1) + num_para_letra(y2)
    return out


def descriptografar_chave(chave_cifrada: str) -> str:
    """
    Descriptografa uma chave criptografada (8 letras) e retorna a chave em claro (7 caracteres).

    Args:
        chave_cifrada (str): Chave cifrada.

    Returns:
        str: Chave em claro (7 caracteres) ou "" se inválida/erro.
    """
    texto = "".join(ch for ch in str(chave_cifrada).upper() if "A" <= ch <= "Z")
    if len(texto) != 8:
        return ""

    pares_cifrados: list[tuple[int, int]] = []
    for i in range(0, len(texto), 2):
        pares_cifrados.append((letra_para_num(texto[i]), letra_para_num(texto[i + 1])))

    pares = decifrar_pares_numeros(pares_cifrados)
    if pares is None:
        return ""

    saida = ""
    idx = 0
    for x1, x2 in pares:
        for num in (x1, x2):
            deve_ser_digito = idx >= 3
            saida += _num_para_char(num, deve_ser_digito)
            idx += 1

    return saida[:7]