'''
Let d(n) be defined as the sum of proper divisors of n (numbers less
than n which divide evenly into n). If d(a) = b and d(b) = a, where
a ≠ b, then a and b are an amicable pair and each of a and b are
called amicable numbers.

For example, the proper divisors of 220 are 1, 2, 4, 5, 10, 11, 20,
22, 44, 55 and 110; therefore d(220) = 284. The proper divisors of
284 are 1, 2, 4, 71 and 142; so d(284) = 220.

Evaluate the sum of all the amicable numbers under 10000.
'''

amicable_pair = []


def get_factors(num):
    factors = set()

    for n in range(1, int(num ** 0.5) + 1):
        if num % n == 0:
            factors.add(n)
            factors.add(num // n)

    if len(factors) != 1:
        factors.remove(num)

    return factors


for i in range(1, 10000):
    if i not in amicable_pair:
        a = sum(get_factors(i))
        b = sum(get_factors(a))

        if i != a and b == i:
            amicable_pair.extend([a, b])


print(sum(amicable_pair))
