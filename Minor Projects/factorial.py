import math


def factorial(number):
    '''Calculate factorial

    Factorial is the product of an integer and all the integers below. It is represented also by '!'
        Example: Factorial of 5 or 5! = 5 * 4 * 3 * 2 * 1
                                    = 120
    '''

    def method_one(number):
        get_factorial = 1

        for num in range(1, number + 1):
            get_factorial *= num
            num -= 1

        print('Factorial of {} is {} \n'.format(number, get_factorial))

    def method_two(number):
        get_factorial = math.factorial(number)
        print('Factorial of {} is {} \n'.format(number, get_factorial))

    print('Method one')
    method_one(number)

    print('Method two')
    method_two(number)


if __name__ == '__main__':
    try:
        factorial(5)

    except (ValueError, NameError):
        print('Integer value was excepted')
