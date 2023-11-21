from Crypto.Util.number import getPrime, bytes_to_long
from secret import message, x, y

p = getPrime(y)
n = p ** x
e = 0x10001
c = pow(bytes_to_long(message), e, n)

print(f"n = {n}")
print(f"e = {e}")
print(f"c = {c}")
