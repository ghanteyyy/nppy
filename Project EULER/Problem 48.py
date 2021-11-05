'''
The series, 1^1 + 2^2 + 3^3 + ... + 1010 = 10405071317.

Find the last ten digits of the series, 1^1 + 2^2 + 3^3 + ... + 1000^1000.
'''

sums = 0

for i in range(1, 1000 + 1):
    sums += i ** i

print(str(sums)[-10:])
