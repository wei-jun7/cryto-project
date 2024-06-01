import math

#public key
n = 38009
#mod n
e = 7
print("The square root of n:" , math.sqrt(n))  #194.95897004241687

c = 193
for i in range(c, c-40, -2):
    print("Prime number", i, ", n % i :", n%i)

p = 191
q = n / p
print("p:", p,", q:", q,", n:", n,", p*q:", p*q, ", n-p*q:", n - p*q)

phin = (p-1) * (q-1)
print("p:", p,", q:", q,", n:", n,", phin:", phin)


#(d * e) mod phin = 1
d = pow(e, -1, int(phin))
#d = gmpy.invert(e, phin)
print("d:", d,", e:", e, ", d*e % phin: ", int(d*e %phin))

#Assume message = 5
message = 5
txt = 1
while e > 0:
    txt *= message
    txt %= n
    e -= 1
print("Encrption of message:", txt)


cipher = txt
decipher_num = 1
while d > 0:
    decipher_num *= cipher
    decipher_num %= n
    d -= 1
print("Decryption of message:",decipher_num)