from sympy import lcm, mod_inverse

p = 293
q = 433
n = p * q
g = 6497955158
mu = 53022
lamb = lcm(p-1, q-1)


r = [35145, 74384, 10966, 17953, 7292]


def encrypt(m, r, n, g):
    return pow(g, m, n**2) * pow(r, n, n**2) % n**2


def decrypt(c, n, lamb, mu):
    l = (pow(c, lamb, n**2) - 1) // n
    return (l * mu) % n

m = 1
ciphers = []


for i in range(4):
    ci = encrypt(m, r[i], n, g)
    ciphers.append(ci)
    print(f"Step {i+1}, r = {r[i]}, Encrypted Counter: {ci}")


print("ciphers: ", ciphers)
final_cipher = 1
for cipher in ciphers:
    final_cipher = (final_cipher * cipher) % (n**2)

    
lamb = int(lamb)
decrypted_m = decrypt(final_cipher, n, lamb, mu)
print(f"Decrypted final counter value: {decrypted_m}")


inverse_ciphers = []
for i in range(4):
    inverse_ci = pow(ciphers[i], -1, n**2)  # 计算逆元
    inverse_ciphers.append(inverse_ci)


final_decipher = final_cipher
for inv_cipher in inverse_ciphers:
    final_decipher = (final_decipher * inv_cipher) % (n**2)


decrypted_final = decrypt(final_decipher, n, lamb, mu)
print(f"Decrypted final counter after decrement: {decrypted_final}")



print("Incrementing cryptocounter:")
c_i = 1
print("Incrementing cryptocounter:")
c_i = encrypt(1, r[0], n, g)  
print("c_1 =", c_i)
for i in range(1, len(r)):
    c_i = (c_i * encrypt(1, r[i], n, g)) % (n**2)  
    print(f"c_{i+1} =", c_i)

    
print()   
print("\nDecrementing cryptocounter:")
print(f"c_{len(r)} =", c_i)
for i in range(len(r) - 1, -1, -1):
    tmp = encrypt(1, r[i], n, g) 
    tmp = pow(tmp, -1, n**2)  
    c_i = (c_i * tmp) % n**2
    print(f"c_{i} =", c_i)
