'''
The number 3797 has an interesting property. Being prime itself, it is
possible to continuously remove digits from left to right, and remain
prime at each stage: 3797, 797, 97, and 7. Similarly we can work from
right to left: 3797, 379, 37, and 3.

Find the sum of the only eleven primes that are both truncatable from
left to right and right to left.

NOTE: 2, 3, 5, and 7 are not considered to be truncatable primes.
'''


def GetPrimes(n):
    primes = []
    temPrimes = [True] * n

    for i in range(2, n):
        if temPrimes[i]:
            primes.append(i)

            for j in range(i, n, i):
                temPrimes[j] = False

    return primes


def isPrime(N):
    if N == 1:
        return False

    for i in range(2, int(N ** 0.5) + 1):
        if N % i == 0:
            return False

    return True


def IsPrimeTruncatable(n):
    base = 10

    while base < n and isPrime(n % base):  # From Right
        base *= 10

    if base < n:
        return False

    while base > 1 and isPrime(n // base):  # From left
        base //= 10

    return base == 1


def GetSum():
    sums = 0
    count = 0
    primes = GetPrimes(1000000)

    for prime in primes:
        if prime > 10 and IsPrimeTruncatable(prime):
            sums += prime
            count += 1

            if count == 11:  # eleven truncatable primes are found
                return sums


print(GetSum())
