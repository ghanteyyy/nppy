class Pattern_Twenty:
    '''
        P r o g r a m m i n g
        r o g r a m m i n
        o g r a m m i
        g r a m m
        r a m
        a
    '''

    def __init__(self, strings='Programming'):
        if not isinstance(strings, str):
            strings = str(strings)

        for index, value in enumerate(strings):
            output = strings[index:len(strings) - index]

            if output:
                print(output)


if __name__ == '__main__':
    Pattern_Twenty()
