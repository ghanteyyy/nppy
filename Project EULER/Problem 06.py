'''
The sum of the squares of the first ten natural numbers is,

1^2 + 2^2 + ... + 10^2 = 385
The square of the sum of the first ten natural numbers is,

(1 + 2 + ... + 10)^2 = 55^2 = 3025
Hence the difference between the sum of the squares of the first ten
natural numbers and the square of the sum is 3025 − 385 = 2640.

Find the difference between the sum of the squares of the first one
hundred natural numbers and the square of the sum.
'''

squaring_each_number_and_sum = sum([i ** 2 for i in range(1, 101)])  # Square each number and return sums
get_sum_and_square_them = sum(range(1, 101)) ** 2

result = get_sum_and_square_them - squaring_each_number_and_sum
print(result)
