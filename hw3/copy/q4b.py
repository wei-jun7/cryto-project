from utils2 import *
import random

def mod_helper(x,y,z):
    #x^y mod z
    if(y==1):
        return (x%z)
    return (((x%z) * mod_helper(x,y-1,z)) % z)

def mod_inverse(a, m) : 
    a = a % m
    for x in range(1, m) : 
        if ((a * x) % m == 1) : 
            return x 
    return 1

def xor(str1, str2):
    # Convert the binary strings to integers, perform XOR, and then convert back to binary string
    result = bin(int(str1, 2) ^ int(str2, 2))[2:].zfill(8)  # [2:] to remove the '0b' prefix, zfill to ensure 8 bits
    
    return result


#----------------------------------------------------------------------
p = 173
q = 7
e = 7
n = p*q
o_n = (p-1)*(q-1)
d = mod_inverse(e,o_n)

r = int(random.random()*256)

DES_key_1 = bin(int(random.random()*1024))[2:].zfill(10)
DES_key_2 = bin(int(random.random()*1024))[2:].zfill(10)

KU = (e,n)
KR = (d,p,q)
M = ['01001110','01000101','01010100','01010011','01000101','01000011']

#----------------------------------------------------------------------
#encrypt
r_s = bin(r)[2:].zfill(8)

#first round
y1 = mod_helper(r,KU[0],KU[1])
y2_1 = []
r_hash_1 = encrypt(r_s,DES_key_1)
for i in M:
    y2_1.append(xor(i,r_hash_1))

#second round
y2_2 = []
r_hash_2 = encrypt(r_s,DES_key_2)
for i in y2_1:
    y2_2.append(xor(i,r_hash_2))

#final encrypted message
send = (y1,y2_2)
print(send)

#----------------------------------------------------------------------
#decrypt
r = mod_helper(send[0],KR[0],KR[1]*KR[2])
r_s = bin(r)[2:].zfill(8)

#first round
D_1 = []
r_hash_2 = encrypt(r_s,DES_key_2)
for i in send[1]:
    D_1.append(xor(i,r_hash_2))

#second round
D_2 = []
r_hash_1 = encrypt(r_s,DES_key_1)
for i in D_1:
    D_2.append(xor(i,r_hash_1))


print(D_2)
print(M)




