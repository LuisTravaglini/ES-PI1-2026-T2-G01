"""
Criptografia/Descriptografia do Protocolo de Votação usando Cifra de Hill mod 26.

Formato do protocolo (requisito):
- "V" + 2 letras + "26" + número do candidato (2 dígitos) + 5 dígitos aleatórios
- Total = 12 caracteres (3 letras + 9 dígitos) => já é par (não precisa padding)

Regras adotadas:
- Letras são convertidas para 0..25 usando a convenção da aula (Z=0, A=1..Y=25)
- Dígitos '0'..'9' viram números 0..9 diretamente
"""

from utils.cripto.aula_de_hill26 import (
    cifrar_pares_numeros,
    decifrar_pares_numeros,
    num_para_letra,
    letra_para_num,
)

TAMANHO_PROTOCOLO = 12


def _so_az09(s: str) -> str:
    """
    Mantém apenas letras A-Z e dígitos 0-9, e converte para maiúsculo.

    Args:
        s (str): Texto de entrada.

    Returns:
        str: Texto filtrado contendo somente A-Z e 0-9.
    """
    s = str(s).upper()
    out = ""
    for ch in s:
        if ("A" <= ch <= "Z") or ("0" <= ch <= "9"):
            out += ch
    return out


def _char_para_num(ch: str) -> int:
    """
    Converte um caractere (letra ou dígito) para número 0..25.

    Args:
        ch (str): Caractere único (A-Z ou 0-9).

    Returns:
        int: Número equivalente para cifragem Hill.
    """
    if "0" <= ch <= "9":
        return int(ch)
    return letra_para_num(ch)


def _num_para_char(num: int, deve_ser_digito: bool) -> str:
    """
    Converte número decifrado em caractere conforme o tipo esperado na posição.

    Args:
        num (int): Número 0..25.
        deve_ser_digito (bool): Indica se a posição original era dígito.

    Returns:
        str: Caractere reconstruído.
    """
    if deve_ser_digito:
        return str(num % 10)
    return num_para_letra(num)


def criptografar_protocolo(protocolo: str) -> str:
    """
    Criptografa um protocolo em claro (12 chars) e retorna 12 letras.

    Args:
        protocolo (str): Protocolo em claro (12 caracteres A-Z/0-9).

    Returns:
        str: Protocolo criptografado (12 letras) ou "" se inválido.
    """
    protocolo = _so_az09(protocolo)
    if len(protocolo) != 12:
        return ""

    pares: list[tuple[int, int]] = []
    for i in range(0, 12, 2):
        pares.append((_char_para_num(protocolo[i]), _char_para_num(protocolo[i + 1])))

    cif = cifrar_pares_numeros(pares)

    out = ""
    for y1, y2 in cif:
        out += num_para_letra(y1) + num_para_letra(y2)
    return out


def descriptografar_protocolo(protocolo_cifrado: str) -> str:
    """
    Descriptografa um protocolo cifrado (12 letras) e retorna o protocolo original (12 chars).

    Args:
        protocolo_cifrado (str): Protocolo criptografado (12 letras A-Z).

    Returns:
        str: Protocolo em claro (12 chars) ou "" se inválido/erro.
    """
    texto = "".join(ch for ch in str(protocolo_cifrado).upper() if "A" <= ch <= "Z")
    if len(texto) != 12:
        return ""

    pares_cifrados: list[tuple[int, int]] = []
    for i in range(0, 12, 2):
        pares_cifrados.append((letra_para_num(texto[i]), letra_para_num(texto[i + 1])))

    pares = decifrar_pares_numeros(pares_cifrados)
    if pares is None:
        return ""

    # protocolo: 3 letras + 9 dígitos
    saida = ""
    idx = 0
    for x1, x2 in pares:
        for num in (x1, x2):
            deve_ser_digito = idx >= 3
            saida += _num_para_char(num, deve_ser_digito)
            idx += 1

    return saida[:12]