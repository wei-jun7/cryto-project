#DO NOT DELETE SLEEP STATEMENTS
#RSA OAEP may take up to 30s

import socket
import RSA as RSA
import RSA_OAEP as RSA_OAEP
import DES as DES
import Paillier as Paillier
import time as time
from sympy import nextprime
import random
from DES_hash import hash_encrypt_triple_SDES
from DES_hash import hash_decrypt_triple_SDES
import time

def decryptF_data(protocol, data):
    if protocol == '1':
        return DES.decrypt(data)
    elif protocol == '2':
        return RSA.decrypt(data)
    elif protocol == '3':
        return Paillier.decrypt(data)
    elif protocol == '4':
        return RSA_OAEP.decrypt(data)
    else:
        raise ValueError("Unknown protocol")

#generates random 10 bit key eg "1010110001"
def generate_SDES_key():
    key = ""
    for i in range(10): 
        key += str(random.randint(0 , 1))
    return key

    
def main():
    host = 'localhost'
    port = 65432
    balance = 100  # Assume an initial balance of 100
    p = nextprime(random.getrandbits(20// 2))
    q = nextprime(random.getrandbits(30 // 2))   #for RSA keys
    public, private = RSA.generate_keypair(p, q) 
    public_key_OAEP , private_key_OAEP = RSA_OAEP.generate_keypair(2048)

    print("public key: ", public)
    print("public key for RSA_OAEP: ", public_key_OAEP)

    public_key_p,private_key_p = Paillier.generate_keypair(2048)
    print("public key for Pailer: ", public_key_p)
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind((host, port))
        server.listen()
        print("Server is listening on", host, port)
        while True:
            conn, addr = server.accept()
            print(f"Connection from {addr}")
            r1 = conn.recv(64000).decode('utf-8')
            message = "Hello, this is the server\n"
            print(f"Message is {r1}")
            conn.send(message.encode('utf-8'))
            try:

                while True:
                    key = generate_SDES_key()
                    protocol_data = conn.recv(64).decode('utf-8')
                    if not protocol_data:
                        break

                    if protocol_data in ["1", "2", "3"]:
                        protocols = ["RSA", "RSA-OAEP" , "Paillier"]
                        protocol = protocols[int(protocol_data) - 1]
                        response = f"Protocol selected: {protocol}\n"
                        conn.send(response.encode('utf-8'))
                    else:
                        print("Unknown protocol")
                        break
                    if (protocol_data == "1"):  
                        print("starting RSA protocol")
                        time.sleep(1)
                        conn.send(f"{public[0]} {public[1]}\n".encode('utf-8'))
                        print("e: " + str(public[0]) + " n: " + str(public[1]))
                        clientpublic_key= conn.recv(102400).decode('utf-8').split()
                        print("c e:",clientpublic_key[0],"c n:",clientpublic_key[1])
                        
                        message_from_client = conn.recv(102400).decode('utf-8')
                        print("Encrypted message from client: ", message_from_client)
                        ciphertext = [int(num) for num in message_from_client.split(', ')]
                        
                        decrypted_message = RSA.decrypt(private, ciphertext )
                        print("Decrypted message from client: ", decrypted_message )
                        message_to_client = key
                        #print("key is" , key)
                        en_message = RSA.encrypt((int(clientpublic_key[0]), int(clientpublic_key[1])), message_to_client)
                        #print("en_message is" , en_message)
                        enc = ', '.join(str(num) for num in en_message) 
                        #print("enc is" , enc)
                        conn.send(enc.encode('utf-8'))
                        print("Encrypted message to client: ", enc)
                        
                    elif(protocol_data == "2"):
                        time.sleep(2)
                        print("starting RSA_OAEP protocol")
                        conn.send(f"{public_key_OAEP[0]} {public_key_OAEP[1]}\n".encode('utf-8'))
                        print("e: " + str(public_key_OAEP[0]) + " n: " + str(public_key_OAEP[1]))
                        clientpublic_key= conn.recv(102400000).decode('utf-8').split()
                        print("c e:",clientpublic_key[0],"c n:",clientpublic_key[1])
                        e_int = int(clientpublic_key[0])  # 转换 e
                        n_int = int(clientpublic_key[1])  # 转换 n
                        
                        message_from_client= conn.recv(100000000).decode('utf-8') #receive line 127
                        print("Encrypted message from client: ", message_from_client)
                        ciphertext = [int(num) for num in message_from_client.split(', ')]
                        print("ciphertext:",ciphertext)
                        decrypted_encoded_msg = [pow(c, private_key_OAEP[0], private_key_OAEP[1]) for c in ciphertext]
                        decrypted_msg = RSA_OAEP.oaep_decode(bytes(decrypted_encoded_msg), private_key_OAEP[1])
                        print("Decrypted message from client: ", decrypted_msg )
                        
                        message_from_server = key
                        encode_message= RSA_OAEP.oaep_encode(message_from_server,n_int)
                        encrypted_msg = [pow(m, int(clientpublic_key[0]), int(clientpublic_key[1])) for m in encode_message]
                        print("Encoded message", encrypted_msg)
                        encrypted_message = ', '.join(str(num) for num in encrypted_msg)
                        conn.send(encrypted_message.encode('utf-8'))
                        print("Encrypted message to client: ", encrypted_message)
                        
                    elif(protocol_data == "3"):
                        time.sleep(1)
                        client_key_data= conn.recv(1000000).decode('utf-8').split()
                        conn.send(f"{public_key_p[0]} {public_key_p[1]}\n".encode('utf-8'))
                        n_int = int(client_key_data[0])  
                        g_int = int(client_key_data[1])  
                        print("n: ",n_int," g: ",g_int)
                        
                        message_from_client = conn.recv(1000000).decode('utf-8')
                        message_from_client = int(message_from_client)
                        decode_response = Paillier.decrypt(private_key_p,public_key_p,message_from_client)
                        print("decode_response: ",decode_response)
                        
                        message= int(key , 2) #pallier takes in an int instead of string
                        en_message = Paillier.encrypt((n_int, g_int), message)
                        
                        conn.send(str(en_message).encode('utf-8'))
                        print("Encrypted message to client: ", en_message)
                        print("server key is" , key)
                        
                        
                        
                    #print("Here")
                    while True:  
                        encrypted_data = conn.recv(64000).decode('utf-8')
                        print("received encrypted data" , encrypted_data)
                        plaintxt , received_hashval , reconstructed_hashval = hash_decrypt_triple_SDES(encrypted_data , key)
                        parts = plaintxt.split(' ')
                        user_action = parts[0]
                        if reconstructed_hashval != received_hashval:
                            send_plaintxt = "suspected message tampering. Session ended\n"
                            print(send_plaintxt)
                            conn.send(hash_encrypt_triple_SDES(send_plaintxt , key).encode("utf-8"))
                            break
                        if user_action == "4":  # End session
                            send_plaintxt = "Session ended\n"
                            conn.send(hash_encrypt_triple_SDES(send_plaintxt , key).encode("utf-8"))
                            break  # 

                        if user_action == "1":  # Check balance
                            send_plaintxt = f"Current balance: {balance} USD\n"
                            print("sending over" , (hash_encrypt_triple_SDES(send_plaintxt , key).encode("utf-8")))
                            conn.send(hash_encrypt_triple_SDES(send_plaintxt , key).encode("utf-8"))
                        elif user_action in ["2", "3"]:  # Deposit or Withdraw
                            if len(parts) > 1 and parts[1].isdigit():
                                amount = int(parts[1])
                                if user_action == "2":  # Deposit
                                    balance += amount
                                    send_plaintxt = f"New balance after deposit: {balance} USD\n"
                                    print("attempting to encrypt msg")
                                    c_txt = hash_encrypt_triple_SDES(send_plaintxt , key)
                                    print(send_plaintxt)
                                    print("encrypted plaintxt and trying to send")
                                    conn.send(c_txt.encode('utf-8'))
                                elif user_action == "3":  # Withdraw
                                    if amount <= balance:
                                        balance -= amount
                                        send_plaintxt = f"New balance after withdrawal: {balance} USD\n"
                                        print(send_plaintxt)
                                        conn.send(hash_encrypt_triple_SDES(send_plaintxt , key).encode('utf-8'))
                                    else:
                                        send_plaintxt = "Insufficient funds\n"
                                        print(send_plaintxt)
                                        conn.send(hash_encrypt_triple_SDES(send_plaintxt , key).encode('utf-8'))
                            else:
                                send_plaintxt = "Invalid amount\n"
                                print(send_plaintxt)
                                conn.send(hash_encrypt_triple_SDES(send_plaintxt , key).encode('utf-8'))                        

            except Exception as e:
                print(f"Error occurred: {e}")
                break
            except KeyboardInterrupt :
                print("Server is shutting down.")
                break
            finally:
                conn.close()
                print(f"Connection with {addr} has been closed")
                continue

if __name__ == '__main__':
    
    main()
