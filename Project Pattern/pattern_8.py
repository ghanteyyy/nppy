def pattern_eight(strings):
    '''Pattern seven

        If you provide 'Programming' in strings then you get
                    P
                    P r
                    P r o
                    P r o g
                    P r o g r
                    P r o g r a
                    P r o g r a m
                    P r o g r a m m
                    P r o g r a m m i
                    P r o g r a m m i n
                    P r o g r a m m i n g
                    P r o g r a m m i n
                    P r o g r a m m i
                    P r o g r a m m
                    P r o g r a m
                    P r o g r a
                    P r o g r
                    P r o g
                    P r o
                    P r
                    P
    '''

    if not str(strings).isalpha():
        strings = str(strings)

    length = len(strings)

    for i in range(1, length + 1):
        print(' '.join(strings[:i]))

        if i == length:
            for j in range(length - 1, 0, -1):
                print(' '.join(strings[:j]))


if __name__ == '__main__':
    try:
        pattern_eight('Programming')

    except NameError:
        print('String or Integer was expected')
