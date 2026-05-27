from utils.cripto.aula_de_hill26 import (
    cifrar_pares_numeros,
    decifrar_pares_numeros,
    num_para_letra,
    letra_para_num
)

TAMANHO_CPF = 11


def _so_digitos(s: str) -> str:
    return "".join(ch for ch in str(s) if ch.isdigit())


def _cpf_com_padding(cpf11: str) -> str:
    """
    CPF tem 11 (ímpar). Para virar par (12), duplica o ÚLTIMO dígito.
    (Se seu professor exigir "penúltimo", troque cpf11[-1] por cpf11[-2].)
    """
    return cpf11 + cpf11[-1]


def _cifrar_digitos_em_pares(digs: str) -> str:
    pares = []
    for i in range(0, len(digs), 2):
        pares.append((int(digs[i]), int(digs[i + 1])))

    cif = cifrar_pares_numeros(pares)

    out = ""
    for y1, y2 in cif:
        out += num_para_letra(y1) + num_para_letra(y2)
    return out


def criptografar_cpf(cpf: str) -> str:
    cpf = _so_digitos(cpf)
    if len(cpf) != 11:
        return ""
    cpf12 = _cpf_com_padding(cpf)
    return _cifrar_digitos_em_pares(cpf12)


def criptografar_prefixo4_cpf(prefixo4: str) -> str:
    """
    Recebe 4 dígitos e devolve 4 letras compatíveis com LEFT(CPF,4).
    """
    p = _so_digitos(prefixo4)
    if len(p) != 4:
        return ""
    return _cifrar_digitos_em_pares(p)


def descriptografar_cpf(cpf_cifrado: str) -> str:
    """
    Volta para os 11 dígitos originais (remove o padding final).
    cpf_cifrado deve ter 12 letras.
    """
    texto = "".join(ch for ch in str(cpf_cifrado).upper() if "A" <= ch <= "Z")
    if len(texto) != 12:
        return ""

    pares_cifrados = []
    for i in range(0, len(texto), 2):
        pares_cifrados.append((letra_para_num(texto[i]), letra_para_num(texto[i + 1])))

    pares = decifrar_pares_numeros(pares_cifrados)
    if pares is None:
        return ""

    digs = ""
    for x1, x2 in pares:
        digs += str(x1) + str(x2)

    return digs[:11]