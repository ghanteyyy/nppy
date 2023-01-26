'''
The number, 197, is called a circular prime because all rotations of
the digits: 197, 971, and 719, are themselves prime.

There are thirteen such primes below 100: 2, 3, 5, 7, 11, 13, 17, 31,
37, 71, 73, 79, and 97.

How many circular primes are there below one million?
'''


def is_prime(n):
    factors = sum(2 for i in range(1, round(n ** 0.5 + 1)) if not n % i)

    return True if factors == 2 else False


def is_circular_prime(nums):
    for num in nums:
        if not is_prime(num):
            return False

    return True


def rotate(num):
    rotate = []
    nums = str(num)

    for i in range(len(nums)):
        rotate.append(int(nums))
        nums = nums[1:] + nums[0]

    return rotate


def nth_prime_numbers(n):
    prime = []
    sieve = [True] * n

    for p in range(2, n):
        if sieve[p]:
            prime.append(p)

            for i in range(p * p, n, p):
                sieve[i] = False

    return prime


if __name__ == '__main__':
    count = 0
    all_primes = nth_prime_numbers(1000000)

    for prime in all_primes:
        rotation = rotate(prime)

        if is_circular_prime(rotation):
            count += 1

    print(count)
