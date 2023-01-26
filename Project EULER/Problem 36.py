'''
The decimal number, 585 = 10010010012 (binary), is palindromic in both bases.

Find the sum of all numbers, less than one million, which are palindromic in
base 10 and base 2.

(Please note that the palindromic number, in either base, may not include
leading zeros.)
'''


def into_binary(nums):
    binary = ''

    while nums:
        rem = nums % 2
        nums = nums // 2
        binary += str(rem)

    return is_palindrome(binary)


def is_palindrome(num):
    num = str(num)
    return num == num[::-1]


sums = 0


for i in range(1, 1000000):
    if is_palindrome(i) and into_binary(i):
        sums += i

print(sums)
