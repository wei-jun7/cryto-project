# -*- coding: utf-8 -*-
"""
Created on Thu Jan 18 18:25:31 2024

@author: zhonge
"""
from collections import deque

#permutes a string based on a order (list)
def permutation(string , perm_order):
    txt = list(string)
    perm_txt = [""] * len(perm_order)
    for i in range(len(perm_order)):
        perm_txt[i] = txt[perm_order[i] - 1]
    return ''.join(perm_txt)

#takes in a binary string and splits it
#even bits to left, odd bits to right, bits are 1-8
def split(txt):
    assert(len(txt) == 8)
    L = []
    R = []
    for i in range(len(txt)):
        if i % 2 == 0:
            R.append(txt[i])
        else:
            L.append(txt[i])
    return "".join(L) , "".join(R)

#does a circular shift of all characters in string by n elements
def left_shift(string , n = 1):
     d = deque(string)
     d.rotate(-n) #negative rotates to the left
     return "".join(d)
    
 
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

def generate_round_keys(key):
    assert(len(key) == 10)
    P10 = [3 , 5 , 2 , 7 , 4 , 10 , 1 , 9 , 8 , 6]
    scrambled_key = permutation(key , P10)
    L0 = scrambled_key[:5]
    R0 = scrambled_key[5:]
    L0_shift = left_shift(L0);
    R0_shift = left_shift(R0);
    K1_unscrambled = L0_shift + R0_shift
    P8 = [6 , 3 , 7 , 4 , 8 , 5 , 10 , 9]
    K1 = permutation(K1_unscrambled , P8)
    L1_shift = left_shift(L0_shift , 2)
    R1_shift = left_shift(R0_shift , 2)
    K2_unscrambled = L1_shift + R1_shift
    K2 = permutation(K2_unscrambled , P8)
    return K1 , K2

#computes S(b) where b is a 4 bit binary number (string)
#returns the binary string eg Sbox(S , '1000') = '10'
def Sbox(S , b):
    assert(len(b) == 4)
    row = int(b[0] + b[3] , 2)
    col = int(b[1] + b[2] , 2)
    output = bin(S[row][col])[2:] #bin returns 0b#, eg 0b11, and we strip the 0b
    if(len(output) == 1):
        output = '0' + output
    assert(len(output) == 2)
    return output

#takes in 4 bit txt and 8 bit key and returns 4 bits
def F(txt , key):
    P = [4 , 1 , 2 , 3 , 2 , 3 , 4 , 1]
    txt = permutation(txt , P)
    txt = XOR(txt , key)
    L = txt[:4]
    R = txt[4:]
    #do substitution boxes now
    s0 = [[1 , 0 , 3 , 2] , [3 , 2 , 1 , 0] , [0 , 2 , 1 , 3] , [3 , 1 , 3 , 2]]
    s1 = [[0 , 1 , 2 , 3] , [2 , 0 , 1 , 3] , [3 , 0 , 1 , 0] , [2 , 1 , 0 , 3]]
    txt = Sbox(s0 , L) + Sbox(s1 , R)
    P4 = [2 , 4 , 3 , 1]
    txt = permutation(txt , P4)
    return txt;
    
#takes in 8 bits
def Encrypt_Simplified_DES(plaintext , key):
    K1 , K2 = generate_round_keys(key)
    assert(len(plaintext) == 8)
    initial_perm = [2 , 6 , 3 , 1 , 4 , 8 , 5  , 7]
    txt = permutation(plaintext , initial_perm)
    L0 = txt[:4]
    R0 = txt[4:]
    L1 = R0
    R1 = XOR(L0 , F(R0 , K1))
    L2 = R1
    R2 = XOR(L1 , F(R1 , K2))
    #swap left and right since it is end of rounds according to feistel structure
    L = R2
    R = L2
    inv_initial_perm = [4 , 1 , 3 , 5 , 7 , 2 , 8 , 6]
    ciphertxt = permutation(L + R , inv_initial_perm)
    return ciphertxt

def Decrypt_Simplified_DES(ciphertext , key):
    K1 , K2 = generate_round_keys(key)
    initial_perm = [2 , 6 , 3 , 1 , 4 , 8 , 5  , 7]
    inv_initial_perm = [4 , 1 , 3 , 5 , 7 , 2 , 8 , 6]
    txt = permutation(ciphertext , initial_perm)
    L2 = txt[:4]
    R2 = txt[4:]
    L1 = XOR(F(R2 , K2) , L2)
    R1 = R2
    L0 = XOR(F(L1 , K1) , R1)
    R0 = L1
    plaintxt = permutation(L0 + R0 , inv_initial_perm)
    return plaintxt
    
#takes in a char like 'c' and displays the 8 bit binary ascii representation for it
#eg input 'c' output '01100011'
def letter_to_bin(char):
    txt = bin(ord(char))[2:]
    assert(len(txt) <= 8)
    if len(txt) < 8:
        difference = 8 - len(txt)
        txt = "0" * difference + txt
    return txt

#eg input '01100011' output 'c'
def bin_to_letter(bin_num):
    ascii_num = int(bin_num , 2)
    return chr(ascii_num)

#takes in a message like "crypto" and outputs the ciphertxt using simplified DES
def encode_msg(plaintxt , key):
    txt = plaintxt.replace(" " , "") #remove all whitespace
    byte_encoding = []
    for i in range(len(txt)):
        bin_letter = letter_to_bin(txt[i])
        byte_encoding.append(Encrypt_Simplified_DES(bin_letter , key))
    return " ".join(byte_encoding)

def decode_msg(ciphertxt , key):
    encoded_letters = ciphertxt.split()
    decoded_letters = []
    for encoded_letter in encoded_letters:
        bin_decoded_letter = Decrypt_Simplified_DES(encoded_letter , key)
        decoded_letter = bin_to_letter(bin_decoded_letter)
        decoded_letters.append(decoded_letter)
    return "".join(decoded_letters)

#3 TA tests
if __name__ == "__main__":
    assert(Encrypt_Simplified_DES("00101000" , "1100011110") == "10001010")
    assert(Encrypt_Simplified_DES("00010010" , "1111100001") == "01110001")
    assert(Encrypt_Simplified_DES("11001110" , "0011010110") == "00110000")
    #test from hw
    assert(Encrypt_Simplified_DES("00101000" , "1100011110") == "10001010")
    assert(Decrypt_Simplified_DES("10001010" , "1100011110") == "00101000")
    #print(generate_round_keys("1010000010"))
    
    plaintxt = "crypto"
    key = "1100011110"
    
    ciphertxt = encode_msg(plaintxt , key)
    print("plaintext is" , plaintxt)
    print("Encoded message is" , ciphertxt)
    decrypted_txt = decode_msg(ciphertxt , key)
    print("decrypted message is" , decrypted_txt)
    
    #some fun stuff
    ciphertxt2 = encode_msg("Hello agent bob, you have a top secret mission." , "1001100001")
    decrypted_txt = decode_msg(ciphertxt2 , "1001100001")


    
