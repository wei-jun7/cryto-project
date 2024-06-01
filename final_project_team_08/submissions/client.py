import socket
from hash import *
from test import *
from test1 import *

def is_p(n):
    for i in range(2,int(n/2)):
        if(n%i)==0:
            return False
    return True

def find_two(n):
    for i in range(2,int(n/2)):
        if(is_p(i)) and (n%i==0):
            if(is_p(int(n/i))):
                return(i,int(n/i))


def client_encrypt_rsa_semantic_secure(message):
    data = "The quick brown fox jumps over the lazy dog"
    # Helper function to encrypt 8-bit binary string
    def client_encrypt_rsa_a(M):
        M = int(M, 2)
        KU = [11, 221]
        C = pow(M, KU[0], KU[1])
        return bin(C)[2:].zfill(8)

    encrypted_message = ""
    for i in message:
        binary_string = f'{ord(i):08b}'
        hash = sha1(data)
        hashed8=''.join(f'{int(c, 16):04b}' for c in hash)[-8:]
        encrypted_message+=(client_encrypt_rsa_a(xor(binary_string,hashed8)))

    # Convert the encrypted binary message to a byte string
    return bytes(int(encrypted_message[i:i+8], 2) for i in range(0, len(encrypted_message), 8))

def client_decrypt_rsa_semantic_secure(encrypted_bytes):
    data = "The quick brown fox jumps over the lazy dog"
    # Helper function to decrypt 8-bit binary string
    def client_decrypt_rsa_a(C):
        C = int(C, 2)
        KR = [53, 11, 19]
        M = pow(C, KR[0], KR[1] * KR[2])
        return bin(M)[2:].zfill(8)

    # Convert the byte string to binary
    binary_encrypted_message = ''.join(f'{byte:08b}' for byte in encrypted_bytes)

    # Decrypt the binary message
    decrypted_message = ''.join(xor(client_decrypt_rsa_a(binary_encrypted_message[i:i+8]),''.join(f'{int(c, 16):04b}' for c in sha1(data))[-8:]) for i in range(0, len(binary_encrypted_message), 8))

    # Convert the decrypted binary message back to text
    return ''.join(chr(int(decrypted_message[i:i+8], 2)) for i in range(0, len(decrypted_message), 8))

def client_encrypt_rsa(message):
    # Helper function to encrypt 8-bit binary string
    def client_encrypt_rsa_a(M):
        M = int(M, 2)
        KU = [11, 221]
        C = pow(M, KU[0], KU[1])
        return bin(C)[2:].zfill(8)

    encrypted_message = ""
    for i in message:
        binary_string = f'{ord(i):08b}'
        encrypted_message+=(client_encrypt_rsa_a(binary_string))

    # Convert the encrypted binary message to a byte string
    return bytes(int(encrypted_message[i:i+8], 2) for i in range(0, len(encrypted_message), 8))

def client_decrypt_rsa(encrypted_bytes):
    # Helper function to decrypt 8-bit binary string
    def server_decrypt_rsa_a(C):
        C = int(C, 2)
        KR = [53, 11, 19]
        M = pow(C, KR[0], KR[1] * KR[2])
        return bin(M)[2:].zfill(8)

    # Convert the byte string to binary
    binary_encrypted_message = ''.join(f'{byte:08b}' for byte in encrypted_bytes)

    # Decrypt the binary message
    decrypted_message = ''.join(server_decrypt_rsa_a(binary_encrypted_message[i:i+8]) for i in range(0, len(binary_encrypted_message), 8))

    # Convert the decrypted binary message back to text
    return ''.join(chr(int(decrypted_message[i:i+8], 2)) for i in range(0, len(decrypted_message), 8))


def client_decrypt_rsa_k(encrypted_bytes,K1,K2):
    # Helper function to decrypt 8-bit binary string
    def server_decrypt_rsa_a(C):
        C = int(C, 2)
        pq = find_two(K2)
        d = pow(K1,-1,(pq[0]-1)*(pq[1]-1))
        M = pow(C, d, K2)
        return bin(M)[2:].zfill(8)

    # Convert the byte string to binary
    binary_encrypted_message = ''.join(f'{byte:08b}' for byte in encrypted_bytes)

    # Decrypt the binary message
    decrypted_message = ''.join(server_decrypt_rsa_a(binary_encrypted_message[i:i+8]) for i in range(0, len(binary_encrypted_message), 8))

    # Convert the decrypted binary message back to text
    return ''.join(chr(int(decrypted_message[i:i+8], 2)) for i in range(0, len(decrypted_message), 8))


def client_decrypt_rsa_semantic_secure_k(encrypted_bytes,K1,K2):
    data = "The quick brown fox jumps over the lazy dog"
    # Helper function to decrypt 8-bit binary string
    def client_decrypt_rsa_a(C):
        C = int(C, 2)
        pq = find_two(K2)
        d = pow(K1,-1,(pq[0]-1)*(pq[1]-1))
        M = pow(C, d, K2)
        return bin(M)[2:].zfill(8)

    # Convert the byte string to binary
    binary_encrypted_message = ''.join(f'{byte:08b}' for byte in encrypted_bytes)

    # Decrypt the binary message
    decrypted_message = ''.join(xor(client_decrypt_rsa_a(binary_encrypted_message[i:i+8]),''.join(f'{int(c, 16):04b}' for c in sha1(data))[-8:]) for i in range(0, len(binary_encrypted_message), 8))

    # Convert the decrypted binary message back to text
    return ''.join(chr(int(decrypted_message[i:i+8], 2)) for i in range(0, len(decrypted_message), 8))



def client_program():
    host = socket.gethostname()
    port = 6002
    client_socket = socket.socket()
    client_socket.connect((host, port))
    message="hello"
    client_socket.send(client_encrypt_rsa_semantic_secure(message))
    data=client_socket.recv(1024)
    temp=client_decrypt_rsa_semantic_secure(data)
    split = temp.split()
    server_public_key_part_2 = int(split[-1])
    server_public_key_part_1 = int(split[-2])
    message="prove it"
    client_socket.send(client_encrypt_rsa_semantic_secure(message))
    data=client_socket.recv(1024)
    temp=client_decrypt_rsa_semantic_secure_k(data,server_public_key_part_1,server_public_key_part_2)
    if(temp == sha1("Alice, This Is Bob")):
        message="ok bob, here is a secret"+" "+str(11)+" "+str(221)
        client_socket.send(client_encrypt_rsa_semantic_secure(message))

        print("Deposit : 1   Withdraw : 2  Check Balance : 3  Exit : 4")
        message = input("Enter operation code (1, 2, or 3):")
        while message.lower().strip() != '4':
            if(message=="1"):
                amount = input("Enter amount u need deposit: ")
                encrypted_message = client_encrypt_rsa_semantic_secure(message+" "+amount)
                client_socket.send(encrypted_message)
                data = client_socket.recv(1024)
                print(client_decrypt_rsa_semantic_secure(data))
            if(message=="2"):
                amount = input("Enter amount u need withdraw: ")
                encrypted_message = client_encrypt_rsa_semantic_secure(message+" "+amount)
                client_socket.send(encrypted_message)
                data = client_socket.recv(1024)
                print(client_decrypt_rsa_semantic_secure(data))
            if(message=="3"):
                encrypted_message = client_encrypt_rsa_semantic_secure(message+" 0")
                client_socket.send(encrypted_message)
                data = client_socket.recv(1024)
                print(client_decrypt_rsa_semantic_secure(data))
            print("Deposit : 1   Withdraw : 2  Check Balance : 3  Exit : 4")
            message = input("Enter operation code (1, 2, or 3):")
        
    client_socket.close()

if __name__ == '__main__':
    client_program()