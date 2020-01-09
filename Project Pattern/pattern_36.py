def pattern_thirty_six():
    '''Pattern thirty_six

        1
        1 2
        1   3
        1     4
        1 2 3 4 5
    '''
    num = '12345'

    for i in range(1, 6):
        x = num[:i]

        if i in range(2, 5):
            space = 2 * (i - 1) - i  # using 2*n - 1 for getting required space where n = 1, 2, 3, .... and here n = i - 1
            print(x[0] + ' ' * space + x[-1])

        elif i == 5:
            print(' '.join(num))

        else:
            print(x)


if __name__ == '__main__':
    pattern_thirty_six()
