from libnum import *
import numpy as np
import ecdsa
from pwn import xor, process, remote
from Crypto.Hash import SHA256
from ecdsa import ellipticcurve as EC
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tqdm import tqdm

re = remote("localhost", int(8010))

d = 91902981401375538375972937489272997252690321931317878648439125771978424689532
curve = ecdsa.curves.NIST256p
n = curve.order

def getRand(seed=None):
    if seed != None:
        np.random.seed(seed)
    return np.random.random((1, 4))

def decrypt(message: EC.PointJacobi)-> EC.PointJacobi:
    return message * 69 * pow(d, 420, n)

def legendre(a, p):
    return pow(a, (p - 1) // 2, p)

def tonelli(n, p):
    q = p - 1
    s = 0
    while q % 2 == 0:
        q //= 2
        s += 1
    if s == 1:
        return pow(n, (p + 1) // 4, p)
    for z in range(2, p):
        if p - 1 == legendre(z, p):
            break
    c = pow(z, q, p)
    r = pow(n, (q + 1) // 2, p)
    t = pow(n, q, p)
    m = s
    t2 = 0
    while (t - 1) % p != 0:
        t2 = (t * t) % p
        for i in range(1, m):
            if (t2 - 1) % p == 0:
                break
            t2 = (t2 * t2) % p
        b = pow(c, 1 << (m - i - 1), p)
        r = (r * b) % p
        c = (b * b) % p
        t = (t * c) % p
        m = i
    return r

def lift_x(x):
    assert(x > 0)
    a = int(curve.curve.a())
    b = int(curve.curve.b())
    rhs = pow(x, 3) + a*x + b
    pmod = int(curve.curve.p())
    rhs = rhs % pmod
    assert(legendre(rhs, pmod) == 1)
    y = tonelli(rhs, pmod)
    return EC.PointJacobi(curve.curve, x, y, 1, n)

banner = re.recvuntil(b'!!!\n')
print(banner)
X = eval(re.recvline().strip().decode())
ct = bytes.fromhex(re.recvline().strip().decode())
print(X, ct)
Xs = []
ys = []
for i in tqdm(range(1000)):
    re.recvuntil(b'>>')
    re.sendline(b'1')
    re.recvuntil(b'>>')
    re.sendline(str(i).encode())
    x = getRand(i)
    Xs.append(x[0])
    yarr = []
    for j in range(12):
        re.recvuntil(b':')
        y = int(re.recvline().strip().decode())
        try:
            point = lift_x(y)
            point = decrypt(point)
            px = int(point.x())
            px = min(px, int(curve.curve.p() - px))
            assert(px < pow(10,12))
            yarr.append(int(px) / pow(10, 10))
        except Exception as e:
            assert(y < pow(10, 12))
            yarr.append(y / pow(10, 10))
    ys.append(np.array(yarr))
print(np.array(Xs))
print(np.array(ys))

model = Sequential()
model.add(Dense(2, activation='sigmoid'))
model.add(Dense(2, activation='relu'))
model.add(Dense(12, activation='linear'))
model.compile(loss='mse', optimizer='adam')
model.fit(np.array(Xs), np.array(ys), epochs = 16, batch_size = 1, verbose = 1)
key = model.predict(np.array([X]))
print(key)
key = "".join([str(int(abs(y_i) * 100)) for y_i in key[0]])
key = SHA256.new(key.encode()).digest()
print(xor(ct, key))