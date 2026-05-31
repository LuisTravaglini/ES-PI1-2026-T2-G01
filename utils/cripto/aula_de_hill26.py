"""
Implementação da Cifra de Hill (2x2) em módulo 26 no padrão definido em aula.

Convenção usada:
- Z -> 0
- A -> 1
- ...
- Y -> 25

A chave fixa do projeto é:
    [[4, 3],
     [1, 2]]

Este módulo fornece funções utilitárias para:
- converter letra <-> número
- calcular inverso modular
- calcular a inversa da matriz 2x2 no módulo 26
- cifrar e decifrar listas de pares numéricos
"""

CHAVE = [[4, 3],
         [1, 2]]
MOD = 26

ALFABETO = ["Z"] + [chr(ord("A") + i) for i in range(25)]


def letra_para_num(letra: str) -> int:
    """
    Converte uma letra (A-Z) para um número no padrão da aula.

    Args:
        letra (str): Letra a ser convertida.

    Returns:
        int: Número equivalente no intervalo 0..25 (Z=0, A=1, ..., Y=25).
    """
    letra = str(letra).upper()
    if letra == "Z":
        return 0
    return ord(letra) - ord("A") + 1


def num_para_letra(n: int) -> str:
    """
    Converte um número no intervalo 0..25 para uma letra no padrão da aula.

    Args:
        n (int): Número a ser convertido.

    Returns:
        str: Letra equivalente (0->Z, 1->A, ..., 25->Y).
    """
    n %= MOD
    if n == 0:
        return "Z"
    return chr(ord("A") + n - 1)


def _mdc(a: int, b: int) -> int:
    """
    Calcula o máximo divisor comum (MDC) entre a e b.

    Args:
        a (int): Primeiro número.
        b (int): Segundo número.

    Returns:
        int: O MDC(a, b).
    """
    while b:
        a, b = b, a % b
    return a


def inverso_mod(a: int, m: int) -> int | None:
    """
    Calcula o inverso multiplicativo de 'a' no módulo 'm'.

    Encontra x tal que:
        (a * x) % m == 1

    Args:
        a (int): Valor para o qual se deseja o inverso.
        m (int): Módulo.

    Returns:
        int | None: Inverso modular se existir, caso contrário None.
    """
    a %= m
    if _mdc(a, m) != 1:
        return None
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    return None


def inversa_2x2_mod26(chave: list[list[int]]) -> list[list[int]] | None:
    """
    Calcula a inversa de uma matriz 2x2 no módulo 26.

    Para uma matriz:
        [a b]
        [c d]
    a inversa (mod 26) existe se det for inversível mod 26.

    Args:
        chave (list[list[int]]): Matriz 2x2.

    Returns:
        list[list[int]] | None: Matriz inversa 2x2 no módulo 26, ou None se não existir.
    """
    a, b = chave[0]
    c, d = chave[1]

    det = (a * d - b * c) % MOD
    det_inv = inverso_mod(det, MOD)
    if det_inv is None:
        return None

    inv = [
        [(det_inv * d) % MOD, (det_inv * (-b)) % MOD],
        [(det_inv * (-c)) % MOD, (det_inv * a) % MOD],
    ]
    return inv


def cifrar_pares_numeros(pares: list[tuple[int, int]]) -> list[tuple[int, int]]:
    """
    Cifra uma lista de pares numéricos (x1, x2) usando a Cifra de Hill 2x2 mod 26.

    Cada par é tratado como um vetor coluna X, e a cifra é:
        Y = CHAVE * X (mod 26)

    Args:
        pares (list[tuple[int, int]]): Lista de pares (x1, x2), cada um em 0..25.

    Returns:
        list[tuple[int, int]]: Lista de pares cifrados (y1, y2) em 0..25.
    """
    out: list[tuple[int, int]] = []
    for x1, x2 in pares:
        y1 = (CHAVE[0][0] * x1 + CHAVE[0][1] * x2) % MOD
        y2 = (CHAVE[1][0] * x1 + CHAVE[1][1] * x2) % MOD
        out.append((y1, y2))
    return out


def decifrar_pares_numeros(pares_cifrados: list[tuple[int, int]]) -> list[tuple[int, int]] | None:
    """
    Decifra uma lista de pares numéricos (y1, y2) usando a inversa da matriz CHAVE.

    Cada par é tratado como um vetor coluna Y, e a decifra é:
        X = CHAVE^-1 * Y (mod 26)

    Args:
        pares_cifrados (list[tuple[int, int]]): Lista de pares cifrados (y1, y2).

    Returns:
        list[tuple[int, int]] | None: Lista de pares decifrados (x1, x2) ou None se não existir inversa.
    """
    inv = inversa_2x2_mod26(CHAVE)
    if inv is None:
        return None

    out: list[tuple[int, int]] = []
    for y1, y2 in pares_cifrados:
        x1 = (inv[0][0] * y1 + inv[0][1] * y2) % MOD
        x2 = (inv[1][0] * y1 + inv[1][1] * y2) % MOD
        out.append((x1, x2))
    return out