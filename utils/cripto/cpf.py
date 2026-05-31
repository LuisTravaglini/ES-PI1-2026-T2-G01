"""
Criptografia/Descriptografia do CPF usando Cifra de Hill mod 26 (padrão da aula).

Regras:
- CPF é armazenado criptografado no banco.
- CPF original tem 11 dígitos (ímpar), então é aplicado padding (vira 12) duplicando o último dígito.
- O CPF cifrado retorna letras no padrão Z/A..Y.
"""

from utils.cripto.aula_de_hill26 import (
    cifrar_pares_numeros,
    decifrar_pares_numeros,
    num_para_letra,
    letra_para_num,
)

TAMANHO_CPF = 11


def _so_digitos(s: str) -> str:
    """
    Remove qualquer caractere que não seja dígito.

    Args:
        s (str): Texto de entrada.

    Returns:
        str: Apenas os dígitos contidos em s.
    """
    return "".join(ch for ch in str(s) if ch.isdigit())


def _cpf_com_padding(cpf11: str) -> str:
    """
    Aplica padding ao CPF (11 dígitos) para torná-lo par (12 dígitos).

    Regra adotada:
    - Se o CPF tem 11 dígitos, duplica o ÚLTIMO dígito e anexa ao final.

    Args:
        cpf11 (str): CPF com 11 dígitos.

    Returns:
        str: CPF com 12 dígitos (padding aplicado).
    """
    return cpf11 + cpf11[-1]


def _cifrar_digitos_em_pares(digs: str) -> str:
    """
    Cifra uma string de dígitos em pares, convertendo cada dígito para inteiro
    e aplicando Cifra de Hill mod 26.

    Args:
        digs (str): String contendo quantidade PAR de dígitos.

    Returns:
        str: Texto cifrado em letras (cada par gera 2 letras).
    """
    pares: list[tuple[int, int]] = []
    for i in range(0, len(digs), 2):
        pares.append((int(digs[i]), int(digs[i + 1])))

    cif = cifrar_pares_numeros(pares)

    out = ""
    for y1, y2 in cif:
        out += num_para_letra(y1) + num_para_letra(y2)
    return out


def criptografar_cpf(cpf: str) -> str:
    """
    Criptografa um CPF (11 dígitos) e retorna 12 letras.

    Args:
        cpf (str): CPF em claro (pode conter máscara).

    Returns:
        str: CPF criptografado (12 letras) ou "" se inválido.
    """
    cpf = _so_digitos(cpf)
    if len(cpf) != 11:
        return ""

    cpf12 = _cpf_com_padding(cpf)
    return _cifrar_digitos_em_pares(cpf12)


def criptografar_prefixo4_cpf(prefixo4: str) -> str:
    """
    Criptografa apenas os 4 primeiros dígitos do CPF.

    Args:
        prefixo4 (str): String com 4 dígitos.

    Returns:
        str: 4 letras criptografadas ou "" se inválido.
    """
    p = _so_digitos(prefixo4)
    if len(p) != 4:
        return ""
    return _cifrar_digitos_em_pares(p)


def descriptografar_cpf(cpf_cifrado: str) -> str:
    """
    Descriptografa um CPF cifrado (12 letras) e retorna o CPF original (11 dígitos),
    removendo o padding final.

    Args:
        cpf_cifrado (str): CPF criptografado (12 letras A-Z).

    Returns:
        str: CPF em claro (11 dígitos) ou "" se inválido/erro.
    """
    texto = "".join(ch for ch in str(cpf_cifrado).upper() if "A" <= ch <= "Z")
    if len(texto) != 12:
        return ""

    pares_cifrados: list[tuple[int, int]] = []
    for i in range(0, len(texto), 2):
        pares_cifrados.append((letra_para_num(texto[i]), letra_para_num(texto[i + 1])))

    pares = decifrar_pares_numeros(pares_cifrados)
    if pares is None:
        return ""

    digs = ""
    for x1, x2 in pares:
        digs += str(x1) + str(x2)

    return digs[:11]