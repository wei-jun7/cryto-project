import hashlib
import os
import random
from sympy import nextprime

def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

def modinv(a, m):
    m0, x0, x1 = m, 0, 1
    if m == 1:
        return 0
    while a > 1:
        q = a // m
        m, a = a % m, m
        x0, x1 = x1 - q * x0, x0
    if x1 < 0:
        x1 += m0
    return x1

def generate_keypair(p, q):
    if p == q:
        raise ValueError('p and q cannot be equal')
    n = p * q
    phi = (p-1) * (q-1)

    e = 65537
    while gcd(phi, e) != 1:
        e += 2

    d = modinv(e, phi)
    return ((e, n), (d, n))

def encrypt(public_key, plaintext):
    key, n = public_key
    cipher = [pow(ord(char) , key , n) for char in plaintext]
    #cipher = [(ord(char) ** key) % n for char in plaintext]
    return cipher

#takes in a string 
def decrypt(private_key, ciphertext):
    key, n = private_key
    #plain = [chr((int(char) ** key) % n) for char in ciphertext]
    plain = [chr(pow(int(char) , key , n)) for char in ciphertext]
    return ''.join(plain)

# Example usage
p = nextprime(random.getrandbits(20// 2))
q = nextprime(random.getrandbits(30 // 2))
public, private = generate_keypair(p, q)
message = "100101001"
encrypted_msg = encrypt(public, message)
print('Encrypted:', encrypted_msg)
decrypted_msg = decrypt(private, encrypted_msg)
print('Decrypted:', decrypted_msg)
