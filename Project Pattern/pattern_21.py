class Pattern_Twenty_One:
    '''Pattern twenty_one

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

    def __init__(self):
        for i in range(1, 10):
            print(' '.join(str(i) * i))


if __name__ == '__main__':
    Pattern_Twenty_One()
