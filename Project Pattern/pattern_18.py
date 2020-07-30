class Pattern_Eightteen:
    ''' Pattern eighteen

        9 8 7 6 5 4 3 2 1
        9 8 7 6 5 4 3 2
        9 8 7 6 5 4 3
        9 8 7 6 5 4
        9 8 7 6 5
        9 8 7 6
        9 8 7
        9 8
        9
    '''

    def __init__(self, steps=9):
        _range = [str(i) for i in range(1, steps + 1)][::-1]

        for i in range(len(_range), 0, -1):
            print(' '.join(_range[:i]))


if __name__ == '__main__':
    Pattern_Eightteen()
