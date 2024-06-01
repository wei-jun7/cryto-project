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


#----------------------------------------------------------------------
p = 173
q = 7
e = 7
n = p*q
o_n = (p-1)*(q-1)
d = mod_inverse(e,o_n)

KU = (e,n)
KR = (d,p,q)
M = [78,69,84,83,69,67]

#----------------------------------------------------------------------
#encrypt
C = []
for i in M:
    C.append(mod_helper(i,KU[0],KU[1]))

print(C)

#----------------------------------------------------------------------
#decrypt
D = []
for i in C:
    D.append(mod_helper(i,KR[0],KR[1]*KR[2]))

print(D)
print(M)




