def pattern_two(strings, steps):
    '''Pattern two

        1 1 1 1 1 1 1
        1 1 1 1 1 1
        1 1 1 1 1
        1 1 1 1
        1 1 1
        1 1
        1

    '''

    if not str(strings).isalpha():
        strings = str(strings)  # If provided is integer then converting to string

    def method_one(strings, steps):
        while steps > 0:
            print(((strings + ' ') * steps).strip(' '))
            steps -= 1

    def method_two(strings, steps):
        for step in range(steps, 0, -1):
            print(((strings + ' ') * step).strip(' '))

    print('Method One')
    method_one(strings, steps)

    print('\n\nMethod Two')
    method_two(strings, steps)


if __name__ == '__main__':
    try:
        pattern_two('1', 10)

    except NameError:
        print('String and Integer was expected')
