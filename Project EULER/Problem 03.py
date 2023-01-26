'''
The prime factors of 13195 are 5, 7, 13 and 29.

What is the largest prime factor of the number 600851475143 ?
'''


def get_factors(numbers):
    '''Get factors of given number'''

    factors = [num for num in range(1, int(numbers ** 0.5) + 1) if numbers % num == 0]
    return factors


if __name__ == '__main__':
    factors = get_factors(600851475143)   # Storing all factors of 600851475143
    prime_factors = [fact for fact in factors if len(get_factors(fact)) == 1]  # Getting only prime factors of 600851475143
    print(max(prime_factors))  # Getting maximum prime factors
