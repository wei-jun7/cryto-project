# -*- coding: utf-8 -*-
"""
Created on Sun Apr 14 15:38:25 2024

@author: zhonge
"""
import DES
import hashfunctions

def hash_encrypt_triple_SDES(plaintxt , key):
    hash_val = hashfunctions.hmac(plaintxt , key)
    bundled_plaintxt = plaintxt + " " + hash_val
    ciphertxt = DES.encode_triple_SDES(bundled_plaintxt , key)
    return ciphertxt

def hash_decrypt_triple_SDES(ciphertxt , key):
    data = DES.decode_triple_SDES(ciphertxt , key)
    parts = data.split(' ')
    plaintxt = " ".join(parts[:-1])
    received_hashval = parts[-1]
    reconstructed_hashval = hashfunctions.hmac(plaintxt , key)
    # print("plaintxt is" , plaintxt)
    # print("received_hashval is" , received_hashval)
    # print("reconstructed_hashval is" , reconstructed_hashval)
    return plaintxt , received_hashval , reconstructed_hashval