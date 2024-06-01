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

def choose_protocol():
    protocol = input("Choose protocol: (1)RSA (2)RSA-OAEP (3)Paillier or enter q to quit\n")
    return protocol
def encrypt_data(protocol, data):
    if protocol == '1':
        return DES.encrypt(data)
    elif protocol == '2':
        return RSA.encrypt(data)
    elif protocol == '3':
        return Paillier.encrypt(data)
    elif protocol == '4':
        return RSA_OAEP.encrypt(data)
    else:
        raise ValueError("Unknown protocol")

def decrypt_data(protocol, encrypted_data):
    if protocol == '1':
        return DES.decrypt(encrypted_data)
    elif protocol == '2':
        return RSA.decrypt(encrypted_data)
    elif protocol == '3':
        return Paillier.decrypt(encrypted_data)
    elif protocol == '4':
        return RSA_OAEP.decrypt(encrypted_data)
    else:
        raise ValueError("Unknown protocol")

    
def receive_message(client):
    data = client.recv(10240000).decode('utf-8')
    return data

    
def main():

    host = 'localhost'
    port = 65432
    continouse_1= True
    while continouse_1:
        try:
            while True:
                p = nextprime(random.getrandbits(32// 2))
                q = nextprime(random.getrandbits(32 // 2))   #for RSA keys
                public, private = RSA.generate_keypair(p, q) #for RSA keys
                print("public key: ", public)
                public_key_OAEP , private_key_OAEP = RSA_OAEP.generate_keypair(2048)
                print("public key for RSA_OAEP: ", public_key_OAEP)# for RSA_OAEP keys
                public_key_P, private_key_P = Paillier.generate_keypair(2048)
                print("public key for Paillier: ", public_key_P)
                print("start a new connection")
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
                    client.connect((host, port))
                    print("Connected to server.")
                    #phrase 1 build the connection 
                    message = "Hello, this is a ATM"
                    client.send(message.encode('utf-8'))
                    time.sleep(1)
                    r1= receive_message(client)
                    print("Server response: ", r1.strip())    
                    protocol = choose_protocol()
                    if protocol == "q":
                        print("Exiting program")
                        continouse_1 = False
                        break
                    elif protocol in ["1", "2", "3"]:
                        client.send(protocol.encode('utf-8'))
                        response = receive_message(client)
                        print("Server response: ", response.strip())
                    else:
                        print("Invalid protocol selected\n")
                        continue
                    if(protocol == "1"):
                        #print("send my public key")
                        client.send(f"{public[0]} {public[1]}\n".encode('utf-8'))
                        public_key =receive_message(client).split()
                        public_key[0]=int(public_key[0])
                        public_key[1]=int(public_key[1])
                        #print("e: %d n: %d" % (public_key[0], public_key[1]))
                        
                        message = '1'
                        encrypted_message = RSA.encrypt(public_key, message)
                        encrypted_message = ', '.join(str(num) for num in encrypted_message) 
                        
                        #print(encrypted_message)
                        client.send(encrypted_message.encode('utf-8'))
                        #print("Encrypted message sent")
                        
                        response = client.recv(100000).decode('utf-8')
                        #print(response)
                        ciphertext = [int(num) for num in response.split(', ')]
                        #print(ciphertext)
                        decrypted_message = RSA.decrypt(private, ciphertext )
                        #print("Server response: ",decrypted_message.strip())
                        key = decrypted_message
                    elif(protocol == "2"):
                        #print("send my public key")
                        client.send(f"{public_key_OAEP[0]} {public_key_OAEP[1]}\n".encode('utf-8'))
                        public_key_server = receive_message(client).split()
                        # public_key_server[0]=int(public_key[0])
                        # public_key_server[1]=int(public_key[1])
                        #print("e:",public_key_server[0]," n: ", public_key_server[1])
                        e_int = int(public_key_server[0])  
                        n_int = int(public_key_server[1])  

                        message = '1'
                        encode_message= RSA_OAEP.oaep_encode(message, n_int)
                        encrypted_msg = [pow(m, e_int, n_int) for m in encode_message]
                        #print("Encoded message", encrypted_msg)
                        encrypted_message = ', '.join(str(num) for num in encrypted_msg) 
                        
                        #print(encrypted_message)
                        client.send(encrypted_message.encode('utf-8'))
                        #print("Encrypted message sent")
                        
                        response = client.recv(10000000000).decode('utf-8')
                        #print(response)
                        ciphertext = [int(num) for num in response.split(', ')]
                        #print(ciphertext)
                        decrypted_encoded_msg = [pow(c, private_key_OAEP[0], private_key_OAEP[1]) for c in ciphertext]
                        decrypted_msg = RSA_OAEP.oaep_decode(bytes(decrypted_encoded_msg), private_key_OAEP[1])
                        #print("Server response: ",decrypted_msg)
                        key = decrypted_msg
                    elif(protocol == "3"):
                        #print("send the p_pulickey\n")
                        client.send(f"{public_key_P[0]} {public_key_P[1]}\n".encode('utf-8'))
                        public_key_server =receive_message(client).split()
                        
                        n_int = int(public_key_server[0])  
                        g_int = int(public_key_server[1])  
                        
                        #print("n_int:", n_int,"g_int:", g_int)
                        
                        m= 1
                        encode_message = Paillier.encrypt((n_int, g_int), m)
                        #encrypted_message = ', '.join(str(num) for num in encode_message)
                        client.send(str(encode_message).encode('utf-8'))
                        
                        response = client.recv(100000000).decode('utf-8')
                        response = int(response)
                        decode_response = Paillier.decrypt(private_key_P,public_key_P, response)
                        #print("Server response: ", decode_response)
                        key = bin(decode_response)[2:]
                        key = (10 - len(key)) * "0" + key
                        #print("client key is" , key)
                        
                        
                    while True:  # 使用 True 循环，确保用户可以连续操作直至选择退出
                        user_choice = input("Select the service you need: 1. Check balance 2. Deposit 3. Withdraw 4. Quit\n")
                        if user_choice == "4":
                            print("Connection closed.")
                            break  
                        if user_choice in ["1", "4"]:  # For check balance and quit, no need to send amount
                            ciphertxt = hash_encrypt_triple_SDES(user_choice, key)
                            client.send(ciphertxt.encode('utf-8'))
                        elif user_choice in ["2", "3"]:  # For deposit and withdraw, need to send amount
                            amount = input("Enter the amount:")
                            if not amount.isdigit() or int(amount) <= 0:
                                print("Invalid amount. Please enter a positive integer.")
                                continue
                            plaintxt = f"{user_choice} {amount}"
                            ciphertxt = hash_encrypt_triple_SDES(plaintxt, key)
                            client.send(ciphertxt.encode('utf-8'))
                        else:
                            print("Invalid selection and quit")
                            break  
                        print("attempting to receive message back")
                        ctxt_response = receive_message(client)
                        response , received_hashval , reconstructed_hashval = hash_decrypt_triple_SDES(ctxt_response , key)
                        if received_hashval != reconstructed_hashval:
                            print("Server repsonse has been tampered with. Shutting down client connection")
                            client.close()
                            break
                        print("Server response: ", response.strip())                     

        except Exception as e:
            print(f"Error occurred: {e}")
            client.close()
            time.sleep(5)  
        except KeyboardInterrupt:
            print("Client is shutting down.")
            continouse_1 = False
        finally:
            client.close()
            print("Connection with server has been closed")

                

if __name__ == '__main__':
    main()
