'''
2 ^ 15 = 32768 and the sum of its digits is 3 + 2 + 7 + 6 + 8 = 26.

What is the sum of the digits of the number 2 ^ 1000?
'''

values = list(str(2 ** 1000))
int_values = [int(value) for value in values]
sums = sum(int_values)
print(sums)
