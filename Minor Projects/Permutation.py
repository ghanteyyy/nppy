import math


class Permutation:
    '''
    Formula to calculate permutation.
        P(n,r) = n! / (n-r)!   ; n > r

            where, n = total number of arrangements
                   r = difference of arrangements
                   ! = factorial of the number  eg: 4! = 4 * 3 * 2 * 1 = 24
    '''

    def __init__(self, number, difference):
        self.number = number
        self.difference = difference

    def factorial(self, num):
        '''
        See more about factorial in factorial.py
        '''

        return math.factorial(num)

    def get_permutation(self):
        '''
        Calculating permutation of the given number and difference
        '''

        if self.difference > self.number:
            return 'Number must be greater than difference'

        n = self.factorial(self.number)
        r = self.factorial(self.number - self.difference)

        return n // r     # Here r is equivalent to n - r


if __name__ == '__main__':
    permutation = Permutation(18, 6)
    print(permutation.get_permutation())
