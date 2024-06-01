import socket
from hash import *
from test import *
from test1 import *

def server_decrypt_rsa_semantic_secure(encrypted_bytes):
    data = "The quick brown fox jumps over the lazy dog"
    # Helper function to decrypt 8-bit binary string
    def server_decrypt_rsa_a(C):
        C = int(C, 2)
        KR = [35, 13, 17]
        M = pow(C, KR[0], KR[1] * KR[2])
        return bin(M)[2:].zfill(8)

    # Convert the byte string to binary
    binary_encrypted_message = ''.join(f'{byte:08b}' for byte in encrypted_bytes)

    # Decrypt the binary message
    decrypted_message = ''.join(xor(server_decrypt_rsa_a(binary_encrypted_message[i:i+8]),''.join(f'{int(c, 16):04b}' for c in sha1(data))[-8:]) for i in range(0, len(binary_encrypted_message), 8))

    # Convert the decrypted binary message back to text
    return ''.join(chr(int(decrypted_message[i:i+8], 2)) for i in range(0, len(decrypted_message), 8))

def server_encrypt_rsa_semantic_secure(message):
    data = "The quick brown fox jumps over the lazy dog"
    # Helper function to encrypt 8-bit binary string
    def server_encrypt_rsa_a(M):
        M = int(M, 2)
        KU = [17, 209]
        C = pow(M, KU[0], KU[1])
        return bin(C)[2:].zfill(8)

    encrypted_message = ""
    for i in message:
        binary_string = f'{ord(i):08b}'
        hash = sha1(data)
        hashed8=''.join(f'{int(c, 16):04b}' for c in hash)[-8:]
        encrypted_message+=(server_encrypt_rsa_a(xor(binary_string,hashed8)))

    # Convert the encrypted binary message to a byte string
    return bytes(int(encrypted_message[i:i+8], 2) for i in range(0, len(encrypted_message), 8))

def server_decrypt_rsa(encrypted_bytes):
    # Helper function to decrypt 8-bit binary string
    def server_decrypt_rsa_a(C):
        C = int(C, 2)
        KR = [35, 13, 17]
        M = pow(C, KR[0], KR[1] * KR[2])
        return bin(M)[2:].zfill(8)

    # Convert the byte string to binary
    binary_encrypted_message = ''.join(f'{byte:08b}' for byte in encrypted_bytes)

    # Decrypt the binary message
    decrypted_message = ''.join(server_decrypt_rsa_a(binary_encrypted_message[i:i+8]) for i in range(0, len(binary_encrypted_message), 8))

    # Convert the decrypted binary message back to text
    return ''.join(chr(int(decrypted_message[i:i+8], 2)) for i in range(0, len(decrypted_message), 8))

def server_encrypt_rsa(message):
    # Helper function to encrypt 8-bit binary string
    def client_encrypt_rsa_a(M):
        M = int(M, 2)
        KU = [17, 209]
        C = pow(M, KU[0], KU[1])
        return bin(C)[2:].zfill(8)

    encrypted_message = ""
    for i in message:
        binary_string = f'{ord(i):08b}'
        encrypted_message+=(client_encrypt_rsa_a(binary_string))

    # Convert the encrypted binary message to a byte string
    return bytes(int(encrypted_message[i:i+8], 2) for i in range(0, len(encrypted_message), 8))



balance=0
def encrypt_message(message, key, iv):
    return message.encode('utf-8') 
def decrypt_message(encrypted_message, key, iv):
    return  encrypted_message.decode('utf-8') 
def deposit(depo):
    global balance
    balance += int(depo)
    return "Deposit SUCCESS, your current balance is {}".format(balance)
def withdraw(cash):
    global balance
    if int(cash) > balance:
        return "Withdrawal amount larger than your balance"
    else:
        balance -= int(cash)
        return "Here is your cash!! Your remaining balance is {}".format(balance)
    return balance
def check_balance():
    return "Your remaining balance is {}".format(balance)

    

def server_program():
    host = socket.gethostname()
    port = 6002
    server_socket = socket.socket()
    server_socket.bind((host, port))
    server_socket.listen(2)
    print("Server is listening...")
    conn, address = server_socket.accept()
    print(f"Connection from: {address}")
    data = conn.recv(1024)
    if(server_decrypt_rsa_semantic_secure(data)=='hello'):
        response="Hi, I'm Bob"+" "+str(17)+" "+str(209)
        conn.send(server_encrypt_rsa_semantic_secure(response))
        data = conn.recv(1024)
        if(server_decrypt_rsa_semantic_secure(data)=='prove it'):
            response1="Alice, This Is Bob"
            aa= server_encrypt_rsa_semantic_secure(sha1(response1))
            conn.send(aa)
            data = conn.recv(1024)
    
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                decrypted_message = server_decrypt_rsa_semantic_secure(data)
                operation, value = decrypted_message.split()
                operation = int(operation)
                value = int(value)
                if operation==1:
                    response=deposit(value)
                    response=str(response)
                    conn.send(server_encrypt_rsa_semantic_secure(response)) 
                elif operation==2:
                    response=withdraw(value)
                    response=str(response)
                    conn.send(server_encrypt_rsa_semantic_secure(response)) 
                elif operation==3:
                    response = check_balance()
                    response=str(response)
                    conn.send(server_encrypt_rsa_semantic_secure(response)) 
                else:
                    print("Failed to decrypt message.")
    conn.close()

if __name__ == '__main__':
    server_program()
