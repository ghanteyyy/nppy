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
        _range = [str(i) for i in range(1, steps + 1)]

        for i in range(1, len(_range)):
            print(' '.join(_range[:i]))


if __name__ == '__main__':
    Pattern_Fifteen()
