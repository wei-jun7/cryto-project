import random
from math import gcd
from sympy import nextprime, mod_inverse

def lcm(x, y):
    return x * y // gcd(x, y)

def generate_keypair(bits=2048):

    p = nextprime(random.getrandbits(bits // 2))
    q = nextprime(random.getrandbits(bits // 2))
    if p == q:  
        raise ValueError("p and q should not be equal.")
    n = p * q
    nsquare = n * n
    lam = lcm(p-1, q-1)
    g = n + 1
    mu = mod_inverse((pow(g, lam, nsquare) - 1) // n, n)
    return ((n, g), (lam, mu))

#takes in an int m
def encrypt(public_key, m):
    
    n, g = public_key
    nsquare = n * n
    r = random.randint(1, n-1)
    while gcd(r, n) != 1:
        r = random.randint(1, n-1)  # 选择一个与n互质的随机数r
    c = (pow(g, m, nsquare) * pow(r, n, nsquare)) % nsquare
    return c

def decrypt(private_key, public_key, c):

    n, g = public_key
    lam, mu = private_key
    nsquare = n * n
    x = pow(c, lam, nsquare)
    l = (x - 1) // n
    m = (l * mu) % n
    return m

# 示例使用
public_key, private_key = generate_keypair(2048)  # use the 2048 bit  to generate the key
m = 1
c = encrypt(public_key, m)
print("Encrypted:", c)
m_dec = decrypt(private_key, public_key, c)
print("Decrypted:", m_dec)
