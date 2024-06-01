from sympy import symbols, mod_inverse

# 初始化所需的常数和份额
p = 31847  # 素数P
shares = [(413, 25439), (432, 14847), (451, 24780), (470, 5910), (489, 12734)]

# 拉格朗日插值计算秘密（f(0)）
def lagrange_interpolation(x, shares, p):
    n = len(shares)
    x_values, y_values = zip(*shares)
    secret = 0

    for i in range(n):
        xi, yi = shares[i]
        term = yi

        for j in range(n):
            if i != j:
                xj = shares[j][0]
                # (x - xj) / (xi - xj)
                numerator = x - xj
                denominator = xi - xj
                term = term * numerator * mod_inverse(denominator, p) % p

        secret = (secret + term) % p

    return secret

# 计算秘密
secret_key = lagrange_interpolation(0, shares, p)
print(secret_key)
# 计算给定 x 坐标等于 10000 的参与者的份额
x_coord = 10000
share_at_x_10000 = lagrange_interpolation(x_coord, shares, p)
print(share_at_x_10000)
