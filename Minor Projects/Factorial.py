import math


class Factorial:
    '''
    Factorial is the product of an integer and all the integers below.
    It is represented also by '!'
        Example: Factorial of 5 or 5! = 5 * 4 * 3 * 2 * 1
                                      = 120
    '''

    def __init__(self, number=5):
        self.number = number

    def method_one(self):
        '''
        Using while loop
        '''

        get_factorial = 1
        nums = self.number

        while nums != 1:
            get_factorial *= nums
            nums -= 1

        return f'{self.number}! = {get_factorial}'

    def method_two(self):
        '''
        Using for loop
        '''

        get_factorial = 1

        for num in range(1, self.number + 1):
            get_factorial *= num

        return f'{self.number}! = {get_factorial}'

    def method_three(self):
        '''
        Using built-in "math" module
        '''

        get_factorial = math.factorial(self.number)
        return f'{self.number}! = {get_factorial}'

    def method_four(self, number):
        '''
        Using recursive method
        '''

        if number == 1:
            return number

        return number * self.method_four(number - 1)


if __name__ == '__main__':
    factorial = Factorial()

    print('\nMethod One')
    print(factorial.method_one())

    print('\nMethod Two')
    print(factorial.method_two())

    print('\nMethod Three')
    print(factorial.method_three())

    print('\nMethod Four')
    print(factorial.method_four(factorial.number))
