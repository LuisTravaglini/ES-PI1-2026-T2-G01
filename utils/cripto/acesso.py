from utils.cripto.criptografia import criptografar as _criptografar, descriptografar as _descriptografar

TAMANHO_CHAVE = 7


def criptografar_chave(chave: str) -> str:
    return _criptografar(chave)


def descriptografar_chave(chave_cifrada: str) -> str:
    return _descriptografar(chave_cifrada, TAMANHO_CHAVE)