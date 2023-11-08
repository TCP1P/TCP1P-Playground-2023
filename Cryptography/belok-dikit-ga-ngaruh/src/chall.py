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

FLAG = open("src/flag.txt", "rb").read().strip()
pt = s2n(FLAG)
PRNG = PRNG()

with open("src/out.txt", "w+") as f:
    for i in range(6):
        f.write(str(PRNG.next_number()))
        f.write("\n")
    pt = pt ^ PRNG.next_number()
    f.write(str(pt))
    f.write("\n")