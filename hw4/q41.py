
import numpy as np

def square_and_multiply(x, exp, mod):
    result = 1
    base = x % mod
    while exp > 0:
        if (exp % 2) == 1:
            result = (result * base) % mod
        base = (base * base) % mod
        exp = exp >> 1
        #print(f"Square-and-Multiply: Current Base={base}, Current Exp={exp}, Mod={mod}, Intermediate Result={result}")  # 更准确的调试信息
    return result

def crt(a, a_mod, b, b_mod):
    # Extended Euclidean Algorithm to find inverses
    def extended_gcd(aa, bb):
        lastremainder, remainder = abs(aa), abs(bb)
        x, lastx, y, lasty = 0, 1, 1, 0
        while remainder:
            lastremainder, (quotient, remainder) = remainder, divmod(lastremainder, remainder)
            x, lastx = lastx - quotient*x, x
            y, lasty = lasty - quotient*y, y
        return lastremainder, lastx * (-1 if aa < 0 else 1), lasty * (-1 if bb < 0 else 1)
    
    # Diophantine solution to ax + by = gcd(a, b)
    gcd, x, y = extended_gcd(a_mod, b_mod)
    if a % gcd != b % gcd:
        raise ValueError('No solutions!')
    lcm = a_mod // gcd * b_mod
    result = (a * (b_mod // gcd) * y + b * (a_mod // gcd) * x) % lcm
    return result + lcm if result < 0 else result


def encrypt(message, p, q, x0):
    n = p * q
    binary_message = ''.join(format(ord(char), '08b') for char in message)
    length = len(binary_message)
    x = x0
    encrypted_bits = []
    x_values = [x]
    
    for bit in binary_message:
        x = square_and_multiply(x, 2, n)
        x_values.append(x)
        b = x % 2
        encrypted_bit = int(bit) ^ b
        encrypted_bits.append(encrypted_bit)
    
    xt = x_values[-1]
    print("Final xt:", xt)  # Debug: Output final xt
    return encrypted_bits, xt, x_values

def decrypt(encrypted_bits, xt, p, q, length):
    n = p * q
    t = length
    # Calculate exponents more carefully
    exponent_p = pow(2, t, p - 1)
    exponent_q = pow(2, t, q - 1)

    # Debugging: Print calculated exponents
    print(f"Debug: exponent_p={exponent_p}, exponent_q={exponent_q}")


    xp = square_and_multiply(xt, exponent_p, p)
    xq = square_and_multiply(xt, exponent_q, q)
    print(f"Calculated xp: {xp}, xq: {xq} from xt: {xt}")
    x0 = crt(xp, p, xq, q)
    print(f"Recovered x0: {x0}, expected x0: {159201} for verification")
    original_message = []
    x = x0
    for bit in encrypted_bits:
        x = square_and_multiply(x, 2, n)
        b = x % 2
        decrypted_bit = bit ^ b
        original_message.append(str(decrypted_bit))
    binary_string = ''.join(original_message)
    print("Binary string before conversion:", binary_string)
    decrypted_bytes = bytearray(int(binary_string[i:i+8], 2) for i in range(0, len(binary_string), 8))
    decrypted_message = decrypted_bytes.decode('latin-1')
    return decrypted_message


p = 499
q = 547
x0 = 159201
message = "NETSEC"


encrypted_bits, xt, x_values = encrypt(message, p, q, x0)
encrypted_message = ''.join(map(str, encrypted_bits))
print("Encrypted Message:", encrypted_message)


decrypted_message = decrypt(encrypted_bits, xt, p, q, len(encrypted_bits))
print("Decrypted Message:", decrypted_message)
