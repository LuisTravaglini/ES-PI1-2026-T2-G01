# utils/crypto/base.py
from utils.cripto.codificar import cifrar_hill
from utils.cripto.descriptografar import decifrar_hill

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

_ESCAPE = "Q"


def normalizar_alfa_num(texto: str) -> str:
    texto = str(texto).upper()
    out = ""
    for c in texto:
        if ("A" <= c <= "Z") or ("0" <= c <= "9"):
            out += c
    return out


def alfa_num_para_letras(texto: str) -> str:
    texto = normalizar_alfa_num(texto)
    out = ""
    for c in texto:
        if "0" <= c <= "9":
            out += _ESCAPE + _DIG_PARA_LETRA[c]
        else:
            out += c
    return out


def letras_para_alfa_num(texto: str) -> str:
    texto = str(texto).upper()
    out = ""
    i = 0
    while i < len(texto):
        if texto[i] == _ESCAPE and i + 1 < len(texto) and texto[i + 1] in _LETRA_PARA_DIG:
            out += _LETRA_PARA_DIG[texto[i + 1]]
            i += 2
        else:
            out += texto[i]
            i += 1
    return out


def criptografar(texto: str) -> str:
    convertido = alfa_num_para_letras(texto)
    return cifrar_hill(convertido)


def descriptografar(texto_cifrado: str, tamanho_original: int) -> str:
    dec = decifrar_hill(texto_cifrado)
    if dec is None:
        return ""

    # regra do trabalho: se o original era ímpar, o cifrador adicionou 1 char
    if tamanho_original % 2 == 1:
        dec = dec[:-1]

    return letras_para_alfa_num(dec)