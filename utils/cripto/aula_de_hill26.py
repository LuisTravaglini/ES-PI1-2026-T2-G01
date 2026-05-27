CHAVE = [[4, 3],
         [1, 2]]
MOD = 26

# Convenção da aula:
# Z -> 0
# A -> 1
# ...
# Y -> 25
ALFABETO = ["Z"] + [chr(ord("A") + i) for i in range(25)]  # ["Z","A",...,"Y"]


def letra_para_num(letra: str) -> int:
    letra = letra.upper()
    if letra == "Z":
        return 0
    return ord(letra) - ord("A") + 1


def num_para_letra(n: int) -> str:
    n %= MOD
    if n == 0:
        return "Z"
    return chr(ord("A") + n - 1)


def _mdc(a: int, b: int) -> int:
    while b:
        a, b = b, a % b
    return a


def inverso_mod(a: int, m: int) -> int | None:
    a %= m
    if _mdc(a, m) != 1:
        return None
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    return None


def inversa_2x2_mod26(chave):
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
    out = []
    for x1, x2 in pares:
        y1 = (CHAVE[0][0] * x1 + CHAVE[0][1] * x2) % MOD
        y2 = (CHAVE[1][0] * x1 + CHAVE[1][1] * x2) % MOD
        out.append((y1, y2))
    return out


def decifrar_pares_numeros(pares_cifrados: list[tuple[int, int]]) -> list[tuple[int, int]] | None:
    inv = inversa_2x2_mod26(CHAVE)
    if inv is None:
        return None

    out = []
    for y1, y2 in pares_cifrados:
        x1 = (inv[0][0] * y1 + inv[0][1] * y2) % MOD
        x2 = (inv[1][0] * y1 + inv[1][1] * y2) % MOD
        out.append((x1, x2))
    return out