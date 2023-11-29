from Crypto.Util.number import *
from output import *

p = 13517320509842582039844708650743296878732182021493666519676728360245752217336665512491731939984100054350599823381878161842911677750085924434889627166895103

C1_flag, C2_flag = ciphertext[-1]

for i, c in enumerate(ciphertext[:-1]):
    m = bytes_to_long(c[2])
    flag = long_to_bytes(C2_flag * pow(c[1], -1, p) * m % p)
    if b"TCP1P" in flag:
        print(flag, i)
        break