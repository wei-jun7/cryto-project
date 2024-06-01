# -*- coding: utf-8 -*-
"""
Created on Wed Mar 27 16:06:58 2024

@author: zhonge
"""
import math

#Also got from gfg
def string_to_bits(string):
    return "".join(format(ord(i), '08b') for i in string)



#copied extended euclidean algorith from gfg since already did that by hand in hw2.
#https://www.geeksforgeeks.org/python-program-for-basic-and-extended-euclidean-algorithms-2/
def gcdExtended(a, b): 
    # Base Case 
    if a == 0 : 
        return b,0,1
             
    gcd,x1,y1 = gcdExtended(b%a, a) 
     
    # Update x and y using results of recursive 
    # call 
    x = y1 - (b//a) * x1 
    y = x1 
     
    return gcd,x,y 


#xor function from hw1a
def XOR(str1 , str2):
    #pad the shorter string with 0s in front if they are different length
    if len(str1) <= len(str2):
        short_str = str1
        long_str = str2
    else:
        short_str = str2
        long_str = str1
    length_diff = len(long_str) - len(short_str)
    str1 = '0' * length_diff + short_str
    str2 = long_str
    assert(len(str1) == len(str2))
    output = []
    for i in range(len(str1)):
        if str1[i] == str2[i]:
            output.append('0')
        else:
            output.append('1')
    return "".join(output)

p = 499
q = 547
a , b = gcdExtended(p , q)[1:]
x0 = 159201 #quadratic residue
n = p * q
k = math.floor(math.log(n , 2))
h = math.floor(math.log(k , 2))
x_arr = [] #populate with x1, x2 ... x_t

#m_arr and p_arr for debugging
m_arr = []
p_arr = []
c_arr = []
stringbits = string_to_bits("NETSEC")
print("string as bits are" , stringbits)
for ptxt_index , i in zip(range(0 , len(stringbits) , h) , range(len(stringbits))) :
    m_i = stringbits[ptxt_index :ptxt_index +h]
    m_arr.append(m_i)
    if i == 0:
        x_i = x0**2 % n
    else:
        x_i = x_arr[-1]**2 % n
    x_arr.append(x_i)
    p_i = bin(x_arr[i])[-h:]
    p_arr.append(p_i)
    c_i = XOR(p_i , m_i)
    c_arr.append(c_i)
x_key = x_arr[-1]**2 % n

ciphertext = (c_arr , x_key) #[c_1 ... c_t] , x_t + 1


#---------------------------- DECRYPTION------------------------------------------------

t = len(m_arr)
d1 = pow((p+1) // 4 , t + 1 , p - 1) #(int) (((p + 1) / 4)**(t + 1)) %  (p - 1)
d2 = pow((q + 1) // 4 , t + 1 , q -  1) #(int) (((q + 1) / 4)**(t + 1)) % (q - 1)
u = pow(x_key , d1 , p)
v = pow(x_key , d2 , q)
x_0 = (v * a * p + u * b * q) % n
print("x0 is" , x0)
print("x_0 for decryption is" , x_0)

m_arr2 = []
x_arr2 = []
for i in range(len(c_arr)):
    if i == 0:
        x_i = pow(x_0 , 2 , n)
    else:
        x_i = pow(x_arr2[-1] , 2 , n)
    x_arr2.append(x_i)
    p_i = bin(x_arr2[i])[-h:]
    m_i = XOR(p_i , c_arr[i])
    m_arr2.append(m_i)
Decrypted_bits = "".join(m_arr2)
print("decrypted bits are" , Decrypted_bits)
assert(Decrypted_bits == stringbits)