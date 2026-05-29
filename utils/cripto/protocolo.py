from utils.cripto.aula_de_hill26 import (
    cifrar_pares_numeros,
    decifrar_pares_numeros,
    num_para_letra,
    letra_para_num,
)

TAMANHO_PROTOCOLO = 12


def _so_az09(s: str) -> str:
    s = str(s).upper()
    out = ""
    for ch in s:
        if ("A" <= ch <= "Z") or ("0" <= ch <= "9"):
            out += ch
    return out


def _char_para_num(ch: str) -> int:
    if "0" <= ch <= "9":
        return int(ch)
    return letra_para_num(ch)


def _num_para_char(num: int, deve_ser_digito: bool) -> str:
    if deve_ser_digito:
        return str(num % 10)
    return num_para_letra(num)


def criptografar_protocolo(protocolo: str) -> str:
    protocolo = _so_az09(protocolo)
    if len(protocolo) != 12:
        return ""

    pares = []
    for i in range(0, 12, 2):
        pares.append((_char_para_num(protocolo[i]), _char_para_num(protocolo[i + 1])))

    cif = cifrar_pares_numeros(pares)

    out = ""
    for y1, y2 in cif:
        out += num_para_letra(y1) + num_para_letra(y2)
    return out


def descriptografar_protocolo(protocolo_cifrado: str) -> str:
    texto = "".join(ch for ch in str(protocolo_cifrado).upper() if "A" <= ch <= "Z")
    if len(texto) != 12:
        return ""

    pares_cifrados = []
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