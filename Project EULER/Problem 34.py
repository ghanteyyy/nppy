'''
145 is a curious number, as 1! + 4! + 5! = 1 + 24 + 120 = 145.

Find the sum of all numbers which are equal to the sum of the
factorial of their digits.

Note: As 1! = 1 and 2! = 2 are not sums they are not included.
'''


def factorial(nums):
    _nums = nums
    factorial = 0

    while _nums != 0:
        fact = 1
        num = _nums % 10

        if num in values:
            fact *= values[num]

        else:
            for n in range(2, num + 1):
                fact *= n

            values[_nums] = fact

        factorial += fact
        _nums = _nums // 10

    return nums == factorial


sums = 0
values = {}

for i in range(10, 1854721):
    if factorial(i):
        sums += i


print(sums)
