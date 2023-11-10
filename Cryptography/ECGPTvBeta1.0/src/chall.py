from libnum import *
import numpy as np
import ecdsa
from pwn import xor
from Crypto.Hash import SHA256
from ecdsa import ellipticcurve as EC
from secret import d, FLAG
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense

model = Sequential()
model.add(Dense(2, activation='sigmoid'))
model.add(Dense(2, activation='relu'))
model.add(Dense(12, activation='linear'))

curve = ecdsa.curves.NIST256p
n = curve.order

def getRand(seed=None):
    if seed != None:
        np.random.seed(seed)
    return np.random.random((1, 4))

def getVec(seed=None):
    X = getRand(seed)
    y = model.predict(X, verbose=0)
    return X, y

def unFloat(num):
    return int(num * (pow(10, 10)))

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
    

def encrypt(message: EC.PointJacobi)-> EC.PointJacobi:
    return message * 420 * pow(d, 69, n)
    
def decrypt(message: EC.PointJacobi)-> EC.PointJacobi:
    return message * 69 * pow(d, 420, n)

def server():
    X1, y1 = getVec()
    X2, y2 = getVec()
    try:
        assert(X1[0][0] != X2[0][0])
        assert(y1[0][0] != y2[0][0]) 
    except:
        print("Model is broken, please try again!!!")
        exit(0)
    print("Welcome!!!")
    X, y = getVec()
    print(X[0].tolist())
    key = "".join([str(int(abs(y_i) * 100)) for y_i in y[0]])
    key = SHA256.new(key.encode()).digest()
    print(xor(FLAG, key).hex())
    
    for _ in range(1000):
        print("Nani ka naaa~~")
        print("[1] Encrypt")
        print("[2] Nyerah")
        print("[3] Exit")
        choice = int(input(">> "))
        
        if choice == 1:
            print("Seed?")
            seed = int(input(">> "))
            X, y = getVec(seed)
            for i, y_i in enumerate(y[0]):
                y_i = unFloat(y_i)
                try:
                    message = lift_x(y_i)
                    ct = encrypt(message)
                    if (decrypt(ct).x() != message.x()):
                        print("Sorry, seems like chall is broken")
                        exit(0)
                    print(f"y1_{i}: {ct.x()}")
                except Exception as e:
                    print(f"y2_{i}: {y_i}")
        elif choice == 2:
            np.random.seed(np.random.randint(1, 1e2))
            print("Jangan nyerah bang dikit lagi")
        elif choice == 3:
            exit(0)
        else:
            print("Sumimasen wakaranai")
            
        if _ % 32 == 0:
            np.random.seed(np.random.randint(1, 1e6))
    exit(0)


if __name__ == "__main__":
    server()
