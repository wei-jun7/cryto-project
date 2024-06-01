
Overview
The Blum-Goldwasser algorithm operates on binary data, transforming plaintext messages into encrypted ciphertext and vice versa, using modular arithmetic and properties of prime numbers. The encryption process generates a ciphertext and a part of the key used for decryption. The decryption process requires the ciphertext and the decryption part of the key to recover the original message.

Components
Extended Euclidean Algorithm (extended_gcd): A function used to find the greatest common divisor (GCD) of two numbers and the coefficients (Bezout's coefficients) that satisfy Bezout's identity.

Modular Exponentiation (mod_exp): Efficiently computes base raised to the power exponent modulo a modulus. This function is crucial for the encryption and decryption processes, handling large exponentiations.

XOR Operation (xor): Performs a bitwise XOR operation on two binary strings. In the context of this implementation, it's used to encrypt and decrypt individual bits of the message.

Split Message (split_m): Divides a binary message into chunks of a specified length. This division is necessary for processing the message in parts during encryption and decryption.

Encrypt Function (encrypt): Accepts a binary message and public key components (primes p and q, and a random quadratic residue x0), returning the ciphertext and the last value of x used in encryption.

Decrypt Function (decrypt): Uses the ciphertext, the last x value from the encryption, the primes p and q, and the length of the split binary message to recover the original message.

Example Usage
Given the binary representation of "NETSEC", the primes p = 499 and q = 547, and a random quadratic residue x0 = 159201, the script encrypts the message and then decrypts it, demonstrating the BG algorithm's effectiveness.

