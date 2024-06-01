# define the function
def jacobi(a, n):
    if a == 0:
        return 0 if n > 1 else 1
    if a == 2:
        return (-1) ** ((n ** 2 - 1) // 8)
    if a == -1:
        return (-1) ** ((n - 1) // 2)
    if a < 0:
        return jacobi(-a, n) * (-1) ** ((n - 1) // 2)
    if a % 2 == 0:
        return jacobi(2, n) * jacobi(a // 2, n)
    if a >= n:
        return jacobi(a % n, n)
    if a % n != a:
        return jacobi(a % n, n)
    if pow(a, (n - 1) // 2, n) == 1:
        return 1
    return -1

#
def jacobi_symbol(a, n):
    if n <= 0 or n % 2 == 0:
        return 0  # invalid symbol
    result = 1
    if a < 0:
        a = -a
        if n % 4 == 3:
            result = -result
    while a != 0:
        while a % 2 == 0:
            a = a // 2
            if n % 8 in [3, 5]:
                result = -result
        a, n = n, a  # apply quadratic reciprocity
        if a % 4 == 3 and n % 4 == 3:
            result = -result
        a = a % n
        if a > n // 2:
            a = a - n
    if n == 1:
        return result
    return 0

# calculate the jacobi symbol
jacobi_values = {
    'a': jacobi_symbol(700, 1617),
    'b': jacobi_symbol(100, 173),
    'c': jacobi_symbol(1000, 173),
    'd': jacobi_symbol(1000, 171),
}

print(jacobi_values)
