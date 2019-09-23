def pattern_twenty(strings):
    '''Pattern Twentry

        If you input "Programming" then you will get

            K A T H M A N D U
            A T H M A N D
            T H M A N
            H M A
            M

        or SIMILAR
    '''

    strings = str(strings)

    for index, value in enumerate(strings):
        output = strings[index:len(strings) - index]

        if len(output) != 0:
            print(' '.join(output))


if __name__ == '__main__':
    pattern_twenty('KATHMANDU')
