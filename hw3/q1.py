# define the parameters
p = 257
a = 0
b = -4
G = (2, 2)
NB = 101
Pm = (112, 26)
k = 41
# part 1 find the ciphertext 
# ecc addition function
def ecc_add(P, Q, p):
    if P == (0, 0):
        return Q
    if Q == (0, 0):
        return P
    if P[0] == Q[0] and (P[1] != Q[1] or P[1] == 0):
        return (0, 0) 
    if P == Q:
        lam = (3 * P[0]**2 + a) * pow(2 * P[1], -1, p) % p
    else:
        lam = (Q[1] - P[1]) * pow(Q[0] - P[0], -1, p) % p
    x3 = (lam**2 - P[0] - Q[0]) % p
    y3 = (lam * (P[0] - x3) - P[1]) % p
    return (x3, y3)

# ecc multiplication function
def ecc_mul(P, k, p):
    R = (0, 0)  # R is the point of infinity
    while k > 0:
        if k & 1:
            R = ecc_add(R, P, p)
        P = ecc_add(P, P, p)
        k >>= 1
    return R

# calculate the ciphertext1 and ciphertext2
C1 = ecc_mul(G, k, p)
NBG = ecc_mul(G, NB, p)
kNBG = ecc_mul(NBG, k, p)
C2 = ecc_add(Pm, kNBG, p)

print("C1: ", C1 , " C2:{f}" ,C2)
#part2 Decrypt the ciphertext

# 1. calculate N_B * C1
NBC1 = ecc_mul(C1, NB, p)

# 2. find NBC1 inverse
NBC1_inv = (NBC1[0], p - NBC1[1])

# 3. let the inverse point add with  C2 and get the plaintext
Pm_recovered = ecc_add(C2, NBC1_inv, p)

print("Plaintext is ", Pm_recovered)

