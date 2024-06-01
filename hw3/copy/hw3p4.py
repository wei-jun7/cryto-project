# -*- coding: utf-8 -*-
"""
Created on Thu Mar 28 01:13:53 2024

@author: zhonge
"""

import hw1a
import random




#https://www.geeksforgeeks.org/gcd-in-python/
def computeGCD(x, y):
 
    if x > y:
        small = y
    else:
        small = x
    for i in range(1, small + 1):
        if((x % i == 0) and (y % i == 0)):
            gcd = i
             
    return gcd

#Also got from gfg
def string_to_bits(string):
    return "".join(format(ord(i), '08b') for i in string)




def Encrypt_RSA(msg , public_key):
    e = public_key[0]
    N = public_key[1]
    c_arr = []
    for i in range(len(msg)):
        m_i = ord(msg[i])
        c_i = pow(m_i , e , N)
        c_arr.append(c_i)
    return c_arr

def Decrypt_RSA(c_arr , public_key , private_key):
    N = public_key[1]
    d = private_key[0]
    p = private_key[1]
    q = private_key[2]
    m_arr = []
    for c_i in c_arr:
        m_i = pow(c_i , d , N)
        m_arr.append(m_i)
    return m_arr

def Encrypt_semantic_secure_RSA(msg , SDES_key , public_key):
    e = public_key[0]
    N = public_key[1]
    r = random.randint(0 , 255)
    r_bits = bin(r)[2:]
    r_bits = "0" * (8 - len(r_bits)) + r_bits
    hash_value = hw1a.Encrypt_Simplified_DES(r_bits , SDES_key)
    print("random number is" , r)
    print("Hash value is" , hash_value)
    y1 = pow(r , e , N)
    c_arr = []
    for i in range(len(msg)):
        m_i = string_to_bits(msg[i]) #ascii value of msg[i]
        c_i = hw1a.XOR(m_i , hash_value)
        c_arr.append(c_i)
    y2 = c_arr
    return(y1 , y2)

def Decrypt_semantic_secure_RSA(ciphertext , SDES_key , public_key , private_key):
    y1 = ciphertext[0]
    y2 = ciphertext[1]
    N = public_key[1]
    d = private_key[0]
    p = private_key[1]
    q = private_key[2]
    r = pow(y1 , d , N)
    print("Decrypted random number is" , r)
    r_bits = bin(r)[2:]
    r_bits = "0" * (8 - len(r_bits)) + r_bits
    hash_value = hw1a.Encrypt_Simplified_DES(r_bits , SDES_key)
    plaintxt = []
    for letter in y2:
        plaintxt_i = hw1a.XOR(letter , hash_value)
        plaintxt.append(plaintxt_i)
    return plaintxt
 
#takes in a list of characters in binary string representation and returns an array of chars
#Example: ['01001110', '01000101', '01010100', '01010011', '01000001', '01000011'] -> 
#['N' , 'E' , 'T' , 'S' , 'A' , 'C']   
def bits_to_letters(char_bits_arr):
    char_arr = []
    for char_bits in char_bits_arr:
        dec_val = int(char_bits , 2)
        char_val = chr(dec_val)
        char_arr.append(char_val)
    return char_arr

#converts an array to decimal values to ascii
#Example: [78, 69, 84, 83, 65, 67] -> ['N' , 'E' , 'T' , 'S' , 'A' , 'C'] 
def dec_to_letters(dec_arr):
    char_arr = []
    for dec_val in dec_arr:
        char_val = chr(dec_val)
        char_arr.append(char_val)
    return char_arr
    
 
def main():
    print("---------------------part a---------------------------")
    N = 1211
    totient_N = 172 * 6
    e = random.randint(1 , totient_N)
    while(computeGCD(e , totient_N) != 1):
        e = random.randint(1 , totient_N)
    d = pow(e , -1 , totient_N)
    p = 173
    q = 7
    public_key = (e , N)
    private_key = (d , p , q)
    print("public key is" , public_key)
    print("private key is" , private_key)
    ciphertext = Encrypt_RSA("NETSAC", public_key)
    plaintext = Decrypt_RSA(ciphertext , public_key , private_key)
    plaintext_ascii = dec_to_letters(plaintext)
    print("ciphertext for classic RSA is" , ciphertext)
    print("Decrypted ciphertext for classic RSA is" , plaintext)
    print("Decrypted ciphertext for classic RSA in ascii is" , plaintext_ascii)
    print("---------------------part b---------------------------")
    sdes_key = "1100101101"
    print("key for SDES is" , sdes_key)
    N = 1211
    totient_N = 172 * 6
    e = random.randint(1 , totient_N)
    while(computeGCD(e , totient_N) != 1):
        e = random.randint(1 , totient_N)
    # print("e = " , e)
    d = pow(e , -1 , totient_N)
    p = 173
    q = 7
    public_key = (e , N)
    private_key = (d , p , q)
    print("public key is" , public_key)
    print("private key is" , private_key)
    ciphertext = Encrypt_semantic_secure_RSA("NETSAC" , sdes_key , public_key)
    print("ciphertext is" , ciphertext)
    ciphertext_ascii = bits_to_letters(ciphertext[1])
    print("ciphertext in ascii is" , ciphertext_ascii)
    plaintext_bits = Decrypt_semantic_secure_RSA(ciphertext, sdes_key, public_key, private_key)
    print("plaintext bits are" , plaintext_bits)
    plaintext = bits_to_letters(plaintext_bits)
    print("plaintext in ascii is" , plaintext)
    
    #-----------------------run 2------------------------------------
    print("-------------------------------------run 2 ---------------------------------")
    ciphertext = Encrypt_semantic_secure_RSA("NETSAC" , sdes_key , public_key)
    print("ciphertext is" , ciphertext)
    ciphertext_ascii = bits_to_letters(ciphertext[1])
    print("ciphertext in ascii is" , ciphertext_ascii)
    plaintext_bits = Decrypt_semantic_secure_RSA(ciphertext, sdes_key, public_key, private_key)
    print("plaintext bits are" , plaintext_bits)
    plaintext = bits_to_letters(plaintext_bits)
    print("plaintext in ascii is" , plaintext)

random.seed(0)     
main()