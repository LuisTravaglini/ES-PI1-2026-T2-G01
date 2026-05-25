# utils/crypto/protocolo.py
from utils.cripto.criptografia import criptografar as _criptografar, descriptografar as _descriptografar

TAMANHO_PROTOCOLO = 12


def criptografar_protocolo(protocolo: str) -> str:
    return _criptografar(protocolo)


def descriptografar_protocolo(protocolo_cifrado: str) -> str:
    return _descriptografar(protocolo_cifrado, TAMANHO_PROTOCOLO)