class Pattern_Three:
    '''
        K
        K A
        K A T
        K A T H
        K A T H M
        K A T H M A
        K A T H M A N
        K A T H M A N D
        K A T H M A N D U
    '''

    def __init__(self, strings='KATHMANDU'):
        if isinstance(strings, str):
            self.strings = strings

        else:  # If provided 'strings' is integer then converting it to string
            self.strings = str(strings)

        self.length = len(self.strings)

    def method_one(self):
        print('\nMethod One')

        for i in range(1, self.length + 1):
            print(' '.join(self.strings[:i]))

    def method_two(self):
        print('\nMethod Two')

        i = 1

        while i != self.length + 1:
            print(' '.join(self.strings[:i]))

            i += 1


if __name__ == '__main__':
    pattern_three = Pattern_Three()

    pattern_three.method_one()
    pattern_three.method_two()
