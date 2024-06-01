# Given
q = 257
a = 0
b = -4
G = (2, 2)
NB = 101
Pm = (112, 26)
k = 41

#----------------------------------------------------------------------
def mod_inverse(a, m) : 
    a = a % m
    for x in range(1, m) : 
        if ((a * x) % m == 1) : 
            return x 
    return 1

#----------------------------------------------------------------------
# Point addition
def point_add(P, Q):
    if P == (0, 0):
        return Q
    if Q == (0, 0):
        return P
    if P[0] == Q[0] and P[1] != Q[1]:
        return (0, 0)  # P + (-P) = O
    if P == Q:
        lam = (((3 * P[0]**2 + a) % q) * (mod_inverse(2 * P[1], q) % q) % q)
    else:
        lam = (((Q[1] - P[1]) % q) * (mod_inverse(Q[0] - P[0], q) % q) % q)
    x3 = (lam**2 - P[0] - Q[0]) % q
    y3 = (lam * (P[0] - x3) - P[1]) % q
    return (x3, y3)

#----------------------------------------------------------------------
# Scalar multiplication
def scalar_mult(k, P):
    result = (0,0)
    for i in range(k):
        result = point_add(result,P)
    return result


#----------------------------------------------------------------------
# Compute Bob's public key PB
PB = scalar_mult(NB, G)

#----------------------------------------------------------------------
# encrypt
# Compute ciphertext (C1, C2)
C1 = scalar_mult(k, G)
C2 = point_add(Pm, scalar_mult(k, PB))
send = (C1,C2)
print(send)

#----------------------------------------------------------------------
# decrypt
# Compute D = NB * C1
D = scalar_mult(NB, send[0])
# Compute original message point Pm' = C2 - D
M_new = point_add(send[1], (D[0], -D[1]))

print(M_new)
print(Pm)
