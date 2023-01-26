'''
The sum of the primes below 10 is 2 + 3 + 5 + 7 = 17.

Find the sum of all the primes below two million.
'''


def summation_of_primes(n):
    sums, sieve = 0, [True] * n
    for p in range(2, n):
        if sieve[p]:
            sums += p
            for i in range(p * p, n, p):
                sieve[i] = False
    print(sums)


if __name__ == '__main__':
    summation_of_primes(2000000)
