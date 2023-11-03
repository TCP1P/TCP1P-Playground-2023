from sage.all import *

with open("flag.txt","rb") as f:
    FLAG = f.read()

n = len(FLAG)

V = Permutations(n)

G = V.random_element()

Cipher = bytes([FLAG[G[i] - 1] for i in range(n)])


e = next_prime(n)
P = G ** e

Cipher = Cipher.decode()

print(f"{P = }")
print(f"{Cipher = }")