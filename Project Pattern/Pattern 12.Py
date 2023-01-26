class Pattern_Twelve:
    '''
        U
        D U
        N D U
        A N D U
        M A N D U
        H M A N D U
        T H M A N D U
        A T H M A N D U
        K A T H M A N D U
    '''

    def __init__(self, strings='KATHMANDU'):
        if isinstance(strings, str):
            self.strings = strings

        else:  # If provided 'strings' is integer then converting it to string
            self.strings = str(strings)

        self.length = len(self.strings)

    def method_one(self):
        print('Method One')

        for x in range(1, self.length + 1):
            print(' '.join(self.strings[-x:]))

    def method_two(self):
        print('\nMethod Two')

        for x in range(self.length - 1, -1, -1):
            print(' '.join(self.strings[x:]))

    def method_three(self):
        print('\nMethod Three', end='')

        x = self.length

        while x != -1:
            print(' '.join(self.strings[x:]))

            x -= 1


if __name__ == '__main__':
    pattern_twelve = Pattern_Twelve()

    pattern_twelve.method_one()
    pattern_twelve.method_two()
    pattern_twelve.method_three()
