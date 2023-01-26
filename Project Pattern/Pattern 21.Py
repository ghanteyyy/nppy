class Pattern_Twenty_One:
    '''
        1
        2 2
        3 3 3
        4 4 4 4
        5 5 5 5 5
        6 6 6 6 6 6
        7 7 7 7 7 7 7
        8 8 8 8 8 8 8 8
        9 9 9 9 9 9 9 9 9
    '''

    def __init__(self, steps=9):
        self.steps = steps

    def method_one(self):
        print('\nMethod One')

        for i in range(1, self.steps + 1):
            print(' '.join(str(i) * i))

    def method_two(self):
        print('\nMethod Two')

        for i in range(1, self.steps + 1):
            k = i

            for j in range(1, i):
                k = k * 10 + i

            print(' '.join(str(k)))

    def method_three(self):
        print('\nMethod Three')

        for i in range(1, self.steps + 1):
            for _ in range(1, i + 1):
                print(i, end=' ')

            print()


if __name__ == '__main__':
    pattern_twenty_one = Pattern_Twenty_One()

    pattern_twenty_one.method_one()
    pattern_twenty_one.method_two()
    pattern_twenty_one.method_three()
