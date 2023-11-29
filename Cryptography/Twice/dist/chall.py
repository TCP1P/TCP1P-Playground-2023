from Crypto.Util.number import *
import random, string

with open("flag.txt", "rb") as f:
    FLAG = f.read() 

assert FLAG.startswith(b"TCP1P{")

N = 5000

class ElGamal:
    def __init__(self):
        self.p = 13517320509842582039844708650743296878732182021493666519676728360245752217336665512491731939984100054350599823381878161842911677750085924434889627166895103
        self.q = (self.p - 1) // 2
        self.g = 2
        self.pub, self.priv = self.gen_keys()
        self.k = [random.randint(2, self.p -2) % self.q for i in range(N)]
        self.idx = 0

    def gen_keys(self):
        a = random.randint(1, self.p-1)
        return pow(self.g, a, self.p), a


    def encrypt(self, m):
        self.m = bytes_to_long(m)
        k = self.k[self.idx % len(self.k)]
        self.idx += 1
        c1 = pow(self.g, k, self.p)
        c2 = (self.m * pow(self.pub, k, self.p))% self.p
        return c1, c2

    def decrypt(self, c1, c2):
        x = inverse(pow(c1, self.priv, self.p), self.p)
        m =(x * c2) % self.p
        return long_to_bytes(m)



cipher = ElGamal()
ciphertext = []

for i in range(N):
    plain = "".join(random.choices(string.ascii_uppercase, k = 10)).encode()
    c1, c2 = cipher.encrypt(plain)
    ciphertext.append((c1, c2, plain))


assert cipher.decrypt(ciphertext[0][0], ciphertext[0][1]) == ciphertext[0][2]

random.shuffle(ciphertext)

c1, c2 = cipher.encrypt(FLAG)
ciphertext.append((c1, c2))
print(f"{ciphertext = }")
