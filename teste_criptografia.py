from utils.codificar import cifrar_hill
from utils.descriptografar import decifrar_hill

texto = "LOVES"

c = cifrar_hill(texto)
d = decifrar_hill(c)

print("Texto:", texto)
print("Cifrado:", c)
print("Decifrado:", d)