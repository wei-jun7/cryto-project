"""
HW01.b Crypto
Erwin Hitgano
RIN: 662001996
"""

def Sbox(S, n: int)-> int:
    n = f"{n:04b}"
    rowS0 = n[0] + n[3]
    colS0 = n[1] + n[2]
    rowS0 = int(rowS0, 2)
    colS0 = int(colS0, 2)
    ret0 = S[rowS0][colS0]
    return ret0

# Function that creates DDT. Takes in the S-box, the number of
# input bits, and the number of output bits.
def DDT(S, inputLen, outputLen):
    # Initialize the table
    table = [[0] * (2**outputLen) for i in range(2**inputLen)]
    
    # This array of sets houses the inputs that produce the outputs
    full = [[set() for j in range(2**outputLen)] for i in range(2**inputLen)]
    
    # Populate DDT
    for i in range(0, 2**inputLen, 1):
        for j in range(0,2**inputLen, 1):
            x = i ^ j
            y = Sbox(S, i) ^ Sbox(S, j)
            table[x][y] += 1
            full[x][y].add(i)
            full[x][y].add(j)
    return table, full

def reverseKeyGen(n):
    # Reversing the P8 permutation
    a =  f"{n:08b}"
    b = "0" + "0" + a[1]+a[3]+a[5]+a[0]+a[2]+a[4]+a[7]+a[6]
    
    # Reversing the left circular shift
    left = b[0:5]
    right = b[5:10]
    left = left[4] + left[0:4]
    right = right[4] + right[0:4]
    p = left + right
    ikey = p[6]+p[2]+p[0]+p[4]+p[1]+p[9]+p[3]+p[8]+p[7]+p[5]
    return ikey

# EVERYTHING NEEDED TO DECRYPT ================================================================================
# =============================================================================================================
def leftShift(key):
    temp = key[1:5] + key[0]
    return temp
    
def genK1(iKey):
    # Generation of P10
    P10 = iKey[2]+iKey[4]+iKey[1]+iKey[6]+iKey[3]+iKey[9]+iKey[0]+iKey[8]+iKey[7]+iKey[5]
    
    # Generation of LH and RH bits and left shift for both
    left = P10[0:5]
    right = P10[5:10]
    left = leftShift(left)
    right = leftShift(right)
    
    # Generation of P8
    temp = left + right
    P8 = temp[5]+temp[2]+temp[6]+temp[3]+temp[7]+temp[4]+temp[9]+temp[8]
    return P8

def genK2(iKey):
    # Generation of P10
    P10 = iKey[2]+iKey[4]+iKey[1]+iKey[6]+iKey[3]+iKey[9]+iKey[0]+iKey[8]+iKey[7]+iKey[5]
    
    # Generation of LH and RH bits and 3x left shift for both
    left = P10[0:5]
    right = P10[5:10]
    left = leftShift( leftShift( leftShift(left) ) )
    right = leftShift( leftShift( leftShift(right) ) )
    
    # Generation of P8
    temp = left + right
    P8 = temp[5]+temp[2]+temp[6]+temp[3]+temp[7]+temp[4]+temp[9]+temp[8]
    return P8

def Sboxes(left, right):
    # Creating indicies to index S0
    rowS0 = left[0] + left[3]
    colS0 = left[1] + left[2]
    rowS0 = int(rowS0, 2)
    colS0 = int(colS0, 2)
    
    # Creating S0
    S0 = [ [1, 0, 3, 2],
           [3, 2, 1, 0],
           [0, 2, 1, 3],
           [3, 1, 3, 2]
         ]    
    
    # Indexing S0 and changing the value to binary
    ret0 = S0[rowS0][colS0]
    ret0 = bin(ret0)
    ret0 = ret0[2:4]

    # Creating indicies to index S1
    rowS1 = right[0] + right[3]
    colS1 = right[1] + right[2] 
    rowS1 = int(rowS1, 2)
    colS1 = int(colS1, 2)
    
    # Creating S1
    S1 = [ [0, 1, 2, 3],
           [2, 0, 1, 3],
           [3, 0, 1, 0],
           [2, 1, 0, 3]
         ]
    ret1 = S1[rowS1][colS1]
    ret1 = bin(ret1)
    ret1 = ret1[2:4]    
    
    # Padding leading zeros if needed
    if (len(ret0) == 1):
        ret0 = "0" + ret0
    if (len(ret1) == 1):
        ret1 = "0" + ret1 
    return (ret0, ret1)
    
def F(bit4, key): 
    # Expansion of 4-bit into 8-bit
    bit8 = bit4[3]+bit4[0]+bit4[1]+bit4[2]+bit4[1]+bit4[2]+bit4[3]+bit4[0]
    
    # XOR function of 8-bit and 8-bit key
    temp = ""
    for i in range(0, 8, 1):
        x = bit8[i]
        y = key[i]
        if (x == "1" and y == "0"):
            temp = temp + "1"
        elif (x == "0" and y== "1"):
            temp = temp + "1"
        else:
            temp = temp + "0"
                
    # Sbox functions with LH and RH bits
    left = temp[0:4]
    right = temp[4:8]
    (t1, t2) = Sboxes(left, right)
    
    # Generation and permutation of P4
    P4 = t1 + t2
    P4 = P4[1]+P4[3]+P4[2]+P4[0]    
    return P4

def decrypt(cText, key):
    # Initial permutation and generation of LH and RH bits
    IP = cText[1] + cText[5] + cText[2] + cText[0] + cText[3] + cText[7] + cText[4] + cText[6]
    left0 = IP[0:4]
    right0 = IP[4:8]
    r0 = IP[4:8]
    
    # Generation of K2 and first feistel cipher
    K2 = genK2(key)
    right0 = F(right0, K2)
    
    # XOR function for 4-bit left0 and 4-bit right0
    XOR0 = ""
    for i in range(0, 4, 1):
        x = left0[i]
        y = right0[i]
        if (x == "1" and y == "0"):
            XOR0 = XOR0 + "1"
        elif (x == "0" and y== "1"):
            XOR0 = XOR0 + "1"
        else:
            XOR0 = XOR0 + "0"
            
    # Generation of left1 and right1
    left1 = r0
    right1 = XOR0
    
    # Generation of K1 and second feistel cipher
    K1 = genK1(key)
    right1 = F(right1, K1)
    
    #XOR function for 4-bit left1 and 4-bit right1
    XOR1 = ""
    for i in range(0, 4, 1):
        x = left1[i]
        y = right1[i]
        if (x == "1" and y == "0"):
            XOR1 = XOR1 + "1"
        elif (x == "0" and y== "1"):
            XOR1 = XOR1 + "1"
        else:
            XOR1 = XOR1 + "0"
    
    # Inverse initial permutation
    t1 = XOR1 + XOR0
    IPInv = t1[3] + t1[0] + t1[2] + t1[4] + t1[6] + t1[1] + t1[7] + t1[5]
    return IPInv
# =============================================================================================================
# =============================================================================================================


def main():
    # Generate DDT based off of S-box
    S0 = [ [1, 0, 3, 2],
           [3, 2, 1, 0],
           [0, 2, 1, 3],
           [3, 1, 3, 2]
         ]
    S1 = [ [0, 1, 2, 3],
           [2, 0, 1, 3],
           [3, 0, 1, 0],
           [2, 1, 0, 3]
         ]
    DDT0, Full0 = DDT(S0, 4, 2)
    DDT1, Full1 = DDT(S1, 4, 2)
    print("Difference Distribution Table for S0:")
    for i in range(0, len(DDT0), 1):
       print(i, DDT0[i])
    print()
    print("Difference Distribution Table for S1:")
    for i in range(0, len(DDT1), 1):
        print(i, DDT1[i])
    print()
    
    print("Working with S0")
    print("Choosing from DDT0, delta x = 5")
    print("DDT values for delta x = 5", Full0[5])
    print()
    
    print("Using delta y = 3, we know that 2 inputs that XOR to delta x = 5, are 8 and 13")
    print("Suppose x0 = 8 and x1 = 13 have their outputs XOR to 0")
    canKeys0 = set()
    for val0 in Full0[5][3]:
        for val1 in Full0[5][0]:
            canKey = val0^val1
            print(val0, "XOR", val1, "=", canKey)
            canKeys0.add(canKey)
    print("Candidate Keys 0:", canKeys0)
    print()
    
    print("Using delta y = 2, we know that 2 inputs that XOR to delta x = 5, are 9 and 12")
    print("Suppose x0 = 9 and x1 = 11 have their outputs XOR to 0")
    canKeys1 = set()
    temp = [9, 11]
    for i in range(0, 2, 1):
        for val1 in Full0[5][0]:
            canKey = temp[i]^val1
            print(temp[i], "XOR", val1, "=", canKey)
            canKeys1.add(canKey)
    print("Candidate Keys 1:", canKeys1)
    print()
    
    canKeys = canKeys0.intersection(canKeys1)
    print("The candidate keys must appear in both Candidate Keys 0 and Candidate Keys 1:", canKeys)
    print()
    
    print("Now that candidate keys have been reduced by a significant amount, using brute force...")
    print()
    ikey = []
    for val in canKeys:
        temp = reverseKeyGen(val)
        ikey.append(temp)
    
    print("Reverse engineering to initial keys gives:")
    for i in range(0, len(ikey), 1):
        print(ikey[i])
    print()
    
    
    ciphText = "z(8FÃ)"
    print("Known PlainText: crypto")
    print("Known CipherText: ", ciphText)
    print("\tUsed to check which initial key is correct")
    
    for j in range(0, len(ikey), 1):
        # Decryption
        decTextBin = ""
        for i in range(0, len(ciphText), 1):
            # Converting each letter into its binary representation, and then putting it through the cipher
            t = ord(ciphText[i])
            u = f"{t:08b}"
            decTextBin = decTextBin + decrypt(u, ikey[j])
        
        decText = ""
        for i in range(0, int(len(decTextBin)/8), 1):
            x = i * 8
            y = i * 8 + 8
            a = decTextBin[x:y]
            b = int(a, 2)
            c = chr(b)
            decText = decText + c
        print("DecipheredText: ", decText)
        
if __name__ == "__main__":
    main()


































