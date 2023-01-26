'''
By listing the first six prime numbers: 2, 3, 5, 7, 11, and 13, we can
see that the 6th prime is 13.

What is the 10 001st prime number?
'''


import math


def primes(n):
    sums, sieve = [], [True] * n

    for p in range(2, n):
        if sieve[p]:
            sums.append(p)

            for i in range(p * p, n, p):
                sieve[i] = False

    return sums


if __name__ == '__main__':
    nth_prime = 10001
    upper_bound = int(nth_prime * math.log(nth_prime) + nth_prime * math.log(math.log(nth_prime)))
    _primes = primes(upper_bound)
    print(_primes[10000])
