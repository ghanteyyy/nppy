def pattern_twenty(strings):
    '''Pattern twenty

        P r o g r a m m i n g
        r o g r a m m i n
        o g r a m m i
        g r a m m
        r a m
        a
    '''

    strings = str(strings)
    print()

    for index, value in enumerate(strings):
        output = strings[index:len(strings) - index]

        if len(output) != 0:
            print(output)


if __name__ == '__main__':
    pattern_twenty('Programming')
