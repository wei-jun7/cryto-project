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

def generate_keypair(bits=2048):

    p = nextprime(random.getrandbits(bits // 2))
    q = nextprime(random.getrandbits(bits // 2))
    n = p * q
    phi = (p - 1) * (q - 1)

    e = 65537
    while gcd(phi, e) != 1:
        e += 2

    d = modinv(e, phi)
    return ((e, n), (d, n))

def xor_bytes(a, b):
    return bytes(x ^ y for x, y in zip(a, b))

def mgf1(input_str, length, hash_func=hashlib.sha256):
    counter = 0
    output = b''
    while len(output) < length:
        C = input_str + counter.to_bytes(4, byteorder='big')
        output += hash_func(C).digest()
        counter += 1
    return output[:length]

def oaep_encode(message, n, hash_func=hashlib.sha256):
    k = n.bit_length() // 8
    hlen = hash_func().digest_size
    message = message.encode()

    if len(message) > k - 2 * hlen - 2:
        raise ValueError("Message too long.")

    l_hash = hash_func(b'').digest()
    ps = b'\x00' * (k - len(message) - 2 * hlen - 2)
    db = l_hash + ps + b'\x01' + message
    seed = os.urandom(hlen)
    db_mask = mgf1(seed, k - hlen - 1, hash_func)
    masked_db = xor_bytes(db, db_mask)
    seed_mask = mgf1(masked_db, hlen, hash_func)
    masked_seed = xor_bytes(seed, seed_mask)

    return b'\x00' + masked_seed + masked_db

def oaep_decode(encoded, n, hash_func=hashlib.sha256):
    k = n.bit_length() // 8
    hlen = hash_func().digest_size

    _, masked_seed, masked_db = encoded[0], encoded[1:1+hlen], encoded[1+hlen:]
    seed_mask = mgf1(masked_db, hlen, hash_func)
    seed = xor_bytes(masked_seed, seed_mask)
    db_mask = mgf1(seed, k - hlen - 1, hash_func)
    db = xor_bytes(masked_db, db_mask)
    l_hash = hash_func(b'').digest()

    l_hash_prime = db[:hlen]
    if l_hash_prime != l_hash:
        raise ValueError("Decoding error")

    separator = db.find(b'\x01', hlen)
    if separator < 0:
        raise ValueError("Decoding error")

    message = db[separator+1:].decode()
    return message

# Example usage
public, private = generate_keypair(2048)
message = '1111111111'
encoded_message = oaep_encode(message, private[1])
encrypted_msg = [pow(m, public[0], public[1]) for m in encoded_message]
print("encrypted message len is" , len(encrypted_msg))
# print("Encoded message", encrypted_msg)
decrypted_encoded_msg = [pow(c, private[0], private[1]) for c in encrypted_msg]
decrypted_msg = oaep_decode(bytes(decrypted_encoded_msg), private[1])
print('Decrypted:', decrypted_msg)
