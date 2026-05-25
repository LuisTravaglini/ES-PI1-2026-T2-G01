from utils.codificar import cifrar_hill
from utils.descriptografar import decifrar_hill
from utils.criptografia import (
    criptografar, 
    descriptografar
)
texto = "40580282899"

c = criptografar(texto)
d = descriptografar(c)

print("Texto:", texto)
print("Cifrado:", c)
print("Decifrado:", d)