def pattern_one(strings, steps):
    '''Pattern one

        If you enter "1" then you will get

            1
            1 1
            1 1 1
            1 1 1 1
            1 1 1 1 1
            1 1 1 1 1 1
            1 1 1 1 1 1 1


        or SIMILAR
    '''

    if not str(strings).isalpha():
        strings = str(strings)  # If provided is integer then converting to string

    for line in range(1, steps):
        print(((strings + ' ') * line).strip(' '))


if __name__ == '__main__':
    try:
        pattern_one('1', 10)

    except NameError:
        print('String and Integer was expected')
