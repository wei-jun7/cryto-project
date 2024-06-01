#------------------------------------------------------------------------
def xor(bits1, bits2):
    return ''.join(str(int(b1) ^ int(b2)) for b1, b2 in zip(bits1, bits2))

#------------------------------------------------------------------------
def permute(input_bits, permutation_table):
    output_bits = ''
    for index in permutation_table:
        output_bits += input_bits[index - 1]  # Adjust for 0-based indexing
    return output_bits

#------------------------------------------------------------------------
def S0(input_bits):
    # Substitution matrix (S-box)
    sbox = [[1, 0, 3, 2],
            [3, 2, 1, 0],
            [0, 2, 1, 3],
            [3, 1, 3, 2]]

    if len(input_bits) != 4:
        raise ValueError("Input must be a 4-bit string.")

    # Calculate row index (bits 1 and 4)
    row = int(input_bits[0] + input_bits[3], 2)

    # Calculate column index (bits 2 and 3)
    column = int(input_bits[1] + input_bits[2], 2)

    # Perform the substitution
    output = sbox[row][column]

    return format(output, '02b')  # Return the output as a 2-bit binary string

#------------------------------------------------------------------------
def S1(input_bits):
    # Substitution matrix (S-box)
    sbox = [[0, 1, 2, 3],
            [2, 0, 1, 3],
            [3, 0, 1, 0],
            [2, 1, 0, 3]]

    if len(input_bits) != 4:
        raise ValueError("Input must be a 4-bit string.")

    # Calculate row index (bits 1 and 4)
    row = int(input_bits[0] + input_bits[3], 2)

    # Calculate column index (bits 2 and 3)
    column = int(input_bits[1] + input_bits[2], 2)

    # Perform the substitution
    output = sbox[row][column]

    return format(output, '02b')  # Return the output as a 2-bit binary string

#------------------------------------------------------------------------
#the functions used in F
def F0(input_bits):
    if len(input_bits) != 4:
        raise ValueError("Input must be a 4-bit string.")

    # Expansion and permutation for F1 and F2
    F1 = permute(input_bits, [4, 1, 2, 3])
    F2 = permute(input_bits, [2, 3, 4, 1])

    # Combine F1 and F2 to get an 8-bit output
    output = F1 + F2
    return output

#------------------------------------------------------------------------
def circular_left_shift(bits, number_of_shifts):
    shifted_bits = bits[number_of_shifts:] + bits[:number_of_shifts]
    return shifted_bits

#------------------------------------------------------------------------
def generate_keys(initial_key):
    # Apply P10 permutation
    p10_table = [3, 5, 2, 7, 4, 10, 1, 9, 8, 6]
    key_after_p10 = permute(initial_key, p10_table)

    # Split the key into two halves
    left_half, right_half = key_after_p10[:5], key_after_p10[5:]

    # First round of left shifts
    left_half_shifted = circular_left_shift(left_half, 1)
    right_half_shifted = circular_left_shift(right_half, 1)

    # Combine and apply P8 to get K1
    combined_key_for_k1 = left_half_shifted + right_half_shifted
    p8_table = [6, 3, 7, 4, 8, 5, 10, 9]
    k1 = permute(combined_key_for_k1, p8_table)

    # Second round of left shifts
    left_half_shifted = circular_left_shift(left_half_shifted, 2)
    right_half_shifted = circular_left_shift(right_half_shifted, 2)

    # Combine and apply P8 to get K2
    combined_key_for_k2 = left_half_shifted + right_half_shifted
    k2 = permute(combined_key_for_k2, p8_table)

    return k1, k2

#------------------------------------------------------------------------
def F(input_bits, key):
    if len(input_bits) != 4 or len(key) != 8:
        raise ValueError("Input must be a 4-bit string and key must be an 8-bit string.")

    # Apply F0 to the 4-bit input to get an 8-bit output
    expanded_input = F0(input_bits)

    # XOR the expanded input with the key
    xor_result = xor(expanded_input, key)

    # Divide the result into two 4-bit parts
    left_half, right_half = xor_result[:4], xor_result[4:]

    # Apply substitution function and combine
    output_S0 = S0(left_half)
    output_S1 = S1(right_half)
    combined_output = output_S0 + output_S1

    # Apply P4 permutation [2, 4, 3, 1] to the combined output
    final_output = permute(combined_output, [2, 4, 3, 1])

    return final_output

#------------------------------------------------------------------------
def encrypt(plaintext, key):
    if len(plaintext) != 8 or len(key) != 10:
        raise ValueError("Plaintext must be an 8-bit string and key must be a 10-bit string.")

    # Generate K1 and K2
    K1, K2 = generate_keys(key)

    # Apply initial permutation and divide into two 4-bit halves
    permuted_text = permute(plaintext, [2, 6, 3, 1, 4, 8, 5, 7])
    text1, text2 = permuted_text[:4], permuted_text[4:]

    # Apply function F to text2 with K1
    textF2 = F(text2, K1)

    # XOR text1 with textF2
    textX1 = xor(text1, textF2)

    # Apply function F to textX1 with K2
    textF1 = F(textX1, K2)

    # XOR textF1 with text2
    textX2 = xor(textF1, text2)

    # Combine textX2 and textX1
    combined_text = textX2 + textX1

    # Apply inverse initial permutation
    ciphertext = permute(combined_text, [4, 1, 3, 5, 7, 2, 8, 6])

    return ciphertext

#------------------------------------------------------------------------
def decrypt(ciphertext, key):
    if len(ciphertext) != 8 or len(key) != 10:
        raise ValueError("Ciphertext must be an 8-bit string and key must be a 10-bit string.")

    # Generate K1 and K2
    K1, K2 = generate_keys(key)

    # Apply initial permutation and divide into two 4-bit halves
    permuted_text = permute(ciphertext, [2, 6, 3, 1, 4, 8, 5, 7])
    text1, text2 = permuted_text[:4], permuted_text[4:]

    # Apply function F to text2 with K2
    textF2 = F(text2, K2)

    # XOR text1 with textF2
    textX1 = xor(text1, textF2)

    # Apply function F to textX1 with K1
    textF1 = F(textX1, K1)

    # XOR textF1 with text2
    textX2 = xor(textF1, text2)

    # Combine textX2 and textX1
    combined_text = textX2 + textX1

    # Apply inverse initial permutation
    plaintext = permute(combined_text, [4, 1, 3, 5, 7, 2, 8, 6])

    return plaintext

#------------------------------------------------------------------------
def string_to_8bit_list(input_string):
    return [format(ord(char), '08b') for char in input_string]

#------------------------------------------------------------------------
def list_8bit_to_string(binary_list):
    return ''.join(chr(int(binary, 2)) for binary in binary_list)

#------------------------------------------------------------------------
def encrypt_final(input_string,key):
    print("\nstart encryption:")
    plain = string_to_8bit_list(input_string)
    print("list of 8-bit plain text: ")
    print(plain)
    cipher = []
    for i in plain:
        cipher.append(encrypt(i,key))
    print("list of 8-bit cipher text: ")
    print(cipher)
    return cipher

#------------------------------------------------------------------------
def decrypt_final(cipher,key):
    print("\nstart decryption:")
    print("list of 8-bit cipher text: ")
    print(cipher)
    plain = []
    for i in cipher:
        plain.append(decrypt(i,key))
    print("list of 8-bit plain text: ")
    print(plain)
    output_string = list_8bit_to_string(plain)
    return output_string