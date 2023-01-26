'''
We shall say that an n-digit number is pandigital if it makes use of all
the digits 1 to n exactly once. For example, 2143 is a 4-digit pandigital
and is also prime.

What is the largest n-digit pandigital prime that exists?
'''


def seivePrimes(n):
    primes = []
    temPrimes = [True] * n

    for i in range(2, n):
        if temPrimes[i]:
            primes.append(i)

            for j in range(i, n, i):
                temPrimes[j] = False

    return primes


def isPandigitalPrime(n):
    n = str(n)

    for i in range(1, len(n) + 1):
        if not str(i) in n:
            return False

    return True


largest = 0
n = 10000000
primes = seivePrimes(n)

for prime in primes[::-1]:
    if isPandigitalPrime(prime):
        largest = prime
        break

print(largest)
