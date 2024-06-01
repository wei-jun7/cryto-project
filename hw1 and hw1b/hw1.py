# Simplified DES Algorithm Implementation

def permute(k, arr, n):
    permutation = ""
    for i in range(0, n):
        permutation += k[arr[i] - 1]
    return permutation

def shift_left(k, shifts):
    s = ""
    for i in range(shifts):
        for j in range(1, len(k)):
            s += k[j]
        s += k[0]
        k = s
        s = ""
    return k

def xor(a, b):
    ans = ""
    for i in range(len(a)):
        if a[i] == b[i]:
            ans += "0"
        else:
            ans += "1"
    return ans

def s_box(sbox, row, col):
    # return the s box in the form of a 2 bit binary number
    return sbox[row][col]

def convert_to_binary(text):
    """Converts the given text to binary."""
    binary_representation = ''
    for char in word:
        binary_representation += format(ord(char), '08b') + ' '
        
    return binary_representation.strip()

def key_generation(p10,p8,key):
    """Generate the keys."""
    # First key permutation
   
    key = permute(key, p10, 10)

    # Splitting
    left = key[:5]
    right = key[5:]

    # First shift
    left = shift_left(left, 1)
    right = shift_left(right, 1)

    # Second key permutation
    
    key1 = permute(left + right, p8, 8)

    # Second shift
    left = shift_left(left, 2)
    right = shift_left(right, 2)

    # Third key permutation
    key2 = permute(left + right, p8, 8)

    return key1, key2

def function_fk(part, sk):
    """Function Fk."""
    # Expansion permutation (E/P)
    ep = [4, 1, 2, 3, 2, 3, 4, 1]
    part = permute(part, ep, 8)

    # XOR with the subkey
    part = xor(part, sk)

    # S-boxes
    s0 = [[1, 0, 3, 2], [3, 2, 1, 0], [0, 2, 1, 3], [3, 1, 3, 2]]
    s1 = [[0, 1, 2, 3], [2, 0, 1, 3], [3, 0, 1, 0], [2, 1, 0, 3]]

    # Divide the part into two halves
    left = part[:4]
    right = part[4:]

    # Row and column for S-boxes
    row1 = int(left[0] + left[3], 2)
    col1 = int(left[1] + left[2], 2)
    row2 = int(right[0] + right[3], 2)
    col2 = int(right[1] + right[2], 2)

    # Perform the S-box lookups
    s_box_result_0 = s_box(s0, row1, col1)
    s_box_result_1 = s_box(s1, row2, col2)

    # Convert the S-box results to binary and pad with zeros if necessary
    result_bin_0 = format(s_box_result_0, '02b')
    result_bin_1 = format(s_box_result_1, '02b')

    # Combine the two binary results
    result_combined = result_bin_0 + result_bin_1

    # P4 permutation
    p4 = [2, 4, 3, 1]
    result = permute(result_combined, p4, 4)

    return result

def s_des_encrypt(plaintext, key1, key2,ip ,ip_inv):


    # Initial permutation
    plaintext = permute(plaintext, ip, 8)

    # Splitting
    left = plaintext[:4]
    right = plaintext[4:]

    # Round 1
    left = xor(left, function_fk(right, key1))
    left, right = right, left  # Switch

    # Round 2
    left = xor(left, function_fk(right, key2))

    # Combine and final permutation (inverse of IP)
    result = permute(left + right, ip_inv, 8)

    return result

def s_des_decrypt(ciphertext, key1, key2 ,ip ,ip_inv ):


    # Initial permutation
    ciphertext = permute(ciphertext, ip, 8)
    

    # Splitting
    left = ciphertext[:4]
    right = ciphertext[4:]

    # Round 1 (using key2 for decryption)
    left = xor(left, function_fk(right, key2))
    left, right = right, left  # Switch

    # Round 2 (using key1 for decryption)
    left = xor(left, function_fk(right, key1))

    # Combine and final permutation (inverse of IP)
    result = permute(left + right, ip_inv, 8)

    return result


if __name__ == '__main__':
    
    # Convert plaintext to binary
    word = "crypto"
    
    binary_representation = convert_to_binary(word)

    # Initial Key
    key = "1100011110"

    p10 = [3, 5, 2, 7, 4, 10, 1, 9, 8, 6]
    p8 = [6, 3, 7, 4, 8, 5, 10, 9]
    
    #2 rounds key
    key1,key2 = key_generation(p10,p8,key)
    
    # Initial permutation
    ip = [2, 6, 3, 1, 4, 8, 5, 7]
    # Combine and final permutation (inverse of IP)
    ip_inv = [4, 1, 3, 5, 7, 2, 8, 6]
    
    
    # Test case
    test_block = '00101000'
    enblock = s_des_encrypt(test_block, key1, key2,ip ,ip_inv)
    deblock = s_des_decrypt(enblock, key1, key2,ip ,ip_inv)
    print("Test case")
    print("Original Binary:  ", test_block)
    print("Encrypted Binary: ", enblock)
    print("Decrypted Binary: ", deblock)
    
    # we encrypt each block and use for loop to generate the encrypted blocks and decrypt block then print it at the end
    blocks = binary_representation.split(' ')
    encrypted_blocks = []
    decrypted_blocks = []

    for block in blocks:
        encrypted_block = s_des_encrypt(block, key1, key2,ip ,ip_inv)
        decrypted_block = s_des_decrypt(encrypted_block, key1, key2, ip,ip_inv)
        encrypted_blocks.append(encrypted_block)
        decrypted_blocks.append(decrypted_block)
    
    encrypted_result = ' '.join(encrypted_blocks)
    decrypted_result = ' '.join(decrypted_blocks)
    

    # Displaying the results
    print("Original Binary:  ", binary_representation)
    print("Encrypted Binary: ", encrypted_result)
    print("Decrypted Binary: ", decrypted_result)
    print("Key1 and Key2: ", key1,key2)

