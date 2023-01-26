'''
An irrational decimal fraction is created by concatenating the positive integers:

0.123456789101112131415161718192021...

It can be seen that the 12th digit of the fractional part is 1.

If dn represents the nth digit of the fractional part, find the value of
the following expression.

d1 × d10 × d100 × d1000 × d10000 × d100000 × d1000000
'''

num = 1
sums = 1
count = 0
fractional_part = ''

# Contacting value from 1 to until the length reaches 1000000
while len(fractional_part) <= 1000000:
    count += 1
    fractional_part += str(count)

# Getting value from respective index 1, 10, etc and getting its product
while num != 1000000:
    sums *= int(fractional_part[num - 1])
    num *= 10

print(sums)
