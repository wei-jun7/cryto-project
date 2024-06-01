import hw1 as DES
import random
from sympy import mod_inverse
p = 173
q = 7
N = p * q
e = 7
phi_N = (p - 1) * (q - 1)
d = mod_inverse(e, phi_N)
public_key = (e, N)
private_key = (d, N)
p10 = [3, 5, 2, 7, 4, 10, 1, 9, 8, 6]
p8 = [6, 3, 7, 4, 8, 5, 10, 9]
ip = [2, 6, 3, 1, 4, 8, 5, 7]
ip_inv = [4, 1, 3, 5, 7, 2, 8, 6]
key = "1100011110" 
DES_key =(DES.key_generation(p10, p8, key))


def Encrypt_semantic_secure_RSA(msg, DES_key, public_key):
    random.seed(0)  # 确保随机数生成器的可预测性，仅用于示例

    # RSA 公钥
    e, N = public_key
    
    # 生成随机数并加密
    r = random.randint(1, N-1)
    r_encrypted = pow(r, e, N)  # 使用RSA公钥加密随机数r
    
    # 使用s-DES加密随机数生成哈希值
    r_bits = format(r, '08b')  # 将随机数转换为8位二进制
    hash_value = DES.s_des_encrypt(r_bits, DES_key[0], DES_key[1], p10, p8)  # 假设DES_key是一个元组，包含key1和key2
    
    # 将消息的每个字符与哈希值进行XOR操作
    encrypted_msg = ''
    for char in msg:
        char_bits = DES.convert_to_binary(char)
        encrypted_char = DES.xor(char_bits, hash_value)
        encrypted_msg += encrypted_char
    
    # 返回加密后的随机数和加密后的消息
    return r_encrypted, encrypted_msg

def Decrypt_semantic_secure_RSA(encrypted_data, DES_key, private_key):
    r_encrypted, encrypted_msg = encrypted_data
    d, N = private_key  # RSA 私钥
    
    # 使用RSA私钥解密随机数
    r_decrypted = pow(r_encrypted, d, N)
    
    # 再次使用s-DES加密解密后的随机数生成哈希值
    r_bits = format(r_decrypted, '08b')
    hash_value = DES.s_des_encrypt(r_bits, DES_key[0], DES_key[1], p10, p8)
    
    # 将加密的消息与哈希值进行XOR操作以解密
    decrypted_msg = ''
    for i in range(0, len(encrypted_msg), 8):  # 假设加密的消息是连续的二进制字符串
        encrypted_char = encrypted_msg[i:i+8]
        decrypted_char_bits = DES.xor(encrypted_char, hash_value)
        decrypted_char = chr(int(decrypted_char_bits, 2))
        decrypted_msg += decrypted_char
    
    return decrypted_msg

# 初始化RSA和DES数据
  # 假设你已经通过DES.key_generation生成了key1和key2

# 加密和解密示例
encrypted_data = Encrypt_semantic_secure_RSA("NETSEC", DES_key, public_key)
decrypted_msg = Decrypt_semantic_secure_RSA(encrypted_data, DES_key, private_key)

print("Encrypted data:", encrypted_data)
print("Decrypted message:", decrypted_msg)
