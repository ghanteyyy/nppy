def fibonascci(first_value, second_value, steps):
    ''' Fibonacci number is a series of numbers in which each number is the sum of the two preceding numbers.
                The simplest series is 1, 1, 2, 3, 5, 8, etc. '''

    try:
        for _ in range(steps):
            print(first_value)

            third_value = first_value + second_value
            first_value = second_value
            second_value = third_value

            '''Here, first_value will be second_value
                        and
                second_value will be third_value '''

    except (ValueError, NameError):
        print('Integer value was excepted')


if __name__ == '__main__':
    fibonascci(2, 3, 10)
