CHAVE = [[4, 3],
         [1, 2]]
MOD = 26


def _so_letras_az(texto):
    texto = texto.upper()
    saida = ""
    for c in texto:
        if "A" <= c <= "Z":
            saida += c
    return saida


def letra_para_num(letra):
    # A..Y = 1..25, Z = 0
    if letra == "Z":
        return 0
    return ord(letra) - ord("A") + 1


def num_para_letra(n):
    # 0->Z, 1->A, ..., 25->Y
    n = n % MOD
    if n == 0:
        return "Z"
    return chr(ord("A") + n - 1)


def _mdc(a, b):
    while b != 0:
        a, b = b, a % b
    return a


def _inverso_mod(a, m):
    # acha x tal que (a*x) % m == 1
    a = a % m
    if _mdc(a, m) != 1:
        return None
    x = 1
    while x < m:
        if (a * x) % m == 1:
            return x
        x += 1
    return None


def _inversa_chave():
    a = CHAVE[0][0]
    b = CHAVE[0][1]
    c = CHAVE[1][0]
    d = CHAVE[1][1]

    det = (a * d - b * c) % MOD
    det_inv = _inverso_mod(det, MOD)
    if det_inv is None:
        return None

    inv = [
        [(det_inv * d) % MOD, (det_inv * (-b)) % MOD],
        [(det_inv * (-c)) % MOD, (det_inv * a) % MOD],
    ]
    return inv


def decifrar_hill(texto_cifrado):
    texto_cifrado = _so_letras_az(texto_cifrado)

    if len(texto_cifrado) % 2 == 1:
        return None

    inv = _inversa_chave()
    if inv is None:
        return None

    saida = ""
    i = 0
    while i < len(texto_cifrado):
        y1 = letra_para_num(texto_cifrado[i])
        y2 = letra_para_num(texto_cifrado[i + 1])

        x1 = (inv[0][0] * y1 + inv[0][1] * y2) % MOD
        x2 = (inv[1][0] * y1 + inv[1][1] * y2) % MOD

        saida += num_para_letra(x1)
        saida += num_para_letra(x2)
        i += 2

    return saida