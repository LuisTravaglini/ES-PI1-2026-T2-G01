# utils/crypto/cpf.py
from utils.cripto.criptografia import criptografar as _criptografar, descriptografar as _descriptografar

TAMANHO_CPF = 11


def criptografar_cpf(cpf: str) -> str:
    return _criptografar(cpf)


def descriptografar_cpf(cpf_cifrado: str) -> str:
    return _descriptografar(cpf_cifrado, TAMANHO_CPF)