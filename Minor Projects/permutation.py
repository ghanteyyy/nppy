import math


def permutation(number, difference):
    '''
       Formula to calulate permutation.
               P(n,r) = n! / (n-r)!   ; n > r

                    where, n = total number of arrangements
                           r = difference of arrangements
                           ! = factorial of the number  eg: 4! = 4 * 3 * 2 * 1 = 24
    '''

    try:
        if difference > number:
            print('Difference is greater than Number')

        else:
            num = math.factorial(number)
            diff = math.factorial(number - difference)

            permutation = int(num / diff)
            print(permutation)

    except (ValueError, NameError):
        print('Integer value was expected')

    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    permutation(18, 6)
