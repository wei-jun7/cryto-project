def extended_gcd(a, b):
    # Extended Euclidean Algorithm
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = extended_gcd(b % a, a)
        return (g, x - (b // a) * y, y)

def mod_exp(base, exponent, modulus):
    # Modular exponentiation
    result = 1
    while exponent > 0:
        if exponent % 2 == 1:
            result = (result * base) % modulus
        exponent = exponent >> 1
        base = (base * base) % modulus
    return result

def xor(a, b):
    # XOR operation for binary strings
    a, b = a.zfill(max(len(a), len(b))), b.zfill(max(len(a), len(b)))
    return ''.join(str(int(x) ^ int(y)) for x, y in zip(a, b))

def split_m(m, count):
    # Split the binary message into chunks
    return [m[i:i+count] for i in range(0, len(m), count)]

def encrypt(m, p, q, x0):
    n = p * q
    m_split = split_m(m, 4)
    t = len(m_split)
    x = [x0]
    c = []

    for i in range(t):
        xi = mod_exp(x[i], 2, n)
        x.append(xi)
        pi = bin(xi)[2:].zfill(4)[-4:]
        ci = xor(m_split[i], pi)
        c.append(ci)
    xt1 = mod_exp(x[-1], 2, n)

    return (''.join(c), xt1)

def decrypt(ciphertext, xt1, p, q, t):
    n = p * q
    d1 = mod_exp((p+1)//4, t+1, p-1)
    d2 = mod_exp((q+1)//4, t+1, q-1)
    u = mod_exp(xt1, d1, p)
    v = mod_exp(xt1, d2, q)

    # Compute x0 using Chinese Remainder Theorem
    a, b = extended_gcd(p, q)[1:3]
    x0 = (v*a*p + u*b*q) % n

    x = [x0]
    m_n = []

    for i in range(t):
        xi = mod_exp(x[i], 2, n)
        x.append(xi)
        pi = bin(xi)[2:].zfill(4)[-4:]
        mi = xor(pi, ciphertext[4*i:4*(i+1)])
        m_n.append(mi)

    message_binary = ''.join(m_n)
    message_text = ''.join(chr(int(message_binary[i:i+8], 2)) for i in range(0, len(message_binary), 8))

    return message_text
#data initalization
p = 499
q = 547
x0 = 159201
m = '010011100100010101010100010100110100010101000011'  # Binary of M = {NETSEC}
# Encrypting
ciphertext, xt1 = encrypt(m, p, q, x0)
print(f'Ciphertext: {ciphertext}, Last X: {xt1}')

# Decrypting
original_message_text = decrypt(ciphertext, xt1, p, q, len(m)//4)
print(f'Original Message Text: {original_message_text}')


