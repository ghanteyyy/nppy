'''
A palindromic number reads the same both ways. The largest palindrome
made from the product of two 2-digit numbers is 9009 = 91 × 99.

Find the largest palindrome made from the product of two 3-digit numbers.
'''


def is_palindrome(i, j):
    product = str(i * j)

    return product == product[::-1]


li = [i * j for i in range(900, 1000) for j in range(900, 1000) if is_palindrome(i, j)]

print(max(li))
