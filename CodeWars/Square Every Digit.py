def square_digits(num):
    return int(''.join([str(int(n) ** 2) for n in str(num)]))


print(square_digits(9119))   # 811181
print(square_digits(0))      # 0
