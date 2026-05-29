from utils.cripto.aula_de_hill26 import (
    cifrar_pares_numeros,
    decifrar_pares_numeros,
    num_para_letra,
    letra_para_num,
)

TAMANHO_CHAVE = 7  # original (LLLDDDD)


def _so_az09(s: str) -> str:
    s = str(s).upper()
    out = ""
    for ch in s:
        if ("A" <= ch <= "Z") or ("0" <= ch <= "9"):
            out += ch
    return out


def _pad_ultimo(s: str) -> str:
    # regra do seu CPF atual: duplica o ÚLTIMO quando é ímpar
    if len(s) % 2 == 1:
        s += s[-1]
    return s


def _char_para_num(ch: str) -> int:
    # dígito vira número 0..9
    if "0" <= ch <= "9":
        return int(ch)
    # letra vira índice da aula: Z=0, A=1..Y=25
    return letra_para_num(ch)


def _num_para_char(num: int, deve_ser_digito: bool) -> str:
    # na volta, se era dígito, esperamos 0..9
    if deve_ser_digito:
        return str(num % 10)
    return num_para_letra(num)


def criptografar_chave(chave: str) -> str:
    """
    Entrada: LLLDDDD (7 chars)
    Saída: 8 letras (Hill em pares) por causa do padding.
    """
    chave = _so_az09(chave)
    if len(chave) != 7:
        return ""

    chave8 = _pad_ultimo(chave)  # 7 -> 8

    pares = []
    for i in range(0, len(chave8), 2):
        x1 = _char_para_num(chave8[i])
        x2 = _char_para_num(chave8[i + 1])
        pares.append((x1, x2))

    cif = cifrar_pares_numeros(pares)

    out = ""
    for y1, y2 in cif:
        out += num_para_letra(y1) + num_para_letra(y2)
    return out


def descriptografar_chave(chave_cifrada: str) -> str:
    """
    Entrada: 8 letras
    Saída: LLLDDDD (7 chars)
    """
    texto = "".join(ch for ch in str(chave_cifrada).upper() if "A" <= ch <= "Z")
    if len(texto) != 8:
        return ""

    pares_cifrados = []
    for i in range(0, len(texto), 2):
        pares_cifrados.append((letra_para_num(texto[i]), letra_para_num(texto[i + 1])))

    pares = decifrar_pares_numeros(pares_cifrados)
    if pares is None:
        return ""

    # formato original (7):
    # pos 0..2 letras, pos 3..6 dígitos
    saida = ""
    idx = 0
    for x1, x2 in pares:
        for num in (x1, x2):
            # idx refere ao caractere na string DESCRIPTOGRAFADA (antes de cortar)
            deve_ser_digito = idx >= 3  # a partir do 4º char é dígito
            saida += _num_para_char(num, deve_ser_digito)
            idx += 1

    return saida[:7]