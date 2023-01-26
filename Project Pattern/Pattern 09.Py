class Pattern_Nine:
    '''
        K
        A
        T
        H
        M
        A
        N
        D
        U
    '''

    def __init__(self, strings='KATHMANDU'):
        if isinstance(strings, str):
            self.strings = strings

        else:  # If provided 'strings' is integer then converting it to string
            self.strings = str(strings)

        self.length = len(self.strings)

    def method_one(self):
        print('\nMethod One')

        for string in self.strings:
            print(string)

    def method_two(self):
        print('\nMethod Two')

        join_word = '\n'.join(self.strings)
        print(join_word)

    def method_three(self):
        print('\nMethod Three')

        x = 0

        while x != self.length:
            print(self.strings[x])

            x += 1


if __name__ == '__main__':
    pattern_nine = Pattern_Nine()

    pattern_nine.method_one()
    pattern_nine.method_two()
    pattern_nine.method_three()
