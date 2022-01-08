class Pattern_Sixteen:
    ''' Pattern sixteen

        9
        9 8
        9 8 7
        9 8 7 6
        9 8 7 6 5
        9 8 7 6 5 4
        9 8 7 6 5 4 3
        9 8 7 6 5 4 3 2
        9 8 7 6 5 4 3 2 1
    '''

    def __init__(self, steps=9):
        self.steps = steps

    def method_one(self):
        print('\nMethod One')

        _range = [str(i) for i in range(1, self.steps + 1)][::-1]

        for gr in range(1, len(_range) + 1):
            print(' '.join(_range[:gr]))

    def method_two(self):
        print('\nMethod Two')

        for i in range(self.steps, 0, -1):
            for j in range(self.steps, i - 1, -1):
                print(j, end=' ')

            print()


if __name__ == '__main__':
    pattern_sixteen = Pattern_Sixteen()

    pattern_sixteen.method_one()
    pattern_sixteen.method_two()
