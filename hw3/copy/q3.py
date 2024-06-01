
#----------------------------------------------------------------------
def xor(a, b):
    
    a, b = a.zfill(4), b.zfill(4)
    
    result = ""
    for i in range(4):  # Loop over each bit
        # XOR each bit and add to the result string
        result += str(int(a[i]) ^ int(b[i]))
    return result

#----------------------------------------------------------------------
def mod_helper(x,y,z):
    #x^y mod z
    if(y==1):
        return (x%z)
    return (((x%z) * mod_helper(x,y-1,z)) % z)

#----------------------------------------------------------------------
def split_m(m,count):
    a=1
    b=''
    c=[]
    for i in range(len(m)):
        if ((a<count) and (i < len(m)-1)):
            a+=1
            b+=m[i]
        else:
            a=1
            b+=m[i]
            c.append(b)
            b=''
    return c

#----------------------------------------------------------------------
#given condition
p=499
q=547
a=-57
b=52
x0=159201
# binary of M = {NETSEC}
m = '010011100100010101010100010100110100010101000011'
m_split = split_m(m,4)
t = len(m_split)

n = p * q

#----------------------------------------------------------------------
#encrypt
x = []
x.append(x0)

c = []

for i in range(t):
    xi = (x[i] **2) % n
    x.append(xi)
    pi = bin(xi & 15)[2:].zfill(4)
    ci = xor(m_split[i],pi)
    c.append(ci)
xt1 = (x[len(x)-1] **2) % n

send = (c,xt1)
print(send)

#----------------------------------------------------------------------
#decrypt
c = send[0]
xt1 = send[1]

d1 = (int((p+1)/4)**(t+1)) % (p-1)
d2 = (int((q+1)/4)**(t+1)) % (q-1)
u = mod_helper(xt1,d1,p)
v = mod_helper(xt1,d2,q)
x0 = ((v*a*p) + (u*b*q)) % n

x = []
x.append(x0)

m_n = []

for i in range(t):
    xi = (x[i] **2) % n
    x.append(xi)
    pi = bin(xi & 15)[2:].zfill(4)
    mi = xor(pi,c[i])
    m_n.append(mi)

print(m_split)
print(m_n)




