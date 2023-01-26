class Pattern_One:
    '''
        1
        1 1
        1 1 1
        1 1 1 1
        1 1 1 1 1
        1 1 1 1 1 1
        1 1 1 1 1 1 1
    '''

    def __init__(self, strings='1', steps=10):
        self.steps = steps

        if isinstance(strings, str):
            self.strings = strings

        else:  # If provided 'strings' is integer then converting it to string
            self.strings = str(strings)

    def method_one(self):
        print('\nMethod One')

        for i in range(1, self.steps):
            print(' '.join(self.strings * i))

    def method_two(self):
        print('\nMethod Two')

        i = 1

        while i != self.steps:
            print(' '.join(self.strings * i))

            i += 1

    def method_three(self):
        print('\nMethod Three')

        for i in range(1, self.steps):
            for j in range(1, i + 1):
                print(self.strings, end=' ')

            print('\n', end='')


if __name__ == '__main__':
    pattern_one = Pattern_One()

    pattern_one.method_one()
    pattern_one.method_two()
    pattern_one.method_three()
