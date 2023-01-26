class Pattern_Seventeen:
    ''' 
        1 2 3 4 5 6 7 8 9
        1 2 3 4 5 6 7 8
        1 2 3 4 5 6 7
        1 2 3 4 5 6
        1 2 3 4 5
        1 2 3 4
        1 2 3
        1 2
        1
    '''

    def __init__(self, steps=9):
        self.steps = steps

    def method_one(self):
        print('\nMethod One')

        _range = [str(i) for i in range(1, self.steps + 1)]

        for i in range(len(_range), 0, -1):
            print(' '.join(_range[:i]))

    def method_two(self):
        print('\nMethod Two')

        for i in range(self.steps + 1, 0, -1):
            for j in range(1, i):
                print(j, end=' ')

            print()


if __name__ == '__main__':
    pattern_seventeen = Pattern_Seventeen()

    pattern_seventeen.method_one()
    pattern_seventeen.method_two()
