import struct

def xor(str1, str2):
    # Convert the binary strings to integers, perform XOR, and then convert back to binary string
    result = bin(int(str1, 2) ^ int(str2, 2))[2:].zfill(8)  # [2:] to remove the '0b' prefix, zfill to ensure 8 bits
    
    return result

def left_rotate(n, b):
    return ((n << b) | (n >> (32 - b))) & 0xffffffff

def sha1(data):
    bytes = ""
    
    for n in range(len(data)):
        bytes += '{0:08b}'.format(ord(data[n]))
    bits = bytes + "1"
    pBits = bits
    while len(pBits) % 512 != 448:
        pBits += "0"
    pBits += '{0:064b}'.format(len(bits) - 1)
    
    h0 = 0x67452301
    h1 = 0xEFCDAB89
    h2 = 0x98BADCFE
    h3 = 0x10325476
    h4 = 0xC3D2E1F0
    
    for c in range(0, len(pBits), 512):
        words = []
        for i in range(0, 512, 32):
            words.append(int(pBits[c+i:c+i+32], 2))
        for i in range(16, 80):
            words.append(left_rotate(words[i-3] ^ words[i-8] ^ words[i-14] ^ words[i-16], 1))
        
        a = h0
        b = h1
        c = h2
        d = h3
        e = h4
        
        for i in range(0, 80):
            if 0 <= i <= 19:
                f = d ^ (b & (c ^ d))
                k = 0x5A827999
            elif 20 <= i <= 39:
                f = b ^ c ^ d
                k = 0x6ED9EBA1
            elif 40 <= i <= 59:
                f = (b & c) | (d & (b | c))
                k = 0x8F1BBCDC
            elif 60 <= i <= 79:
                f = b ^ c ^ d
                k = 0xCA62C1D6

            temp = left_rotate(a, 5) + f + e + k + words[i] & 0xffffffff
            e = d
            d = c
            c = left_rotate(b, 30)
            b = a
            a = temp
        
        h0 = h0 + a & 0xffffffff
        h1 = h1 + b & 0xffffffff
        h2 = h2 + c & 0xffffffff
        h3 = h3 + d & 0xffffffff
        h4 = h4 + e & 0xffffffff

    return '%08x%08x%08x%08x%08x' % (h0, h1, h2, h3, h4)