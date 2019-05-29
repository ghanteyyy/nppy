def multiples(number):
    '''Get multiplication of a given number'''

    try:
        for x in range(1, 11):
            print('{} * {}  = {}'.format(number, x, number * x))

    except (ValueError, NameError):
        print('Integer value was expected')


if __name__ == '__main__':
    multiples(10)
