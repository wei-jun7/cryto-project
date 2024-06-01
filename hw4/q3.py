def lagrange_interpolation(x, y, p):
    t = len(x)
    secret = 0
    for i in range(t):
        term = y[i]
        for j in range(t):
            if i != j:
                term = term * (-x[j] * pow(x[i] - x[j], -1, p)) % p
        secret = (secret + term) % p
    return secret

def compute_new_share(x, y, x_new, p):
    t = len(x)
    y_new = 0
    for i in range(t):
        term = y[i]
        for j in range(t):
            if i != j:
                term = term * ((x_new - x[j]) * pow(x[i] - x[j], -1, p)) % p
        y_new = (y_new + term) % p
    return y_new


x = [413, 432, 451, 470, 489]
y = [25439, 14847, 24780, 5910, 12734]
p = 31847

secret = lagrange_interpolation(x, y, p)
print("Secret is:",secret)

x_new = 10000
new_share = compute_new_share(x, y, x_new, p)
print("New share is:", new_share)
