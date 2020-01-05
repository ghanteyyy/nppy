def pattern_elevan(strings):
    '''Pattern elevan

        K A T H M A N D U
        A T H M A N D U
        T H M A N D U
        H M A N D U
        M A N D U
        A N D U
        N D U
        D U
        U
    '''

    if not str(strings).isalpha():
        strings = str(strings)  # If provided is integer then converting to string

    for x in range(len(strings)):
        get_string = ' '.join(strings[x:])
        print(get_string)


if __name__ == '__main__':
    try:
        pattern_elevan('KATHMANDU')

    except NameError:
        print('String or Integer was expected')
