def pattern_twelve(strings):
    '''Pattern three

        If you input "KATHMANDU" then you get

                U
                D U
                N D U
                A N D U
                M A N D U
                H M A N D U
                T H M A N D U
                A T H M A N D U
                K A T H M A N D U

        or SIMILAR
    '''

    if not str(strings).isalpha():
        strings = str(strings)  # If provided is integer then converting to string

    for x in range(1, len(strings) + 1):
        print(' '.join(strings[-x:]))

    '''Another Way to do the same thing
            string = 'KATHMANDU'

            for i in range(len(string) - 1, -1, -1):
                print(' '.join(string[i:])) '''


if __name__ == '__main__':
    try:
        pattern_twelve('KATHMANDU')

    except NameError:
        print('String or Integer was expected')
