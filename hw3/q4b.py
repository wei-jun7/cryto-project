# b. Semantically secure RSA: using your simplified DES to create Hash values, and random numbers,
# b1. encrypt the message M = {NETSEC} twice
# b2. Decrypt each ciphertext.
# Show your work. Include your hash values, random variables etc.

import hw1 as DES
import random
from sympy import mod_inverse

def bits_to_letters(char_bits_arr):
    char_arr = []
    for char_bits in char_bits_arr:
        # print("char_bits_for_letter_word: ", char_bits)
        dec_val = int(char_bits , 2)
        char_val = chr(dec_val)
        char_arr.append(char_val)
    return char_arr

def string_to_bits_with_spaces(string):
    return " ".join(format(ord(i), '08b') for i in string) + " "


def computeGCD(x, y):
    while(y):
        x, y = y, x % y
    return x

def Encrypt_semantic_secure_RSA(msg, DES_key, public_key, ip, ip_inv):
    e, n = public_key
    random_number = random.randint(1, n-1)
    r_encrypted = pow(random_number, e, n)
    r_bit = format(random_number, '08b')
    hash_value = DES.s_des_encrypt(r_bit, DES_key[0], DES_key[1], ip, ip_inv)
    print("hash_value: ", hash_value)
    print("r_bit_en",r_bit)
    encrypted_msg = ''
    for char in msg.split(' '): 
        encrypted_char = DES.xor(char, hash_value)
        encrypted_msg += encrypted_char + ' '

    return r_encrypted, encrypted_msg.strip()


def Decrypt_semantic_secure_RSA(encrypted_data, DES_key, private_key, ip, ip_inv):
    r_encrypted, encrypted_msg = encrypted_data
    d, q, p = private_key
    
    r_decrypted = pow(r_encrypted, d, q*p)
    
    r_bits = format(r_decrypted, '08b')
    print("r_bit_de",r_bits) 

    
    hash_value = DES.s_des_encrypt(r_bits, DES_key[0], DES_key[1], ip, ip_inv)
    decrypted_msg = ''
    for encrypted_char in encrypted_msg.split(' '):  
        decrypted_char_bits = DES.xor(encrypted_char, hash_value)
        decrypted_char = chr(int(decrypted_char_bits, 2))
        decrypted_msg += decrypted_char
    
    return decrypted_msg


random.seed(0) 

#initialization the RSA data
p = 173
q = 7
N = p * q  # RSA modulus
e = 7  # Public exponent
phi_N = (p - 1) * (q - 1)  # Euler's totient function of N
message = "NETSEC"
# Calculate the private key 'd' using modular inverse


d = mod_inverse(e, phi_N)
pb_key = (e, N)
pv_key = (d, q, p)
print("Public key: ", pb_key)
print("Private key: ", pv_key)

#use the random value to generate the hash value and se 

#initialization the DES data
p10 = [3, 5, 2, 7, 4, 10, 1, 9, 8, 6]
p8 = [6, 3, 7, 4, 8, 5, 10, 9]
ip = [2, 6, 3, 1, 4, 8, 5, 7]
ip_inv = [4, 1, 3, 5, 7, 2, 8, 6]
key = "1100011110" 
key1, key2 = DES.key_generation(p10, p8, key)
binary_message = DES.convert_to_binary(message)
print("Original message: ", bits_to_letters(binary_message.strip().split(' ')))
print("binary_message: ", binary_message)
print("_____________________________test run 1 encryption and decryto___________________________________")
ciphertext1= Encrypt_semantic_secure_RSA(binary_message, (key1, key2), pb_key, ip, ip_inv)
print("Encrypted message1: ", ciphertext1)
print("ciphertext1 to ascii: ", bits_to_letters(ciphertext1[1].split(' ')))
ciphertext2 = Encrypt_semantic_secure_RSA(ciphertext1[1], (key1, key2), pb_key, ip, ip_inv)
print("Encrypted message2: ", ciphertext2)
print("ciphertext2 to ascii: ", bits_to_letters(ciphertext2[1].split(' ')))
decryto1 = Decrypt_semantic_secure_RSA(ciphertext2, (key1, key2), pv_key, ip, ip_inv)
print("Decrypted message1: ", decryto1)
print("Decrypted message1 to binary: ", string_to_bits_with_spaces(decryto1))
decryto2 = Decrypt_semantic_secure_RSA((ciphertext1[0], ciphertext1[1]), (key1, key2), pv_key, ip, ip_inv)
print("Decrypted message2: ", decryto2)
print("Decrypted message2 to binary: ", string_to_bits_with_spaces(decryto2))
print("Original message: ", binary_message.strip())



