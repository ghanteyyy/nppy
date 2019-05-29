def pattern_four(strings):
    '''Pattern four

        If you input "KATHMANDU" then you get

            K A T H M A N D U
            K A T H M A N D
            K A T H M A N
            K A T H M A
            K A T H
            K A T
            K A
            K


        or SIMILAR
    '''

    if not str(strings).isalpha():
        strings = str(strings)  # If provided is integer then converting to string

    for i in range(len(strings) + 1, 0, -1):
        print(' '.join(strings[:i]))


if __name__ == '__main__':
    try:
        pattern_four('KATHMANDU')

    except NameError:
        print('String or Integer was expected')
