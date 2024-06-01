'''
This is the HW3 Programming Part A For Cryptography and Network Security HW3 taught by Professor Yener at RPI for Fall '18. 

Assignment: 

3.Prog.a. Impelment Blum Goldwasser Probabilistic Encryption Algorithm with the following setup parameters:
p=499, q=547, a=-57, b=52, X0 =159201.
message m to be encrypted is in binary: 10011100000100001100

1. What is the ciphertext?
2. Verify your answer by showing that D(C(m))=m.

I'll be implementing Blum-Goldwasser as described here: https://en.wikipedia.org/wiki/Blum%E2%80%93Goldwasser_cryptosystem
'''

import random
import numpy 
import sys
import binascii
sys.setrecursionlimit(1000000)

# credits to https://stackoverflow.com/questions/4798654/modular-multiplicative-inverse-function-in-python
# because I'm too lazy to write my own multiplicative inverse function right now 

def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)

def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        return("ERROR! THE MULTIPLICATIVE INVERSE DOES NOT EXIST!")
    else:
        return x % m

def text_to_bits(cti):
    return ''.join('{:08b}'.format(ord(c)) for c in cti)

def text_from_bits(s):
    return ''.join(chr(int(s[i*8:i*8+8],2)) for i in range(len(s)//8))

def int2bytes(i):
    hex_string = '%x' % i
    n = len(hex_string)
    return binascii.unhexlify(hex_string.zfill(n + (n & 1)))

def key_generation(p = -1, q = -1):
	'''
	the prime factors, p and q, need to be congruent to 3 % 4. 
	If p and q are not given, generate p and q. 
	'''
	tester = 3 % 4 

	if p == -1: 
		while((p % 4) == tester):
			p = np.random.randint(100, 1024)
	if q == -1 or q == p:
		while((q % 4) == tester):
			q = np.random.randint(100, 1024)

	# now they should be good 
	public_N = p * q
	return public_N 

def message_encryption(m, priv_key, N_gen,x_0 = -1):
	'''
	m is sent in as a string of N bits. 

	If an x_0 is not provided, it is made. 

	This'll return the decimal integer version of the cipher and the cipher bits in a list 
	'''
	if x_0 == -1:
		r = np.random.randint(1, N)
		x_0 = (r**r) % N_gen

	L = len(m) 
	b = ['0' for i in range(L)]
	x_i = x_0_given
	for i in range(L):
		b[i] = int(("{:08b}".format(x_i))[-1])
		x_i = (x_i ** 2) % N_gen

	b = b[::-1]
	# get m ready to get cipher'd 
	m_split = [] # should be the same length as L 
	for letter in m:
		m_split.append(letter)
	# print("m_split: ", m_split)
	if (len(m_split) != L and len(m_split) != len(b)):
		print("the message wasn't the same length when split as before. Try again!")
		sys.exit(0)
	cipher_list = ['0' for i in range(L)]
	print("Printing b", b)
	print("Printing m_split:", m_split)
	print("Printing x_i", x_i)
	for i in range(L):
		cipher_list[i] = str(int(m_split[i]) ^ b[i])

	ciphertext = "".join(cipher_list)

	return int(ciphertext, 2), cipher_list, x_i

def message_decryption(cipher_text, p, q, N, a, b, x_l):
	'''
	given a ciphertext, Alice reveives y, and can probably turn it into bits 
	NOTE: We're using 20 bits, so make sure to convert bits in terms of that. 
	Except when calculating randomly generated numbers, I guess those can be 8bit as 
	done in the message_encryption function

	a and b are the numbers such that ap + bq = 1
	'''
	cipher_bit_string = "{:020b}".format(cipher_text)
	cipher_bit_list = [letter for letter in cipher_bit_string]
	print("from message_decryption, cipher_bit_string is: ", cipher_bit_string)
	print("from message_decryption, cipher_bit_list is: ", cipher_bit_list)
	L = len(cipher_bit_list)

	r_p_helper = (((p + 1)//4) ** L) % (p-1)

	r_p = pow(x_l, r_p_helper, p)

	# r_q_helper = ((q+1)/4)**L
	r_q_helper = ( ((q + 1)//4) ** L) % (q-1)
	# r_q = cipher_text**r_q_helper % q
	r_q = pow(x_l, r_q_helper, q)

	# q_inv = modinv(q, p)
	# p_inv = modinv(p, q)

	# print("p is: ", p)
	# print("q is: ", q)
	# print("p_inv is: ", p_inv)
	# print("q_inv is: ", q_inv)
	generated_x_0 = (q*b*r_p + p*a*r_q) % N
	b = ['0' for i in range(L)]
	x_i = generated_x_0

	for i in range(L):
		b[i] = int(("{:08b}".format(x_i))[-1])
		x_i = (x_i ** 2) % N

	message_list = ['0' for i in range(L)]

	b = b[::-1]

	for i in range(L):
		message_list[i] = str(int(cipher_bit_list[i]) ^ b[i])

	generated_m = "".join(message_list)

	return int(generated_m, 2), message_list



if __name__ == "__main__":
	# given vars
	p_given = 499
	q_given = 547
	a_given = -57 
	b_given = 52
	x_0_given = 159201
	m_to_encrypt = '10011100000100001100' # 20-bits

	print("We will be encrypted the given message", m_to_encrypt, "using Blum-Goldwasser!")

	N = key_generation(p_given, q_given)
	private_key = (p_given, q_given)

	cipher, cipher_bits, x_L = message_encryption(m_to_encrypt, private_key, N, x_0_given)
	print("Cipher is :", cipher)
	print("cipher_bits is: ", cipher_bits)

	print("\nNow to decrypt...\n")

	decrypted_m, decrypted_m_bits = message_decryption(cipher, p_given, q_given, N, a_given, b_given, x_L)

	print("The decrypted message is: ", decrypted_m)
	print("The decrypted_m_bits are:", "".join(decrypted_m_bits))

	print("The result of seeing if the given message and the generated decrypted_m_bits are the same is", "".join(decrypted_m_bits) == m_to_encrypt)