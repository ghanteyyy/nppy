class Pattern_Eight:
    '''
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

    def __init__(self, strings='Programming'):
        if isinstance(strings, str):
            self.strings = strings

        else:  # If provided 'strings' is integer then converting it to string
            self.strings = str(strings)

        self.length = len(self.strings)

    def method_one(self):
        print('\nMethod One')

        for i in range(1, self.length + 1):
            print(' '.join(self.strings[:i]))

            if i == self.length:
                for j in range(self.length - 1, 0, -1):
                    print(' '.join(self.strings[:j]))

    def method_two(self):
        print('\nMethod Two')

        i, j = 1, self.length - 1

        while i != self.length + 1:
            print(' '.join(self.strings[:i]))

            if i == self.length:
                while j != 0:
                    print(' '.join(self.strings[:j]))

                    j -= 1

            i += 1


if __name__ == '__main__':
    pattern_eight = Pattern_Eight()

    pattern_eight.method_one()
    pattern_eight.method_two()
