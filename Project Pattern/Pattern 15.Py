class Pattern_Fifteen:
    ''' Pattern fifteen

        1
        1 2
        1 2 3
        1 2 3 4
        1 2 3 4 5
        1 2 3 4 5 6
        1 2 3 4 5 6 7
        1 2 3 4 5 6 7 8
        1 2 3 4 5 6 7 8 9
    '''

    def __init__(self, steps=10):
        self.steps = steps

    def method_one(self):
        print('\nMethod One')

        _range = [str(i) for i in range(1, self.steps + 1)]

        for i in range(1, len(_range)):
            print(' '.join(_range[:i]))

    def method_two(self):
        print('\nMethod Two')

        for i in range(1, self.steps):
            for j in range(1, i + 1):
                print(j, end=' ')

            print()


if __name__ == '__main__':
    pattern_fifteen = Pattern_Fifteen()

    pattern_fifteen.method_one()
    pattern_fifteen.method_two()
