import random

# Simplified DES Algorithm Implementation Helpers
def permute(k, arr, n):
    permutation = ""
    for i in range(0, n):
        permutation += k[arr[i] - 1]
    return permutation

def shift_left(k, shifts):
    s = ""
    for i in range(shifts):
        for j in range(1, len(k)):
            s += k[j]
        s += k[0]
        k = s
        s = ""
    return k

def xor(a, b):
    ans = ""
    for i in range(len(a)):
        if a[i] == b[i]:
            ans += "0"
        else:
            ans += "1"
    return ans

def s_box(sbox, row, col):
    return format(sbox[row][col], '02b')

def key_generation(p10, p8, key):
    key = permute(key, p10, 10)
    left = key[:5]
    right = key[5:]
    left = shift_left(left, 1)
    right = shift_left(right, 1)
    key1 = permute(left + right, p8, 8)
    left = shift_left(left, 2)
    right = shift_left(right, 2)
    key2 = permute(left + right, p8, 8)
    return key1, key2

def function_fk(part, sk, s0, s1):
    ep = [4, 1, 2, 3, 2, 3, 4, 1]
    part = permute(part, ep, 8)
    part = xor(part, sk)
    left = part[:4]
    right = part[4:]
    row1 = int(left[0] + left[3], 2)
    col1 = int(left[1] + left[2], 2)
    row2 = int(right[0] + right[3], 2)
    col2 = int(right[1] + right[2], 2)
    result = s_box(s0, row1, col1) + s_box(s1, row2, col2)
    p4 = [2, 4, 3, 1]
    result = permute(result, p4, 4)
    return result

def s_des_encrypt(plaintext, key1, key2, ip, ip_inv, s0, s1):
    plaintext = permute(plaintext, ip, 8)
    left = plaintext[:4]
    right = plaintext[4:]
    left = xor(left, function_fk(right, key1, s0, s1))
    left, right = right, left  # Swap
    left = xor(left, function_fk(right, key2, s0, s1))
    result = permute(left + right, ip_inv, 8)
    return result

# Differential Cryptanalysis

# ad and bc
def build_sbox_differential_table(sbox):
    # initialize the differential table with all zeros for a 4x4 S-box
    ddt = [[0 for _ in range(len(sbox)*len(sbox[0]))] for _ in range(len(sbox)*len(sbox[0]))]
    for x1 in range(len(sbox)*len(sbox[0])):
        for x2 in range(len(sbox)*len(sbox[0])):
            # input different
            dx = x1 ^ x2
            # use it for sbox index
            left = f"{x2:04b}"
            right = f"{x1:04b}"
            row1 = int(left[0] + left[3], 2)
            col1 = int(left[1] + left[2], 2)
            row2 = int(right[0] + right[3], 2)
            col2 = int(right[1] + right[2], 2)

            # calculate the output difference
            dy = sbox[row1][col1] ^ sbox[row2][col2]
            # increment the count of the observed output difference for the given input difference
            ddt[dx][dy] += 1
    return ddt

def get_candidate_keys(sbox, ddt):
    candidate_keys = [set(range(16)) for _ in range(16)]  # 对于每个可能的输入差分，初始化候选密钥集合
    for _ in range(100):  # 使用100个随机输入
        input_val = random.randint(0, 15)
        
        for input_diff in range(16):
            input_val_prime = input_val ^ input_diff
            for key_guess in range(16):
                # 假设key_guess是S盒的输入，这里简化处理，实际上您需要考虑如何将密钥应用到S盒的输入
                # 计算S盒输出和输出差分
                output_val = sbox[input_val // 4][input_val % 4]  # 获取S盒输出
                output_val_prime = sbox[input_val_prime // 4][input_val_prime % 4]
                output_diff = output_val ^ output_val_prime
                
                # 检查DDT中对应的条目是否表明这个差分是可能的
                if ddt[input_diff][output_diff] > 0:
                    # 如果是，添加key_guess到对应输入差分的候选密钥集合
                    candidate_keys[input_diff].add(key_guess)
                # 无需从集合中移除不可能的密钥，因为初始时所有可能的密钥都已经包含在集合中

    return candidate_keys


# Update the reduce_candidate_keys function to handle the reduced key sets correctly


def reduce_candidate_keys(candidate_keys_sets):
    reduced_keys = [set() for _ in range(16)]  # Initialize for 16 possible input differences
    for i in range(16):  # Assuming 16 possible input differences for simplicity
        # Intersect across all provided candidate key sets for this particular input difference
        if candidate_keys_sets:  # Check if candidate key sets are not empty
            reduced_keys[i] = set.intersection(*[keys[i] for keys in candidate_keys_sets])
    return reduced_keys

# Update the construct_final_key function to handle the reduced key sets correctly
def construct_final_key(candidate_keys_round1, candidate_keys_round2):
    final_key = 0
    # Combine the reduced keys from both rounds
    combined_keys = candidate_keys_round1 + candidate_keys_round2
    for i, key_set in enumerate(combined_keys):
        if key_set:  # Check if there is any candidate key
            key_value = next(iter(key_set))  # Arbitrarily choose a key if more than one, for demonstration
            final_key |= (key_value << (4 * (len(combined_keys) - 1 - i)))  # Adjust bit position based on index
            print("Final Key: ", final_key)
    return final_key



# Example usage
s2 = [[1, 0, 2, 3], [3, 1, 0, 2], [2, 0, 3, 1], [1, 3, 2, 0]]
s0 = [[1, 0, 3, 2], [3, 2, 1, 0], [0, 2, 1, 3], [3, 1, 3, 2]]
s1 = [[0, 1, 2, 3], [2, 0, 1, 3], [3, 0, 1, 0], [2, 1, 0, 3]]
# build the differential table for each S-box
differential_table_s0 = build_sbox_differential_table(s0)
differential_table_s1 = build_sbox_differential_table(s1)
differential_table_s2 = build_sbox_differential_table(s2)
print("Differentail Table S0")
for row in differential_table_s0:
    print(row)
print("Differentail Table S1")
for row in differential_table_s1:
    print(row)

key = "1100011110"
ip = [2, 6, 3, 1, 4, 8, 5, 7]
ip_inv = [4, 1, 3, 5, 7, 2, 8, 6]
p10 = [3, 5, 2, 7, 4, 10, 1, 9, 8, 6]
p8 = [6, 3, 7, 4, 8, 5, 10, 9]
key1, key2 = key_generation(p10, p8, key)

print("key generation: ",key1,key2)
print(xor(key1,key2))

test_plaintext = '00101000'
test_ciphertext = s_des_encrypt(test_plaintext, key1,key2, ip,ip_inv,s0,s1 )  # Placeholder for the expected ciphertext
print("test ciphertext: ",test_ciphertext)

S0_left = 
# Generate candidate keys for each half of each round
candidate_keys_round1_left = get_candidate_keys(s0, differential_table_s0)
print("candidate keys: ",candidate_keys_round1_left)
candidate_keys_round1_right = get_candidate_keys(s1, differential_table_s1)
print("candidate keys: ",candidate_keys_round1_right)
candidate_keys_round2_left = get_candidate_keys(s0, differential_table_s0)
print("candidate keys: ",candidate_keys_round2_left)
candidate_keys_round2_right = get_candidate_keys(s1, differential_table_s1)
print("candidate keys: ",candidate_keys_round2_right)

# Reduce candidate keys by finding the intersection of candidate key sets for each part
reduced_keys_round1 = reduce_candidate_keys([candidate_keys_round1_left, candidate_keys_round1_right])
reduced_keys_round2 = reduce_candidate_keys([candidate_keys_round2_left, candidate_keys_round2_right])
print("Reduced Keys Round 1: ", reduced_keys_round1)
print("Reduced Keys Round 2: ", reduced_keys_round2)

# Construct the final key from the reduced key sets of both rounds
final_key = construct_final_key(reduced_keys_round1, reduced_keys_round2)
final_key_bin = format(final_key, '016b')  # Convert final key to binary format

print("Final Key:", final_key_bin)
print("Original Key:", key)
    
