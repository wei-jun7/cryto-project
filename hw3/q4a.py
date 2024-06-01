from sympy import mod_inverse

# Given parameters for RSA encryption
p = 173
q = 7
N = p * q  # RSA modulus
e = 7  # Public exponent
phi_N = (p - 1) * (q - 1)  # Euler's totient function of N

# Calculate the private key 'd' using modular inverse
d = mod_inverse(e, phi_N)

# Convert message "NETSEC" to ASCII values
message = "NETSEC"
m_values = [ord(char) for char in message]  # List of ASCII values for each character

# Encrypt each ASCII value of the message
# Encryption formula: c = m^e mod N
c_values = [pow(m, e, N) for m in m_values]

# Decrypt each encrypted value back to the original ASCII values
# Decryption formula: m = c^d mod N
m_decrypted_values = [pow(c, d, N) for c in c_values]
# Convert ASCII values back to characters to form the decrypted message
decrypted_message = ''.join(chr(m) for m in m_decrypted_values)

# Print encrypted and decrypted values for verification
print("Encrypted values:", c_values)
print("Decrypted message:", decrypted_message)


