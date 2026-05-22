CHAVE = [[4, 3],
         [1, 2]]
MOD = 26


def letras_az(texto):
    texto = texto.upper()
    saida = ""
    for c in texto:
        if "A" <= c <= "Z":
            saida += c
    return saida


def _ajustar_impar(texto):
    # Regra: se ímpar, duplica a PENÚLTIMA letra
    if len(texto) % 2 == 1:
        if len(texto) == 1:
            texto = texto + texto
        else:
            texto = texto + texto[-2]
    return texto


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


def cifrar_hill(texto):
    texto = letras_az(texto)
    texto = _ajustar_impar(texto)

    saida = ""
    i = 0
    while i < len(texto):
        x1 = letra_para_num(texto[i])
        x2 = letra_para_num(texto[i + 1])

        y1 = (CHAVE[0][0] * x1 + CHAVE[0][1] * x2) % MOD
        y2 = (CHAVE[1][0] * x1 + CHAVE[1][1] * x2) % MOD

        saida += num_para_letra(y1)
        saida += num_para_letra(y2)
        i += 2

    return saida