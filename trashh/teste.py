from utils.cripto.codificar import cifrar_hill
from utils.cripto.descriptografar import decifrar_hill
from utils.cripto.criptografia import (
    criptografar, 
    descriptografar
)
texto = "GBYXBUDO"

c = criptografar(texto)
d = descriptografar(c)

print("Texto:", texto)
print("Cifrado:", c)
print("Decifrado:", d)