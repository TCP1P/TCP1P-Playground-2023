from libnum import *
from Crypto.Util.number import *

class PRNG:
    def __init__(self):
        self.n = getStrongPrime(2048)
        self.state = getRandomNBitInteger(2047)
        self.a = getRandomNBitInteger(24)
        self.b = getRandomNBitInteger(24)
        for i in range(10):
            self.next_number()
    
    def next_number(self):
        self.state = self.a * (self.state ** 2) + self.b
        self.state = self.state % self.n
        return self.state

flag = open("src/flag.txt", "rb").read().strip()
assert(flag.startswith(b"TCP1P{"))
flag = flag.replace(b'TCP1P{', b'')
assert(flag.endswith(b"}"))
flag = flag.replace(b'}', b'')
pt = s2n(flag)
PRNG = PRNG()

with open("src/out.txt", "w+") as f:
    for i in range(6):
        f.write(str(PRNG.next_number()))
        f.write("\n")
    pt = pt ^ PRNG.next_number()
    f.write(str(pt))
    f.write("\n")