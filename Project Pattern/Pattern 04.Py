class Pattern_Four:
    '''
        K A T H M A N D U
        K A T H M A N D
        K A T H M A N
        K A T H M A
        K A T H
        K A T
        K A
        K
    '''

    def __init__(self, strings='KATHMANDU'):
        if isinstance(strings, str):
            self.strings = strings

        else:  # If provided 'strings' is integer then converting it to string
            self.strings = str(strings)

        self.length = len(self.strings)

    def method_one(self):
        print('\nMethod One')

        for i in range(self.length, 0, -1):
            print(' '.join(self.strings[:i]))

    def method_two(self):
        print('\nMethod Two')

        i = self.length

        while i:
            print(' '.join(self.strings[:i]))

            i -= 1


if __name__ == '__main__':
    pattern_four = Pattern_Four()

    pattern_four.method_one()
    pattern_four.method_two()
